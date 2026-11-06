"""Smoke test for Lesson 04: channel measurements match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "telephony.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["wideband_samples"] == 78080
    assert result["telephony_samples"] == 39040
    assert result["mulaw_quantisation_snr_db"] == 37.3
    assert result["power_1000hz_wideband"] == 0.04
    assert result["power_1000hz_telephony"] == 0.0384
    assert result["power_6000hz_wideband"] == 0.04
    assert result["power_6000hz_after_chain_and_upsample"] == 0.000126
    assert result["power_2000hz_alias_in_telephony"] == 0.0058
    print("smoke ok")


if __name__ == "__main__":
    main()
