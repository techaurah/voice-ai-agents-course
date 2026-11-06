"""Smoke test for Lesson 08: condition table matches the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "noise_sweep.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    cond = result["by_condition"]
    assert cond["telephony_clean"] == {"n": 7, "mean_wer": 0.0848}
    assert cond["telephony_snr12"] == {"n": 2, "mean_wer": 0.0}
    assert cond["wideband_clean"] == {"n": 7, "mean_wer": 0.0321}
    assert cond["wideband_snr5"] == {"n": 1, "mean_wer": 0.3333}
    assert result["by_tag"]["spelling"]["mean_wer"] == 0.1496
    assert result["by_tag"]["digits"]["mean_wer"] == 0.0278
    print("smoke ok")


if __name__ == "__main__":
    main()
