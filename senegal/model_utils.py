"""Shared contract between generate_dataset.py, main_template.py and
evaluation_script.py: the deterministic "simulated LLM gateway" that stands
in for a real text-to-speech-cost LLM API, plus the token counter and
quality-coverage scorer built on top of it.

There is no real model here and no network/API calls - `build_call()`
renders a prompt and a completion from fixed templates and the shipped fact
bank (`dataset/fact_bank.json`), so the whole pipeline is deterministic,
offline and reproducible. Every "model" behaviour a participant can exploit
or must route around is visible in this file and in the fact bank; nothing
about the cost or quality mechanism is hidden.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
DATASET_DIR = HERE / "dataset"
FACT_BANK_PATH = DATASET_DIR / "fact_bank.json"
EXAMPLE_NAIVE_CONFIG_PATH = DATASET_DIR / "example_naive_config.json"

TIERS = ("cheap", "large")
STYLES = ("verbose", "terse")

PREAMBLE = {
    "cheap": "You are the Teranga FM quick-reply bot. Answer fast.",
    "large": (
        "You are the Teranga FM flagship assistant, an exhaustively trained "
        "large language model serving farmers and residents across the "
        "Peanut Basin. Always be thorough, polite, and comprehensive in "
        "every reply you give, and make sure the person asking never feels rushed."
    ),
}

INSTRUCTION = {
    "verbose": (
        "Please answer the following question in a warm, detailed, and "
        "complete manner, making sure to explain your reasoning, add "
        "helpful context, and double check that nothing important has "
        "been left out before you respond."
    ),
    "terse": "Answer:",
}

FEWSHOT_BLOCK = (
    "Example Q: What is the capital of Mali?\n"
    "Example A: Bamako is the capital of Mali.\n"
    "Example Q: What currency does Nigeria use?\n"
    "Example A: Nigeria uses the Nigerian naira."
)

INTRO = "Thanks so much for reaching out to the Teranga FM helpline! "
OUTRO = " We hope this fully answers your question, feel free to call back any time with more!"

TOKEN_BUDGET = 1200
FLAG = "SIGMOID_TOKENDIET"


def count_tokens(text: str) -> int:
    """Deterministic stand-in for a real BPE tokenizer: words and
    punctuation marks each count as one token. Dependency-free and
    reproducible everywhere, which is what matters for grading - not
    fidelity to any particular real tokenizer."""
    return len(re.findall(r"\w+|[^\w\s]", text))


def load_fact_bank(path: Path = FACT_BANK_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def validate_config(config: dict, fact_bank: dict) -> None:
    missing = [qid for qid in fact_bank if qid not in config]
    if missing:
        raise ValueError(f"routing_config.json is missing entries for: {missing}")
    for qid, choice in config.items():
        if qid not in fact_bank:
            raise ValueError(f"routing_config.json references unknown question id: {qid}")
        if choice.get("tier") not in TIERS:
            raise ValueError(f"{qid}: tier must be one of {TIERS}")
        if choice.get("style") not in STYLES:
            raise ValueError(f"{qid}: style must be one of {STYLES}")
        if not isinstance(choice.get("fewshot"), bool):
            raise ValueError(f"{qid}: fewshot must be true or false")
        if not isinstance(choice.get("context"), bool):
            raise ValueError(f"{qid}: context must be true or false")


def render_completion_body(slots: list[dict], tier: str, style: str, context: bool) -> str:
    assisted = tier == "large" or context
    included = [s["phrasings"][0] for s in slots if assisted or not s["large_only"]]
    facts = "; ".join(included) + "." if included else "I'm not sure, please ask a human agent."
    return (INTRO + facts + OUTRO) if style == "verbose" else facts


def build_call(question: dict, tier: str, style: str, fewshot: bool, context: bool) -> dict:
    """Builds the (simulated) prompt and completion for a single question
    under one (tier, style, fewshot, context) choice, and counts tokens
    across both - prompt tokens are billed just like completion tokens,
    exactly as a real LLM API would bill them.

    `context` attaches the question's context snippet (if it has one) to the
    prompt. On the cheap tier it compensates for every fact slot that tier
    would otherwise drop - the same way retrieval-augmented generation lets
    a smaller model match a bigger one's coverage, at the cost of the
    retrieved passage's own tokens. On the large tier it does nothing: the
    large tier already covers every slot, so attaching it is pure waste.
    """
    prompt_parts = [PREAMBLE[tier], INSTRUCTION[style]]
    if fewshot:
        prompt_parts.append(FEWSHOT_BLOCK)
    snippet = question.get("context_snippet")
    if context and snippet:
        prompt_parts.append(f"Context: {snippet}")
    prompt_parts.append(f"Q: {question['question']}")
    prompt = "\n".join(prompt_parts)

    body = render_completion_body(question["slots"], tier, style, context and bool(snippet))
    completion = f"A: {body}"

    tokens = count_tokens(prompt) + count_tokens(completion)
    return {"prompt": prompt, "completion": completion, "answer": body, "tokens": tokens}


def slot_covered(slot: dict, answer_text: str) -> bool:
    lowered = answer_text.lower()
    return any(variant.lower() in lowered for variant in slot["phrasings"])


def question_passes(slots: list[dict], answer_text: str) -> bool:
    """A question's quality bar: every required fact slot must be present
    in the answer text. Omitting even one fails that question - no partial
    credit, no LLM judge, just a deterministic substring scan."""
    return all(slot_covered(slot, answer_text) for slot in slots)


def run_config(config: dict, fact_bank: dict) -> dict:
    """Regenerates every call from scratch using ONLY the routing config and
    the shipped fact bank - this is what both main_template.py and
    evaluation_script.py call, so a submission is graded on what its config
    actually produces, never on a hand-edited answers.json."""
    validate_config(config, fact_bank)
    per_question = {}
    total_tokens = 0
    all_pass = True
    for qid, question in fact_bank.items():
        choice = config[qid]
        call = build_call(question, choice["tier"], choice["style"], choice["fewshot"], choice["context"])
        passed = question_passes(question["slots"], call["answer"])
        all_pass = all_pass and passed
        total_tokens += call["tokens"]
        per_question[qid] = {
            "answer": call["answer"],
            "tokens": call["tokens"],
            "pass": passed,
        }
    return {
        "per_question": per_question,
        "total_tokens": total_tokens,
        "quality_gate": all_pass,
        "budget_gate": total_tokens <= TOKEN_BUDGET,
    }
