# The Great American Token Mystery (United States)

The flag is inside the decoded message (printed by the evaluator).

We get a calibration text with its token IDs, plus secret token IDs. Different tokenizers give different IDs for the
same text. So we try every tiktoken encoding: the one that reproduces the calibration IDs exactly is the right one,
and we decode the secret IDs with it.

Nothing is hardcoded, so it also works on the hidden test, which uses a different tokenizer. On the training sample
the match is `p50k_base`.

```python
for name in tiktoken.list_encoding_names():
    enc = tiktoken.get_encoding(name)
    if enc.encode(d["calibration"]["text"], allowed_special="all") == d["calibration"]["token_ids"]:
        res = {"tokenizer_id": name,
               "decoded_message": enc.decode(d["challenge"]["token_ids"])}
        break
```

Run: `pip install tiktoken && python main.py`
