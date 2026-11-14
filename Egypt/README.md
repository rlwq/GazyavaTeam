# Always Valid, No Excuses

Flag: `SIGMOID_PHARAOH` (platform result: PASS 100/100)

`main.py` uses the local model Qwen3-1.7B (GGUF, Q8_0) through llama-cpp-python to turn each OCR record
from `test-input.txt` into one line of strict JSON in `test-output.txt` (line N of the output is the JSON for line N
of the input).

## How it works

1. Each record is split on `|`. A segment is a real field only if it has the shape `key: value` with a simple word key
   (the rule from the task). Everything else (page numbers, chapter headers, `- 45 -`, `[torn]`, `(faded)`, `Fig 3`,
   `###` ...) is scan noise and is dropped. Keys and values are trimmed, only the first `:` splits key and value.
2. The fields are given to the model as lines `key = value`, with a system prompt that states the typing rules and a
   few examples. Thinking mode of Qwen3 is turned off (empty `<think></think>` block).
3. Generation is held to the format with a GBNF grammar built for every record from the task rules:
   the keys in input order, empty value -> `null`, exactly `true`/`false` -> boolean, whole number -> number,
   anything else -> string with `"` and `\` escaped. The model generates the output token by token, but it cannot
   produce invalid JSON, a quoted number, a lost field, a broken backslash or a kept page number.
4. Every model output is parsed with `json.loads` and compared with the rules. If it ever differs (it did not happen
   in any test), the record is written from the rules instead, so the output is always valid. The script prints how
   many model outputs were rejected.

Decoding is greedy (`temperature=0`, `seed=0`), so the result is deterministic.

## Requirements

- Python 3.10-3.12
- `huggingface-hub==0.26.2`, `llama-cpp-python==0.3.35` built with CUDA (see `requirements.txt`)
- the model file `models/Qwen3-1.7B-Q8_0.gguf` (about 1.8 GB, not in the repository)

## How to reproduce

1. Install the dependencies (llama-cpp-python with CUDA):
   ```
   CMAKE_ARGS="-DGGML_CUDA=on" pip install -r requirements.txt
   ```
2. Download the model once into `models/` next to `main.py`:
   ```
   huggingface-cli download Qwen/Qwen3-1.7B-GGUF Qwen3-1.7B-Q8_0.gguf --local-dir models
   ```
   SHA256 of the file: `061b54daade076b5d3362dac252678d17da8c68f07560be70818cace6590cb1a`
3. Put the records into `test-input.txt` next to `main.py`. To check on the sample data:
   ```
   cp train-input.txt test-input.txt
   ```
4. Run (offline, non-interactive):
   ```
   python main.py
   ```
   It writes `test-output.txt` and prints `N records written, 0 model outputs rejected`.
5. Compare with the sample answers (the grader compares parsed data, not bytes):
   ```
   python -c "import json;a=[json.loads(l) for l in open('test-output.txt',encoding='utf-8')];b=[json.loads(l) for l in open('train-output.txt',encoding='utf-8')];print(sum(x==y for x,y in zip(a,b)),'/',len(b))"
   ```

## Results

- Hidden test set (100 records): `100 records written, 0 model outputs rejected`, accepted by the platform as PASS 100/100.
- Sample data: 13/13 records match `train-output.txt`, 0 model outputs rejected.
- 100 extra generated records with harder cases (quotes, backslashes, `1.5`, `-2.75`, `#5`, `TRUE`, `null` as text,
  values with several colons, many kinds of noise): 100/100 correct straight from the model.
- For comparison, the same model without the grammar got only 53/100 on these records
  (it turned `-2.75` into `-2`, dropped quotes, kept `Fig 3` and `page 7` as fields).
