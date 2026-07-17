# Xuerong feature map

## Theme behavior

- Full-body states: idle, yawning, dozing, collapsing, thinking, working, error, attention, notification, carrying, sleeping, and waking.
- Reactions: drag, left click, right click, annoyed, and double click.
- Edge states: mini-idle, mini-alert, mini-happy, mini-enter, mini-peek, mini-working, mini-crabwalk, mini-enter-sleep, and mini-sleep.
- Edge images are mirrored according to the physical screen side so Xuerong's face remains visible.

## Runtime behavior

- Edge dragging detaches immediately into free X/Y movement.
- Drag release chooses left edge, right edge, or normal mode from the final cursor position.
- The outer-edge clamp is derived from visible content margins and permits 50% of visible horizontal content to cross the display edge.
- Internal multi-monitor seams remain clipped to prevent the hidden half from appearing on the neighboring display.

## Codex integration

- Codex JSONL monitoring exposes current working state, title, model, provider, context usage, and assistant output.
- Structured `request_user_input` calls remain visible in the Session HUD until their matching output arrives.
- HUD choice buttons copy the selected label and open Codex. They do not forge or directly submit a tool response.
- Codex CLI sessions prefer their source terminal; Codex Desktop sessions use the Windows packaged-app activation fallback.

