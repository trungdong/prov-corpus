# prov-corpus

A W3C PROV conformance corpus. It holds PROV-JSON, PROV-N, PROV-JSON-LD and PROV-CONSTRAINTS fixtures, taken from the test suite of [prov](https://github.com/trungdong/prov) (ProvPy) 3.2.1.

Two libraries consume it:

- [prov](https://github.com/trungdong/prov), the Python library.
- provkit, the Rust crate, which pulls this repository in as a git submodule.

## Layout

| Directory | Files | Source | Licence | Profile (PROV-N) |
|---|---|---|---|---|
| `json/` | 398 `.json` | ProvToolbox shared test corpus, via ProvPy | MIT | n/a |
| `provn/spec/prov-n/` | 64 | Examples in the PROV-N Recommendation, extracted by `tools/extract_spec_examples.py` | W3C Document Licence | strict |
| `provn/spec/prov-dm/` | 63 | Examples in the PROV-DM Recommendation, same treatment | W3C Document Licence | strict |
| `provn/provtoolbox/` | 9 | `modules-core/prov-n/src/test/resources/prov/*.provn` in ProvToolbox | MIT | default |
| `provn/provtoolbox-corpus/` | 388 | PROV-N written by ProvToolbox from the shared JSON corpus; each file has a same-named file in `json/` | MIT | default |
| `provn/probes/` | 204 `.provn` and `expected.tsv` | Short PROV-N texts written for this corpus by `tools/gen_probes.py`, each with the result the grammar requires | MIT | strict and default, per probe |
| `jsonld/` | 2 | PROV-JSON-LD examples, via ProvPy | MIT | n/a |
| `constraints/` | 171 `.json` | PROV-CONSTRAINTS unification cases (see below) | MIT and W3C test suite licence | n/a |

`provn/README.md` describes the PROV-N sets in full, including the known differences between the PROV-N and JSON fixtures. `provn/probes/README.md` describes the probes and the columns of `expected.tsv`.

The `constraints/` directory holds 157 files converted from PROV-XML by `tools/convert_constraints.py` (150 ProvToolbox `.xml` cases and 7 W3C `type-*.provx` cases) and 14 files that were already PROV-JSON in ProvPy. `constraints/README.md` is ProvPy's original README for the PROV-XML sources and its naming convention (`-successN`, `-failN`, `PASS`, `FAIL`).

## Stability rule

A file is never renamed or edited after a tag. A correction is a new file and a new tag.

## PROV-N spec examples that do not parse

`EXCLUDED_SPEC_EXAMPLES` names this list in ProvPy's test suite. Consumers keep their own copy of the list.

Each of these is either not a complete PROV-N statement, or a statement the formal grammar
rejects even though the Recommendation's prose presents it as valid. Listed in
`EXCLUDED_SPEC_EXAMPLES`.

- `prov-n-example-16.provn` - the sixth `wasGeneratedBy` variant reuses `tr:WD-prov-dm-20111215`
  as its time argument, which is not a dateTime; a copy-paste artefact in the Recommendation's
  own text
- `prov-n-example-37.provn` - `wasAssociatedWith(ex:a1, ex:ag1)` gives the agent without the
  paired plan; production [20] requires them together
- `prov-n-example-51.provn` - a `default` declaration follows a `prefix` declaration; production
  [45] puts the `default` before every `prefix`
- `prov-n-example-52.provn`, `prov-n-example-53.provn` - a bare typed-literal pair, not a
  statement
- `prov-n-example-54.provn` - a bare qualified-name literal pair, not a statement
- `prov-n-example-55.provn`, `prov-n-example-56.provn` - a list of bare literals, not a
  statement
- `prov-n-example-59.provn` - a literal ellipsis elides the rest of the example, not complete
  PROV-N
- `prov-n-example-61.provn` - the bundle identifier `b` has no declared default namespace; the
  example illustrates qualified-name resolution for `ex:e001`, not the bundle name itself
- `prov-dm-example-03.provn`, `prov-dm-example-04.provn` - `used`/`wasGeneratedBy` give only the
  entity/activity without the paired time; the formal grammar requires them together
- `prov-dm-example-05.provn`, `prov-dm-example-06.provn` - a literal ellipsis elides the
  bundle's content, not complete PROV-N
- `prov-dm-example-16.provn` - `wasGeneratedBy` gives only the entity without the paired time
- `prov-dm-example-19.provn` - a spec typo leaves the agent's attribute list missing its
  closing `]`
- `prov-dm-example-24.provn` - `wasAssociatedWith` and `wasGeneratedBy` give only the
  activity/entity without the paired plan or time
- `prov-dm-example-34.provn`, `prov-dm-example-52.provn` - `wasAssociatedWith` gives only the
  activity and agent without the paired plan
- `prov-dm-example-42.provn` - a statement follows an `endBundle` at document level; production
  [1] puts every expression before the bundles
- `prov-dm-example-53.provn`, `prov-dm-example-56.provn`, `prov-dm-example-63.provn` - `used`
  gives only the activity and entity without the paired time
- `prov-dm-example-55.provn` - `used`/`wasGeneratedBy` give only the activity/entity without
  the paired time
- `prov-dm-example-57.provn` - a list of bare literals, not a statement
- `prov-dm-example-58.provn` - a bare typed-literal pair, not a statement
- `prov-dm-example-59.provn` - a bare qualified-name literal, not a statement

The `provn/README.md` file also lists the ProvToolbox documents that do not parse under the default profile.

## Constraints files not converted

ProvPy cannot read three ProvToolbox PROV-XML files: `bundle-fail1.xml`, `bundle-success1.xml` and `bundle-success2.xml`. They wrap bundle contents in `<prov:bundle>`, where the PROV-XML schema defines `<prov:bundleContent>` ([prov issue #254](https://github.com/trungdong/prov/issues/254)). They have no `.json` counterpart in `constraints/`. The converter's warning about a dropped `prov:id` attribute comes only from these three files, so no written file lost data.

## Regenerating

`tools/extract_spec_examples.py` extracts the PROV-N and PROV-DM examples from the Recommendations. It writes to `tools/spec/`, so move the output to `provn/spec/`. It exits with an error if a wrapped fragment uses a prefix it does not declare.

`tools/gen_probes.py` writes the files in `provn/probes/`, except `expected.tsv`, which is edited by hand:

```bash
python tools/gen_probes.py
```

`tools/convert_constraints.py` converts the PROV-XML cases to PROV-JSON. It expects the PROV-XML sources under `src/prov/tests/unification/constraints`, taken from the ProvPy 3.2.1 archive:

```bash
git -C path/to/ProvPy archive 3.2.1 src/prov/tests/unification | tar -x
uv run --with prov==3.2.1 --with lxml python tools/convert_constraints.py
```

## Versioning

Tags follow `vMAJOR.MINOR.PATCH`.

- MAJOR: a file is removed or changed.
- MINOR: files are added.
- PATCH: README changes.

### v2.1.0

v2.1.0 adds `provn/probes/`, 204 PROV-N probes with `expected.tsv`, under the MINOR rule. The README now lists `prov-n-example-51` and `prov-dm-example-42` among the spec examples that do not parse, since they break productions [45] and [1]. It no longer lists `prov-n-example-63` and `prov-n-example-64`, which use extensibility expressions that section 5 requires a parser to accept, and it drops the `prov-family` ProvToolbox files from the exclusions for the same reason.

### v2.0.0

v2.0.0 regenerates eight files in `provn/spec/` in place, under the MAJOR rule. The v1.0.0 wrapper did not declare a prefix used only inside a qualified-name literal such as `'cc:attributionURL'` ([issue #1](https://github.com/trungdong/prov-corpus/issues/1)). Each file gains one `prefix` line.

- `prov-n-example-34.provn`, `prov-n-example-35.provn` - prefix `cc`
- `prov-dm-example-27.provn`, `prov-dm-example-31.provn` - prefix `rec54`
- `prov-dm-example-61.provn`, `prov-dm-example-62.provn` - prefix `ex`
- `prov-n-example-54.provn`, `prov-dm-example-59.provn` - prefix `ex`; still excluded, changed only so the script reproduces the corpus

## Licences

See `LICENSE.md`.
