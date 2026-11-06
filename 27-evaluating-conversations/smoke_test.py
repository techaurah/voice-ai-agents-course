"""Smoke test for Lesson 27: family table matches the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "eval_conversations.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    as_built = result["as_built"]
    assert as_built["overall"] == {"success": 6, "of": 12}
    families = as_built["families"]
    assert families["slow_speakers"] == {"success": 0, "of": 2}
    assert families["clean_bookings"] == {"success": 1, "of": 2}
    assert families["safety_paths"] == {"success": 3, "of": 3}
    assert families["spoken_number_chunks"] == {"success": 0, "of": 1}
    assert result["hardened"]["overall"] == {"success": 12, "of": 12}
    print("smoke ok")


if __name__ == "__main__":
    main()
