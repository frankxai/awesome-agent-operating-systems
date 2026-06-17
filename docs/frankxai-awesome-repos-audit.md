# FrankX Awesome Repositories Visual Audit

Audit date: 2026-06-17

This inventory tracks the local `awesome-*` repositories and the GitHub README quality upgrades needed to make the FrankX curation layer feel consistent and premium.

## Current State

| Repo | Hero | Versioned assets | Workflow | Contributing | License | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| `awesome-agent-operating-systems` | Yes | Yes | Yes | Yes | Yes | Keep as reference pattern |
| `awesome-hermes-agents` | No | No | Yes | Yes | Yes | High |
| `awesome-cosmos-ai-agents` | No | No | No | No | No | High |
| `awesome-design-agent-skills` | No | No | No | Yes | No | High |
| `awesome-ai-coe` | Partial external/inline visual | No | No | No | No | Medium |
| `awesome-agentic-income` | Partial external/inline visual | No | No | Yes | Yes | Medium |

## World-Class README Rubric

Every public awesome repo should have:

- Full-width versioned `assets/hero.svg`
- Centered title, subtitle, and quick navigation row
- Badges for validation, license, and category
- "Top picks by job" or "start here" matrix
- Category table of contents
- Inclusion policy
- Contribution guide
- License
- Link validation workflow
- Clear provenance and non-affiliation wording

## Suggested Upgrade Order

1. `awesome-hermes-agents` - already important and active; add hero and quick nav without changing its Hermes-specific scope.
2. `awesome-cosmos-ai-agents` - needs the full open-source hygiene pack: hero, license, contribution guide, validation.
3. `awesome-design-agent-skills` - visually important because design repos are judged fast; add hero, license, validation.
4. `awesome-ai-coe` - add license/contributing/workflow and replace any fragile external visual dependency with versioned assets.
5. `awesome-agentic-income` - preserve current content, add versioned assets and validation workflow.

## Reference Pattern

Use `awesome-agent-operating-systems` as the template:

- `assets/hero.svg`
- README with centered hero/title/nav
- `docs/inclusion-policy.md`
- `docs/landscape-map.md`
- `CONTRIBUTING.md`
- `.github/workflows/validate.yml`
- `scripts/validate-links.ps1`

## Design Direction

Keep a shared family resemblance across FrankX awesome repos:

- Dark graphite background
- Teal, green, and blue highlights
- Systems-map or constellation composition
- Minimal readable title text only
- No vendor logos unless there is permission and a reason
- No stock imagery
