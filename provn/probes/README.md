# PROV-N probes

204 short PROV-N texts, one per file, each isolating one production or rule of the [PROV-N Recommendation](https://www.w3.org/TR/prov-n/). `expected.tsv` gives the result the grammar requires for each text under two profiles. A reader passes when it accepts or rejects every probe as the row says.

`tools/gen_probes.py` writes the `.provn` files. The files are stored byte for byte (`.gitattributes` turns off line-ending conversion), because some probes test a bare CR, CRLF, a byte-order mark, NUL or a non-breaking space.

## Profiles

| Profile | Meaning |
|---|---|
| `strict` | The whole grammar of the Recommendation, plus the MUST statements in its prose. |
| `default` | `strict` plus these extensions, which PROV-N writers in the wild produce: bare `mentionOf`, `-` in a required position, a `default` declaration after a `prefix`, expressions after bundles, an identifier or attributes on `alternateOf`, `specializationOf` and `hadMember`, and `prefix prov` or `prefix xsd` bound to their own IRIs. |

Everything else is the same under both profiles.

## Columns of `expected.tsv`

The file has a header row and one row per probe, sorted by name. Columns are tab-separated.

| Column | Content |
|---|---|
| `name` | The probe. The text is in `<name>.provn`. |
| `strict` | `accept` or `reject`. |
| `default` | `accept` or `reject`. |
| `rule` | What decides the row: a production number such as `[53]`, a section such as `3.7.4`, or a terminal borrowed from SPARQL 1.0 (`IRI_REF`, `DATETIME`, `LANGTAG`, `WS`). Borrowed terminals carry no number in the Recommendation. A rule ending in `decision` marks a row the Recommendation does not decide (see below). |
| `provpy` | The number of the [prov](https://github.com/trungdong/prov) issue that reports a difference, when ProvPy 3.2.2 accepts or rejects the probe differently from the row under either profile. Empty when it gives the same accept or reject result under both. The column compares acceptance only, not the documents read. |

## Rows marked `decision`

A few rows reject text the grammar accepts. Each is a choice of the reference implementation, provkit, and the `rule` column ends in `decision`:

- an attribute named after the formal of the record that holds it, such as `[prov:activity='ex:a']` on `wasGeneratedBy`;
- a value typed `prov:QUALIFIED_NAME` whose text is not a qualified name, or whose local part PROV-N cannot write;
- two bundles with one identifier;
- more than 64 levels of nesting in an extensibility expression.

A reader that accepts these rows is conformant to the grammar and differs from the reference only on these rows.

## Semantic rules of section 3.7.5

Table 2 of the Recommendation lists statements such as `wasGeneratedBy(ex:e)` and `wasAssociatedWith(ex:a)` as syntactically correct but unacceptable under PROV-DM, because at least one optional argument must be present. The probes `gen_arity_1` and `association_1` accept them. The table describes a rule of the data model, which a syntax reader does not check.

## Integer literals

An integer literal is `accept` or `reject` by its digits alone. The probes do not test which datatype a reader gives it.

## Stability

The stability rule of the repository applies: a probe is not renamed or edited after a tag. A correction is a new probe and a new tag.
