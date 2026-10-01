#!/usr/bin/env python3
"""English → Nigerian Pidgin (local Marian) then SNO-normalize (rules).

Optional deps: see requirements-translate.txt (torch, transformers, sentencepiece, sacremoses).
Does not write dictionary.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "NITHUB-AI/marian-mt-bbc-en-pcm"
# Pin HF Hub revision; bump intentionally when upgrading.
DEFAULT_MODEL_REVISION = "main"

_tokenizer = None
_model = None
_model_name: str | None = None
_moses_tok = None
_moses_detok = None
_moses_ready: bool | None = None

# Soft smoke cases: English → at least one expected substring in raw or SNO output.
EVAL_CASES: list[tuple[str, list[str]]] = [
    ("I want a book.", ["buk", "book"]),
    ("How are you?", ["haw", "how", "yu", "you", "de", "dey"]),
    ("Come here now.", ["kom", "come", "hia", "here", "nau", "now"]),
    ("The food is sweet.", ["fud", "food", "swit", "sweet"]),
    ("Give me water.", ["giv", "give", "wata", "wota", "water"]),
]


def deps_ok() -> tuple[bool, str]:
    try:
        import torch  # noqa: F401
        import transformers  # noqa: F401
    except ImportError as e:
        return False, (
            "Missing optional deps for translation. Install:\n"
            "  pip install -r requirements-translate.txt\n"
            f"({e})"
        )
    return True, ""


def moses_ok() -> bool:
    """True if sacremoses is importable (used for EN Moses tokenize / pcm detokenize)."""
    global _moses_ready, _moses_tok, _moses_detok
    if _moses_ready is not None:
        return _moses_ready
    try:
        from sacremoses import MosesDetokenizer, MosesTokenizer

        _moses_tok = MosesTokenizer(lang="en")
        _moses_detok = MosesDetokenizer(lang="en")
        _moses_ready = True
    except ImportError:
        _moses_tok = None
        _moses_detok = None
        _moses_ready = False
    return _moses_ready


def preprocess_en(text: str) -> str:
    """Moses-tokenize English when sacremoses is available (Marian training convention)."""
    if not text.strip():
        return text
    if moses_ok() and _moses_tok is not None:
        return _moses_tok.tokenize(text, return_str=True)
    return text


def postprocess_pcm(text: str) -> str:
    """Detokenize Marian pcm when sacremoses is available."""
    if not text.strip():
        return text
    if moses_ok() and _moses_detok is not None:
        return _moses_detok.detokenize(text.split())
    return text


def load_mt(model_name: str = DEFAULT_MODEL):
    global _tokenizer, _model, _model_name
    ok, msg = deps_ok()
    if not ok:
        raise RuntimeError(msg)
    if _model is not None and _model_name == model_name:
        return _tokenizer, _model
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    _tokenizer = AutoTokenizer.from_pretrained(
        model_name, revision=DEFAULT_MODEL_REVISION
    )
    _model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name, revision=DEFAULT_MODEL_REVISION
    )
    _model.eval()
    _model_name = model_name
    return _tokenizer, _model


def translate_raw(
    text: str,
    model_name: str = DEFAULT_MODEL,
    max_length: int = 128,
    *,
    use_moses: bool = True,
) -> str:
    import torch

    tok, model = load_mt(model_name)
    src = preprocess_en(text) if use_moses else text
    inputs = tok(src, return_tensors="pt", truncation=True, max_length=max_length)
    with torch.no_grad():
        out = model.generate(**inputs, max_length=max_length, num_beams=4)
    decoded = tok.decode(out[0], skip_special_tokens=True).strip()
    return postprocess_pcm(decoded) if use_moses else decoded


def translate_and_normalize(
    text: str,
    model_name: str = DEFAULT_MODEL,
    max_length: int = 128,
    *,
    use_moses: bool = True,
) -> dict:
    """EN → pcm (Marian) → SNO via rules normalizer."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from normalize import normalize_sentence

    raw = translate_raw(
        text, model_name=model_name, max_length=max_length, use_moses=use_moses
    )
    normed = normalize_sentence(raw, backend="rules")
    return {
        "input": text,
        "pcm_raw": raw,
        "output": normed["output"],
        "tokens": normed["tokens"],
        "mt_model": model_name,
        "moses": bool(use_moses and moses_ok()),
        "pipeline": "marian_en_pcm+rules",
        "max_length": max_length,
    }


def run_eval(model_name: str = DEFAULT_MODEL, *, use_moses: bool = True) -> int:
    """Soft smoke eval: each case must hit ≥1 expected substring in raw or SNO."""
    ok_n = 0
    rows = []
    for en, expect in EVAL_CASES:
        try:
            r = translate_and_normalize(en, model_name=model_name, use_moses=use_moses)
        except Exception as e:
            print(f"FAIL  {en!r}: {e}", file=sys.stderr)
            rows.append({"en": en, "ok": False, "error": str(e)})
            continue
        blob = f"{r['pcm_raw']} {r['output']}".casefold()
        hit = next((e for e in expect if e.casefold() in blob), None)
        passed = hit is not None
        ok_n += int(passed)
        mark = "OK" if passed else "MISS"
        print(f"{mark}  {en!r}")
        print(f"     raw: {r['pcm_raw']}")
        print(f"     sno: {r['output']}")
        if not passed:
            print(f"     expected one of {expect}", file=sys.stderr)
        rows.append(
            {
                "en": en,
                "ok": passed,
                "hit": hit,
                "pcm_raw": r["pcm_raw"],
                "output": r["output"],
                "moses": r["moses"],
            }
        )
    total = len(EVAL_CASES)
    print(f"eval {ok_n}/{total}  moses={bool(use_moses and moses_ok())}  model={model_name}")
    return 0 if ok_n == total else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Translate English → Pidgin (local) then SNO-normalize.")
    p.add_argument("text", nargs="?", help="English sentence")
    p.add_argument("--model", default=DEFAULT_MODEL, help="Hugging Face model id")
    p.add_argument(
        "--max-length",
        type=int,
        default=128,
        help="Marian encode/generate max_length (same as translate_raw)",
    )
    p.add_argument("--json", action="store_true", help="Emit full JSON")
    p.add_argument("--check-deps", action="store_true", help="Verify optional packages")
    p.add_argument("--eval", action="store_true", help="Run soft smoke eval cases")
    p.add_argument(
        "--no-moses",
        action="store_true",
        help="Skip sacremoses tokenize/detokenize (compare / fallback)",
    )
    args = p.parse_args(argv)

    if args.check_deps:
        ok, msg = deps_ok()
        if not ok:
            print(msg)
            return 1
        print("OK core:", "torch+transformers")
        print("OK moses:" if moses_ok() else "MISS moses (optional):", "sacremoses" if moses_ok() else "pip install sacremoses")
        return 0

    if args.eval:
        return run_eval(model_name=args.model, use_moses=not args.no_moses)

    if not args.text:
        p.print_help()
        return 2

    try:
        result = translate_and_normalize(
            args.text,
            model_name=args.model,
            max_length=args.max_length,
            use_moses=not args.no_moses,
        )
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
