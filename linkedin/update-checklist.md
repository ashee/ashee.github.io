# LinkedIn Update Checklist

Use `../pub/linkedin-profile.md` as the copy-ready LinkedIn presentation. It is generated from `../profile.md`.

## Before editing LinkedIn

- [ ] Confirm that all new facts were added to `profile.md` first.
- [ ] Run `bin/gen-profile-artifacts.py` from the repository root.
- [ ] Compare `../pub/linkedin-profile.md` with `../profile.md` for titles, dates, locations, and metrics.
- [ ] Review the Headline and About sections for tone and current career goals.
- [ ] Decide whether LinkedIn's network-notification setting should be enabled or disabled.

## Apply the update

- [ ] Headline
- [ ] Location
- [ ] About
- [ ] Experience entries
- [ ] Education
- [ ] Licenses and certifications
- [ ] Skills and skill ordering, including AI, LLM, RAG, MCP, PostgreSQL, and platform expertise

## Verify after saving

- [ ] Check the public profile on desktop or in a signed-out browser.
- [ ] Confirm that each position is associated with the correct organization page.
- [ ] Confirm that the current role and dates display correctly.
- [ ] Check that bullets and paragraph breaks survived pasting.
- [ ] Confirm that no private contact information was added unintentionally.
- [ ] Record any factual correction in `profile.md`, then rerun `bin/gen-profile-artifacts.py`.

## Manual step

LinkedIn still requires manual review and save after regenerating this copy-ready artifact.
