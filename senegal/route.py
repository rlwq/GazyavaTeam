import itertools, json
import model_utils as mu

fb = mu.load_fact_bank()
res = {}
for qid, q in fb.items():
    best = None
    for tier, style, fewshot, context in itertools.product(mu.TIERS, mu.STYLES, [False, True], [False, True]):
        call = mu.build_call(q, tier, style, fewshot, context)
        if mu.question_passes(q["slots"], call["answer"]) and (best is None or call["tokens"] < best[0]):
            best = (call["tokens"], {"tier": tier, "style": style, "fewshot": fewshot, "context": context})
    res[qid] = best[1]
    print(qid, best)

mu.save_json(res, mu.HERE / "routing_config.json")
