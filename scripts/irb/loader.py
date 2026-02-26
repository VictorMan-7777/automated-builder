"""loader.py — Spec YAML reader and validator."""
from __future__ import annotations

from pathlib import Path


def load_spec(spec_path: Path) -> dict:
    """Load and validate a tier-N-spec.yaml file.

    Raises ImportError if PyYAML is not installed.
    Raises ValueError if required top-level keys are missing.
    """
    try:
        import yaml
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required by the IRB runner. "
            "Install with: pip install pyyaml"
        ) from exc

    with open(spec_path, encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)

    if spec is None:
        raise ValueError("Spec is empty")
    if not isinstance(spec, dict):
        raise ValueError(f"Spec root must be a mapping/object, got {type(spec).__name__}")

    required = ["spec_id", "spec_version", "tier", "checks"]
    missing = [k for k in required if k not in spec]
    if missing:
        raise ValueError(f"Spec missing required keys: {missing}")

    if not isinstance(spec["checks"], list) or not spec["checks"]:
        raise ValueError("spec.checks must be a non-empty list")

    return spec
