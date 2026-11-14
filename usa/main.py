import json, tiktoken

d = json.load(open("test-input.json"))
for name in tiktoken.list_encoding_names():
    enc = tiktoken.get_encoding(name)
    if enc.encode(d["calibration"]["text"], allowed_special="all") == d["calibration"]["token_ids"]:
        res = {"tokenizer_id": name, "decoded_message": enc.decode(d["challenge"]["token_ids"])}
        break

json.dump(res, open("test-output.json", "w"), indent=2, ensure_ascii=False)
