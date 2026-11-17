# PROV-N probes

228 short PROV-N texts, one per file, each isolating one production or rule of the [PROV-N Recommendation](https://www.w3.org/TR/prov-n/). `expected.tsv` gives the result the grammar requires for each text under two profiles. A reader passes when it accepts or rejects every probe as the row says.

`tools/gen_probes.py` writes the `.provn` files. The files are stored byte for byte (`.gitattributes` turns off line-ending conversion), because some probes test a bare CR, CRLF, a byte-order mark, NUL or a non-breaking space.

## Profiles

| Profile | Meaning |
|---|---|
| `strict` | The whole grammar of the Recommendation, plus the MUST statements in its prose. |
| `default` | `strict` plus these extensions, which PROV-N writers in the wild produce: bare `mentionOf`, `-` in a required argument of a relation (not as the identifier of an entity, activity, agent or bundle, nor as either party of `hadMember`, `alternateOf` or `specializationOf`, nor as either entity of `mentionOf`), a `default` declaration after a `prefix`, expressions after bundles, an identifier on `mentionOf`, an identifier or attributes on `alternateOf`, `specializationOf` and `hadMember`, and `prefix prov` or `prefix xsd` bound to their own IRIs. |

Everything else is the same under both profiles.

## Columns of `expected.tsv`

The file has a header row and one row per probe, sorted by name. Columns are tab-separated.

| Column | Content |
|---|---|
| `name` | The probe. The text is in `<name>.provn`. |
| `strict` | `accept` or `reject`. |
| `default` | `accept` or `reject`. |
| `rule` | What decides the row: a production number such as `[53]`, a section such as `3.7.4`, or a terminal the grammar leaves to another specification: `IRI_REF` and `LANGTAG` are SPARQL 1.0's, `DATETIME` is `xsd:dateTime` of XSD 1.1 (section 3.7.3.2), and `WS` is SPARQL 1.0's white space (space, tab, CR, LF), which the Recommendation uses without naming it. A rule ending in `decision` marks a row the Recommendation does not decide (see below). |
| `provpy` | The number of the [prov](https://github.com/trungdong/prov) issue that reports a difference, when ProvPy 3.3.0 accepts or rejects the probe differently from the row under at least one profile. Empty when it gives the same accept or reject result under both, and when no issue covers the difference yet. The column compares acceptance only, not the documents read, so a probe that ProvPy reads while it drops a statement with a warning counts as accepted. |

## Rows marked `decision`

A few rows are decided by a choice of the reference implementation, provkit, where the Recommendation does not settle the matter. Some reject text the grammar accepts and some accept text that a MUST in the prose would reject. The `rule` column of each ends in `decision`:

- an attribute named after the formal of the record that holds it, such as `[prov:activity='ex:a']` on `wasGeneratedBy`;
- a value typed `prov:QUALIFIED_NAME` whose text is not a qualified name, or whose local part PROV-N cannot write;
- two bundles with one identifier;
- more than 64 levels of nesting in an extensibility expression;
- a `\u` escape that names a surrogate, which section 6 does not exclude and a Unicode string cannot hold;
- a bare name when no `default` declaration exists, which section 3.7.1 leaves without a namespace;
- a leading byte-order mark, since section 6 requires UTF-8 and says nothing about a byte-order mark;
- names inside an extensibility expression, which the reference ignores whole as section 5 allows, so an undeclared prefix or a bare name with no default namespace is accepted there. These rows accept text that section 3.7.1 would reject;
- an empty namespace IRI in a `prefix` or `default` declaration, which `IRI_REF` admits. These rows reject. An empty namespace IRI comes from an unfilled value, and ProvPy has refused one in its model since 2.0.1 ([prov issue #142](https://github.com/trungdong/prov/issues/142)), so a document that holds one cannot be exchanged with it;
- a `\U` escape for a code point below U+10000, in a string or an IRI. Section 6, the media-type registration, gives `\UXXXXXXXX` "for U+10000 onwards", and the grammar has no production for the escape. These rows accept;
- `-` as either party of `hadMember`, `alternateOf` or `specializationOf`, or as either entity of bare `mentionOf`. These rows reject under both profiles. Productions [24] to [26] decide `strict`, and bare `mentionOf` is no keyword there, so the `decision` covers `default` only, where these positions are the one exception to `-` in a required argument of a relation;
- `-` as either entity of `prov:mentionOf`, which production [49] admits as an extensibility expression. These rows reject under both profiles. `-` as its bundle rejects under `strict` and accepts under `default`, as bare `mentionOf` without a bundle does.

A reader that differs from the reference on these rows still follows the grammar's productions.

## Semantic rules of section 3.7.5

Table 2 of the Recommendation lists statements such as `wasGeneratedBy(ex:e)` and `wasAssociatedWith(ex:a)` as syntactically correct but unacceptable under PROV-DM, because at least one optional argument must be present. The probes `gen_arity_1` and `association_1` accept them. The table describes a rule of the data model, which a syntax reader does not check.

## Integer literals

An integer literal is `accept` or `reject` by its digits alone. The probes do not test which datatype a reader gives it.

## Stability

The stability rule of the repository applies: a probe is not renamed or edited after a tag. A correction is a new probe and a new tag.
