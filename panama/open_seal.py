#!/usr/bin/env python3
"""Compliance desk of the Panama Canal Authority: opens the sealed audit certificate.

The certificate in audit_seal.json is locked with the findings of the audit
itself. It opens only for a report whose list of excluded benchmark items is
exactly the one the evidence supports: no item missing, no extra item.

Usage:
    python open_seal.py report.json
    python open_seal.py report.json --seal audit_seal.json

report.json is either {"excluded_ids": ["<id>", ...]} or a bare JSON list of
ids. Order and duplicates do not matter. Standard library only.
"""

import argparse
import hashlib
import hmac
import json
import sys
from pathlib import Path

ITERATIONS = 200_000
SCHEME = "pbkdf2-sha256 / sha256-ctr / hmac-sha256"


def canonical(ids) -> bytes:
    """Sorted, de-duplicated ids, one per line."""
    return "\n".join(sorted({str(i).strip() for i in ids})).encode("utf-8")


def derive_keys(ids, salt: bytes):
    """(encryption key, mac key) derived from the exact set of ids."""
    material = hashlib.pbkdf2_hmac("sha256", canonical(ids), salt, ITERATIONS, dklen=64)
    return material[:32], material[32:]


def keystream_xor(key: bytes, data: bytes) -> bytes:
    """XOR data with a SHA-256 counter-mode keystream (encrypt == decrypt)."""
    out = bytearray()
    for block, start in enumerate(range(0, len(data), 32)):
        pad = hashlib.sha256(key + block.to_bytes(4, "big")).digest()
        out.extend(b ^ p for b, p in zip(data[start:start + 32], pad))
    return bytes(out)


def mac(key: bytes, salt: bytes, ciphertext: bytes) -> bytes:
    return hmac.new(key, salt + ciphertext, hashlib.sha256).digest()


def unseal(seal: dict, ids):
    """Return the certificate payload (dict), or None if the ids do not open the seal."""
    salt = bytes.fromhex(seal["salt"])
    ciphertext = bytes.fromhex(seal["ciphertext"])
    enc_key, mac_key = derive_keys(ids, salt)
    if not hmac.compare_digest(mac(mac_key, salt, ciphertext), bytes.fromhex(seal["tag"])):
        return None
    return json.loads(keystream_xor(enc_key, ciphertext).decode("utf-8"))


def read_ids(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data["excluded_ids"]
    if not isinstance(data, list):
        raise ValueError("expected a list of ids")
    return [str(i) for i in data]


def main() -> int:
    ap = argparse.ArgumentParser(description="Open the sealed CanalQA audit certificate.")
    ap.add_argument("report", type=Path, help="report.json with the excluded benchmark ids")
    ap.add_argument("--seal", type=Path, default=Path(__file__).resolve().with_name("audit_seal.json"))
    args = ap.parse_args()

    try:
        ids = read_ids(args.report)
        seal = json.loads(args.seal.read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError) as exc:
        print(f"[!] Cannot read the inputs: {exc}", file=sys.stderr)
        return 2

    payload = unseal(seal, ids)
    if payload is None:
        print(f"The seal holds. A report of {len(set(ids))} excluded items does not match the evidence.")
        return 1
    print("Seal opened.")
    print(f"  certified honest accuracy: {payload['certified_honest_accuracy'] * 100:.2f}%")
    print(f"  flag: {payload['flag']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
