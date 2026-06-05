# PR Title
<!-- Brief, imperative title describing the change -->

## Description
Explain **what** changed and **why**:
- What: [brief summary]
- Why: [reason / motivation]
- How: [technical approach if non-obvious]

## Test Plan
Steps to verify this PR works:
- [ ] `python3 -m py_compile src/*.py` passes
- [ ] Run the daemon: `./run.sh` and verify AIS parsing
- [ ] Test Twitter posting (dry run): `python3 -m src.twitter_poster --test`
- [ ] Verify map image generation: check `data/img/` for output

## Checklist
- [ ] Code compiles (`py_compile`)
- [ ] No trailing whitespace or lint errors
- [ ] Tests pass (if applicable)
- [ ] README updated (if public API changed)
