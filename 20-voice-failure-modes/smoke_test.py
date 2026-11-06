"""Smoke test for Lesson 20: fault table matches the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "failure_modes.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["reference_hardened"]["success"] == 12
    assert result["consent_gate_off"]["escapes"] == 1
    assert result["consent_gate_off"]["failed_ids"] == ["call-05"]
    assert result["card_storage_on"]["escapes"] == 1
    assert result["card_storage_on"]["failed_ids"] == ["call-07"]
    assert result["aggressive_endpoint_300"]["success"] == 10
    assert result["aggressive_endpoint_300"]["cutoffs"] == 6
    assert result["confirmation_off"]["success"] == 6
    print("smoke ok")


if __name__ == "__main__":
    main()
