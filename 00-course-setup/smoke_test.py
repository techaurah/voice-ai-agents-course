"""Smoke test for Lesson 00: the environment check reports the
fixture counts and WAV round trip recorded in the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "check_environment.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["python_ok"] is True
    assert result["wav_roundtrip_samples"] == 16000
    assert result["wav_rate"] == 16000
    assert result["transcripts"] == 24
    assert result["calls"] == 12
    assert result["schedule_slots"] == 19
    assert result["clinic"] == "BrightSmile Dental"
    print("smoke ok")


if __name__ == "__main__":
    main()
