---
name: xuerong-animation-studio
description: Create, redesign, retime, smooth, repair, validate, visually review, integrate, or package Xuerong animated WebP assets for Clawd on Desk. Use whenever a task changes a Xuerong full-body, reaction, sleep-chain, working, transition, or mini-edge animation and must preserve approved identity, timing, transparency, direction, scale, seams, and release safety through coordinated specialist agents.
---

# Xuerong Animation Studio

Coordinate Xuerong animation work as a gated production line. Keep the Root Agent responsible for the job contract, file ownership, approval state, integration, and final verification.

## Load the standards

Read these references before changing an animation:

1. `references/animation-standard.md` for every job.
2. `references/state-recipes.md` for state-specific motion and transition rules.
3. `references/agent-handoffs.md` before delegating or integrating work.

Also read the repository `AGENTS.md`, `docs/project/theme-state-ui.md`, `docs/guides/state-mapping.md`, and the active `themes/xuerong-hd/theme.json` entries involved in the request.

## Run the workflow

### 1. Freeze the baseline

- Inspect `git status` without changing the user's unrelated work.
- Name the approved reference asset and version before generating anything.
- Use `idle.webp` as the normal-mode identity and apparent-scale anchor.
- Use `mini-idle.webp` as the mini-edge identity and apparent-scale anchor.
- For retiming or smoothing, preserve the approved source WebP as the motion reference.
- Create a unique candidate directory under `build/xuerong-animation-runs/<run-id>/`; never generate directly into `themes/xuerong-hd/assets/`.

### 2. Define one job contract

Record the animation slot, mode, screen side, source and target states, loop behavior, target 24 or 30 FPS, duration, anchors, baseline assets, 5% scale tolerance, GPU need, and acceptance checks. Use the contract in `references/agent-handoffs.md`.

Discuss a new motion's emotional beats and timing with the user before implementation. For a confirmed repair, reuse the stated behavior and change only the failing segment.

### 3. Assign one writer per artifact

- Give one coherent motion or transition chain to `xuerong_animation_builder`.
- Give numeric and structural QA to `xuerong_deterministic_qa` only after a candidate exists.
- Give independent visual comparison to `xuerong_visual_quality_reviewer` only after deterministic QA passes.
- Give formal asset replacement and packaging to `xuerong_release_integrator` only after explicit user approval.

Do not split one continuous action, especially the sleep chain, across unrelated builders. Do not let two agents write the same WebP, manifest, theme entry, or report.

### 4. Build candidates

- Preserve original duration unless the user explicitly changes pacing.
- Output stable 24 or 30 FPS; never choose an arbitrary frame rate.
- Keep character identity, hair and outfit colors, proportions, baseline, and motion direction stable.
- Use natural acceleration and deceleration. Remove duplicate frames, jumps, ghosting, white membrane, jelly motion, warping, and facial or hand drift.
- Detect cuts or discontinuous poses and do not interpolate across them.
- Keep local GPU generation serialized. CPU inspection and documentation may run in parallel when they do not read a half-written candidate.

### 5. Run deterministic QA

Load the bundled workspace Python before running repository Python scripts.

For a v2.1.3-derived smoothing job, run:

```text
python scripts/validate-xuerong-v213-smooth.py --reference-theme <reference> --candidate-theme <candidate> --output-dir <run>/qa
```

Create checker, dark, and magenta contact sheets with `scripts/qa-xuerong-smooth.py`. Run `node scripts/validate-theme.js themes/xuerong-hd` after integration. Run `npm test` when state mapping, timing configuration, mini behavior, or runtime code changes.

Treat a validator PASS as necessary, not sufficient. Report exact commands, exit codes, failed frames, warnings, and artifact paths.

### 6. Run independent visual QA

Review the complete animation, not only a contact sheet. Compare it against the named baseline on transparent, checker, dark, and magenta backgrounds. Inspect the transition before and after the asset, loop seam, first and last frame, screen direction, face and hands, color, scale, edge visibility, and perceived pace.

Reject vague judgments such as “looks good.” Return PASS or FAIL for every hard gate and identify the smallest failing frame range.

### 7. Ask for user acceptance

Show a complete preview and summarize only observable changes. Do not integrate, install, commit, tag, package, or push merely because agents passed QA.

If the user rejects the candidate, regenerate only the smallest failing motion segment and repeat both QA stages.

### 8. Integrate safely

After explicit approval, preserve the current formal asset, copy only approved candidates, update the smallest necessary `theme.json` or timing entries, and rerun fresh validation. Commit, install, package, tag, release, or push only when the user explicitly requests that action.

## Parallelism rules

Parallelize independent animations only when their contracts and output paths are disjoint. Keep at most one local GPU animation job active. A safe four-slot arrangement is Root Agent + one builder + deterministic QA for a completed different candidate + one read-only reviewer. Never run multiple interpolation or image-generation jobs against the same local GPU.

## Completion gate

Do not call the job complete until all are true:

- the candidate matches the requested state behavior;
- duration and 24/30 FPS contract pass;
- apparent character scale and baseline remain within the 5% contract;
- identity, hair, outfit, and palette match the approved baseline;
- transparency has no white membrane, detached fragments, or opaque background;
- motion has no duplicate-frame stall, jump, ghosting, jelly, warp, or direction reversal;
- loop or transition endpoints connect correctly;
- deterministic and visual QA reports exist;
- the user approved the preview;
- fresh post-integration validation passed.
