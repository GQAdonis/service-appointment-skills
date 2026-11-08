# Browser tactics for provider chat widgets

Written for Claude in Chrome's `computer` / `browser_batch` / `find` tools; the patterns transfer to any screenshot-and-click browser automation.

## Work in the user's tab

- The user usually opens the side panel on the provider's support or account page. Work there; don't open a new tab unless the page holds unsaved input.
- Before anything else, `find` for: "manage appointment", "reschedule", "cancel", "chat", "sign in". Capture the appointment card (date, window, contact, order #).
- A visible **Sign in** button means the session is unauthenticated even if an appointment card is showing (cards can render from an order cookie). Unauthenticated chat won't reach a human. Hand sign-in to the user.

## The chat pane

- Provider chat is almost always a fixed right-side pane, ~270 px wide at 1533 px viewport width. Zoom region ≈ `[viewport_w − 270, 40, viewport_w, viewport_h]`.
- For polling, zoom only the bottom ~180 px of the pane (`[x0, viewport_h − 190, viewport_w, viewport_h]`) — the latest message and the input box.
- Click the input box before typing. Press Return to send. Confirm your bubble rendered before waiting.
- Chips/buttons ("Chat with an agent", "Yes") are clickable; typing the same text usually also works.

## Batching

- `browser_batch`: click input → type → key Return → wait → zoom. One round trip per message.
- Keep total waits in a batch under ~100 s; the tool call times out at 120 s.
- Polling cadence while queued: 2–3 × `wait 10` + 1 zoom. Never longer than 30 s between looks near an expected agent join.

## Coordinate mapping from a zoomed image

When you read a button position from a `zoom` capture of region `(x0, y0, x1, y1)` rendered at `zoom_w × zoom_h`:

```
scale_x = zoom_w / (x1 − x0)
scale_y = zoom_h / (y1 − y0)
page_x  = x0 + zoomed_x / scale_x
page_y  = y0 + zoomed_y / scale_y
```

Example: region (1265, 600, 1533, 784) → 395 × 271 px zoom; the "Yes" chip at zoomed (163, 176) maps to page (1376, 719).

## Window resizes

The viewport can change size between messages (e.g., 1247×909 → 1533×784 when the user resizes). Re-screenshot after any user interaction before clicking.

## Reading long transcripts

Scroll inside the pane (`scroll` at a point within it), not the page. Zoom the full pane height at scale ≤ 0.8 to read; the page behind it is irrelevant.

## Don't

- Click links the agent/AI pastes without surfacing them to the user.
- Upload screenshots or files to the chat unless the user asked.
- Dismiss the chat pane when done — leave it for the user.
