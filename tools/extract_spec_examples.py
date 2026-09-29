"""Extract the PROV-N examples from the W3C PROV-N and PROV-DM
Recommendations into ``spec/prov-n/`` and ``spec/prov-dm/`` beside this
script, that is ``tools/spec/``. In the corpus these directories live at
``provn/spec/``, so move the output there.

Fragments (anything not already a ``document ... endDocument``) are wrapped
in a document that declares a default namespace and every prefix the
fragment uses, each under ``http://example.org/<prefix>/``. Run from the
repository root:

    uv run python tools/extract_spec_examples.py

The Recommendations are fetched from w3.org; the generated files are
committed so the tests need no network.
"""

from __future__ import annotations

import html
import re
import urllib.request
from pathlib import Path

SOURCES = {
    "prov-n": "https://www.w3.org/TR/2013/REC-prov-n-20130430/",
    "prov-dm": "https://www.w3.org/TR/2013/REC-prov-dm-20130430/",
}
_BLOCK = re.compile(r'<pre class="codeexample"[^>]*>(.*?)</pre>', re.S)
_TAG = re.compile(r"<[^>]+>")
_PREFIX = re.compile(r"(?<![\w<:/])([A-Za-z][\w.-]*):(?=[\w%\\])")
_STRIP_STRINGS = re.compile(r'"(?:\\.|[^"\\])*"|<[^>]*>|\'(?:\\.|[^\'\\])*\'')
_STRIP_STRINGS_AND_IRIS = re.compile(r'"(?:\\.|[^"\\])*"|<[^>]*>')
# A fragment occasionally declares its own prefix (e.g. to show a later
# redeclaration); wrap() must not add a second, conflicting declaration for it.
_SELF_DECLARED_PREFIX = re.compile(r"(?m)^\s*prefix\s+([A-Za-z][\w.-]*)\s+<")


def used_prefixes(fragment: str) -> set[str]:
    """Prefixes in the fragment's qualified names, including those inside
    single-quoted qualified-name literals such as ``'cc:attributionURL'``."""
    used: set[str] = set()

    def strip(match: re.Match[str]) -> str:
        literal = match.group(0)
        if literal.startswith("'"):
            used.update(_PREFIX.findall(literal[1:-1]))
        return ""

    used.update(_PREFIX.findall(_STRIP_STRINGS.sub(strip, fragment)))
    return used


def check_declared(document: str, name: str) -> None:
    """Fail if the wrapped document uses a prefix it does not declare.

    Scans independently of used_prefixes(), keeping qualified-name literals
    in the text and stripping only strings and IRIs.
    """
    used = set(_PREFIX.findall(_STRIP_STRINGS_AND_IRIS.sub("", document)))
    declared = set(_SELF_DECLARED_PREFIX.findall(document)) | {"prov", "xsd"}
    if missing := sorted(used - declared):
        raise SystemExit(f"{name}: undeclared prefixes {', '.join(missing)}")


def wrap(fragment: str) -> str:
    used = used_prefixes(fragment) - {"prov", "xsd"}
    self_declared = set(_SELF_DECLARED_PREFIX.findall(fragment))
    prefixes = sorted(used - self_declared)
    # A default namespace covers the many illustrative fragments that use a
    # bare, unprefixed identifier; PROV-N requires one to be declared before
    # such an identifier can resolve.
    declarations = "  default <http://example.org/>\n"
    declarations += "".join(
        f"  prefix {p} <http://example.org/{p}/>\n" for p in prefixes
    )
    body = "".join(f"  {line}\n" for line in fragment.splitlines())
    return f"document\n{declarations}{body}endDocument\n"


def main() -> None:
    here = Path(__file__).parent
    for name, url in SOURCES.items():
        target = here / "spec" / name
        target.mkdir(parents=True, exist_ok=True)
        # Fixed W3C TR URLs, fetched only when regenerating the vendored corpus.
        page = urllib.request.urlopen(url).read().decode("utf-8")  # nosec B310 # nosemgrep
        blocks = _BLOCK.findall(page)
        if not blocks:
            raise SystemExit(
                f"no <pre class='codeexample'> blocks found at {url}; "
                "the page layout may have changed"
            )
        for index, raw in enumerate(blocks, start=1):
            text = html.unescape(_TAG.sub("", raw)).strip("\n")
            filename = f"{name}-example-{index:02d}.provn"
            if "endDocument" not in text:
                text = wrap(text)
                check_declared(text, filename)
            elif not text.endswith("\n"):
                text += "\n"
            (target / filename).write_text(text, encoding="utf-8")
        print(name, len(blocks), "examples")


if __name__ == "__main__":
    main()
