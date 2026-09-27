#!/usr/bin/env python3
"""English → Nigerian Pidgin (local Marian) then SNO-normalize (rules).

Optional deps: transformers, torch, sentencepiece (see requirements-optional.txt).
Does not write dictionary.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "NITHUB-AI/marian-mt-bbc-en-pcm"

_tokenizer = None
_model = None
_model_name: str | None = None


def deps_ok() -> tuple[bool, str]:
    try:
        import torch  # noqa: F401
        import transformers  # noqa: F401
    except ImportError as e:
        return False, (
            "Missing optional deps for translation. Install:\n"
            "  pip install -r requirements-optional.txt\n"
            f"({e})"
        )
    return True, ""


def load_mt(model_name: str = DEFAULT_MODEL):
    global _tokenizer, _model, _model_name
    ok, msg = deps_ok()
    if not ok:
        raise RuntimeError(msg)
    if _model is not None and _model_name == model_name:
        return _tokenizer, _model
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    _tokenizer = AutoTokenizer.from_pretrained(model_name)
    _model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    _model.eval()
    _model_name = model_name
    return _tokenizer, _model


def translate_raw(text: str, model_name: str = DEFAULT_MODEL, max_length: int = 128) -> str:
    import torch

    tok, model = load_mt(model_name)
    inputs = tok(text, return_tensors="pt", truncation=True, max_length=max_length)
    with torch.no_grad():
        out = model.generate(**inputs, max_length=max_length, num_beams=4)
    return tok.decode(out[0], skip_special_tokens=True).strip()


def translate_and_normalize(
    text: str, model_name: str = DEFAULT_MODEL
) -> dict:
    """EN → pcm (Marian) → SNO via rules normalizer."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from normalize import normalize_sentence

    raw = translate_raw(text, model_name=model_name)
    normed = normalize_sentence(raw, backend="rules")
    return {
        "input": text,
        "pcm_raw": raw,
        "output": normed["output"],
        "tokens": normed["tokens"],
        "mt_model": model_name,
        "pipeline": "marian_en_pcm+rules",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Translate English → Pidgin (local) then SNO-normalize.")
    p.add_argument("text", nargs="?", help="English sentence")
    p.add_argument("--model", default=DEFAULT_MODEL, help="Hugging Face model id")
    p.add_argument("--json", action="store_true", help="Emit full JSON")
    p.add_argument("--check-deps", action="store_true", help="Verify optional packages")
    args = p.parse_args(argv)

    if args.check_deps:
        ok, msg = deps_ok()
        print("OK" if ok else msg)
        return 0 if ok else 1

    if not args.text:
        p.print_help()
        return 2

    try:
        result = translate_and_normalize(args.text, model_name=args.model)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["output"])
        if result["pcm_raw"] != result["output"]:
            print(f"(raw pcm: {result['pcm_raw']})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
