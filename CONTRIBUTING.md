# Contributing

Contributions should improve an architecture or adoption decision, not simply add links.

## Ground rules

1. **Primary sources first.** Verify repository metadata, documentation, license and current architecture.
2. **10k-star default.** Add lower-star projects only as justified `strategic-exception` entries.
3. **License honesty.** Public source is not automatically open source. Flag unresolved or custom licenses.
4. **One operational reason.** Explain the need the project addresses and why it changes the shortlist.
5. **No install claims without execution.** Do not report a tool as working unless it was actually exercised and evidence is linked.
6. **Human gates.** Money, production, credentials, public sends, legal/IP and destructive actions require explicit controls.
7. **High signal.** Prefer a smaller, differentiated catalog over a dump of similar wrappers.

## Workflow

1. Edit `data/catalog-seed.json`.
2. Refresh and regenerate:

   ```bash
   python scripts/refresh_catalog.py
   python scripts/build_knowledge_graph.py
   python scripts/render_catalog.py
   python scripts/validate_repository.py
   ```

3. Review generated metadata, especially `licenseReviewRequired`, archived state and unexpected threshold failures.
4. Update the needs map or a focused assessment if the recommendation changes.
5. Open a focused pull request explaining the evidence and decision impact.

See [Inclusion Policy](docs/inclusion-policy.md) for the complete admission and removal rules.