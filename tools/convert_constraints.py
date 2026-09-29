"""Convert the PROV-CONSTRAINTS unification cases from PROV-XML to PROV-JSON.

Run once with prov==3.2.1 (``uv run --with prov==3.2.1 --with lxml python tools/convert_constraints.py``).
Reads ``*.xml`` (ProvToolbox) and ``*.provx`` (W3C test suite) files. Files
ProvPy cannot read are listed on stderr and in README.md; they are not
written.
"""
import sys
from pathlib import Path

from prov.model import ProvDocument

SRC = Path("src/prov/tests/unification/constraints")
DST = Path("constraints")


def main() -> None:
    skipped = []
    paths = sorted([*SRC.glob("*.xml"), *SRC.glob("*.provx")])
    for path in paths:
        try:
            with path.open("rb") as fh:
                doc = ProvDocument.deserialize(source=fh, format="xml")
        except Exception as exc:  # noqa: BLE001 - report and continue
            skipped.append(f"{path.name}: {type(exc).__name__}")
            continue
        (DST / path.with_suffix(".json").name).write_text(
            doc.serialize(format="json", indent=2) + "\n", encoding="utf-8"
        )
    for line in skipped:
        print("skipped", line, file=sys.stderr)


if __name__ == "__main__":
    main()
