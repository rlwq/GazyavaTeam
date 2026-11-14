# Please, You Are So Delusional! (Tanzania)

General AI / RAG retrieval. Flag = the one printed by the repaired pipeline (`SIGMOID_` + 20 hex chars).

## Task

`retrieval_pipeline.py` (starter) must return the best source document from `corpus.jsonl` (744 documents) for
each of the 72 questions in `questions.json`. `flag_utils.py` takes the `verification_code` letter of each
retrieved document, in question order, hashes the string with SHA-256 and prints `SIGMOID_<first 20 hex>`. So
the flag is correct only if **all 72** retrievals are correct.

## Bugs found and fixed (diff against the organizers' starter)

1. **Two different embedding models.** Documents were encoded with `sentence-transformers/all-MiniLM-L6-v2`,
   questions with `intfloat/e5-small-v2`. Vectors from different models live in different spaces, so the
   cosine similarity was meaningless. Fix: both use `intfloat/e5-small-v2`.
2. **Missing e5 prefix.** e5 models are trained with `query: ...` / `passage: ...` prefixes. Queries had it,
   passages did not. Fix: `passage: ` added to every document.
3. **180-character chunks.** Each document was cut into fixed 180-char slices, so a slice often lost the title
   (the place and the station name), and fragments of the wrong document could win. Fix: one chunk = the whole
   document (`title + text`).
4. **Outdated documents.** 72 documents have titles starting with `ARCHIVED` - old versions of the notices
   ("current access notice" questions must return the current one). Fix: archived documents are skipped.

## Run

```
pip install -r requirements.txt
python retrieval_pipeline.py    # writes retrieved_ids.json and prints the flag
```
