# The Great American Token Mystery (United States)

NLP / tokenizers. The flag is inside the decoded message; the evaluator prints it when the submission scores 100%.

## Task

`test-input.json` has a calibration pair (a text and its token IDs) and a list of challenge token IDs.
Find which subword tokenizer produced the calibration IDs, then decode the challenge IDs with it. `main.py` is
run on hidden test files that use a different tokenizer than the training sample, so nothing can be hardcoded.

## Solution

`main.py` tries every tiktoken encoding (`tiktoken.list_encoding_names()`: gpt2/r50k_base, p50k_base,
p50k_edit, cl100k_base, o200k_base, ...):

1. Encode the calibration text (`allowed_special="all"`).
2. If the result is exactly the given calibration `token_ids`, this is the tokenizer.
3. Decode the challenge `token_ids` with it and write `{"tokenizer_id", "decoded_message"}` to `test-output.json`.

An exact match of the whole ID sequence identifies the tokenizer: different vocabularies give different IDs
for the same text.

Training sample: the tokenizer is `p50k_base` and the message is
"TRAIN_SAMPLE: Verification successful ... Token IDs map to p50k_base vocabulary!" (matches `train-output.json`).

## Run

```
pip install tiktoken
python main.py     # reads test-input.json, writes test-output.json
```
