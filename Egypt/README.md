# Always Valid, No Excuses (Egypt)

Flag: `SIGMOID_PHARAOH` (PASS 100/100)

Each OCR record must become one line of strict JSON. First the rules clean the record: split on `|`, keep only
segments shaped like `key: value`, and drop page numbers, `[torn]`, chapter headers and other noise. Then the local
model Qwen3-1.7B (llama.cpp) writes the JSON, guided by a system prompt with the typing rules and a few examples.

The model cannot produce invalid output, because generation is forced by a GBNF grammar built for each record:
keys in input order, empty -> `null`, `true`/`false` -> boolean, whole number -> number, everything else -> escaped
string. Every output is also checked against the rules, with a rule-based fallback; it was never needed.

```python
FIELD = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:(.*)$", re.S)   # a real field; anything else is noise
INT = re.compile(r"^-?\d+$")                                         # only whole numbers become JSON numbers

def convert(llm, record):                                            # grammar_for(): per-record GBNF,
    r = llm(build_prompt(record), grammar=grammar_for(record),       # exact keys in order + value types
            temperature=0.0, max_tokens=1024, stop=["<|im_end|>"], seed=0)
    return r["choices"][0]["text"].strip()
```

Run: download `Qwen3-1.7B-Q8_0.gguf` into `models/`, then `python main.py` (writes `test-output.txt`)
