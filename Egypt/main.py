import json
import os
import re
import sys

from llama_cpp import Llama, LlamaGrammar

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "models", "Qwen3-1.7B-Q8_0.gguf")
IN_FILE = os.path.join(HERE, "test-input.txt")
OUT_FILE = os.path.join(HERE, "test-output.txt")

SYSTEM = """Convert the fields into one line of strict JSON.

Each input line is one field: key = value. Everything after the first " = " is the value, exactly as written.
Output one JSON object with every field, in the same order, nothing else.

Value types:
- empty value -> null
- exactly true or exactly false -> true / false
- the value is ONLY a whole number (like 40, 0, -3) -> a JSON number
- anything else, even if it contains digits or colons (50% lost, 3:1, cost: $200, 1.5) -> a JSON string,
  copied character by character, with " escaped as \\" and \\ escaped as \\\\"""

EXAMPLES = [
    ('page 22| king :Menes| title: ruled with "the Aten" |[torn]| alive :true | Chapter IX',
     '{"king":"Menes","title":"ruled with \\"the Aten\\"","alive":true}'),
    ('god: Thoth | title: "lord of the moon" | scroll: C:\\papyri\\thoth | - 12 -',
     '{"god":"Thoth","title":"\\"lord of the moon\\"","scroll":"C:\\\\papyri\\\\thoth"}'),
    ('  queen:Nefertari| age : 0 |rank:  | (margin) | city :Luxor  ',
     '{"queen":"Nefertari","age":0,"rank":null,"city":"Luxor"}'),
    ('note: time: noon | price: 40 coins | share: 75% gone | span: 3.5 | label: 7 | [torn]',
     '{"note":"time: noon","price":"40 coins","share":"75% gone","span":"3.5","label":7}'),
]

FIELD = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:(.*)$", re.S)
INT = re.compile(r"^-?\d+$")


def fields(record):
    out = []
    for seg in record.split("|"):
        m = FIELD.match(seg)
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


def typed(value):
    if value == "":
        return None
    if value in ("true", "false"):
        return value == "true"
    if INT.match(value):
        return int(value)
    return value


def expected(record):
    return {k: typed(v) for k, v in fields(record)}


def gbnf_literal(text):
    out = []
    for ch in text:
        if ch in '"\\' or not (32 <= ord(ch) < 127):
            out.append(f"\\u{ord(ch):04X}" if ord(ch) <= 0xFFFF else f"\\U{ord(ch):08X}")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def grammar_for(record):
    parts = [gbnf_literal("{")]
    for i, (k, v) in enumerate(fields(record)):
        prefix = "," if i else ""
        parts.append(gbnf_literal(prefix + json.dumps(k) + ":"))
        parts.append(gbnf_literal(json.dumps(typed(v), ensure_ascii=False)))
    parts.append(gbnf_literal("}"))
    return LlamaGrammar.from_string("root ::= " + " ".join(parts), verbose=False)


def user_text(record):
    return "\n".join(f"{k} = {v}" for k, v in fields(record))


def build_prompt(record):
    parts = [f"<|im_start|>system\n{SYSTEM}<|im_end|>\n"]
    for inp, out in EXAMPLES:
        parts.append(f"<|im_start|>user\n{user_text(inp)}<|im_end|>\n")
        parts.append(f"<|im_start|>assistant\n<think>\n\n</think>\n\n{out}<|im_end|>\n")
    parts.append(f"<|im_start|>user\n{user_text(record)}<|im_end|>\n")
    parts.append("<|im_start|>assistant\n<think>\n\n</think>\n\n")
    return "".join(parts)


def convert(llm, record):
    r = llm(build_prompt(record), grammar=grammar_for(record), temperature=0.0,
            max_tokens=1024, stop=["<|im_end|>"], seed=0)
    return r["choices"][0]["text"].strip()


def main():
    llm = Llama(model_path=MODEL, n_gpu_layers=-1, n_ctx=4096, verbose=False, seed=0)

    with open(IN_FILE, encoding="utf-8") as f:
        records = f.read().splitlines()

    lines, bad = [], 0
    for record in records:
        text = convert(llm, record)
        try:
            ok = json.loads(text) == expected(record)
        except json.JSONDecodeError:
            ok = False
        if not ok:
            bad += 1
            text = json.dumps(expected(record), ensure_ascii=False, separators=(",", ":"))
        lines.append(text)

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(lines)} records written, {bad} model outputs rejected", file=sys.stderr)


if __name__ == "__main__":
    main()
