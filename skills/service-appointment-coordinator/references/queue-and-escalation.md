# Queue handling and escalation

This is where runs fail. Observed behaviour from a Saturday-evening ISP chat; treat the numbers as typical, not exact.

## Getting into the queue

1. Bot/AI says it can't do the write → reply with the literal chip text, usually **"Chat with an agent"**, or click the chip.
2. Deflection prompt ("there could be a wait…") → click **Chat with an agent** again.
3. Confirmation looks like "Got it! I'll get you to someone" + "You're in line for an agent" + "Estimated wait time: N minutes".
4. If the bot loops twice without queueing, try "representative" / "agent" / "human". If it still loops, the widget is probably unauthenticated — check for a Sign in button and hand that to the user. Phone is the fallback.

## While waiting

- **Estimates are unreliable.** Observed: 12 → 14 → 12 → 8 → 6 → 6 → 6 (for 15 min) → agent. Second queue: 18 → 19 → 16 → … → 4 (plateau 15+ min) → agent at ~33 min. Report real elapsed time to the user, not the estimate.
- **Poll every 20–30 s.** Use a small zoom of the bottom of the chat pane, not a full screenshot. Batches of 2–3 ten-second waits plus one zoom keep each tool call short and the accept window catchable.
- Tell the user at each estimate change (one line) and offer the phone number in parallel. Keep the queue alive regardless of what they choose.

## The accept prompt — the critical 60 seconds

"An agent is ready for you. Tap or type **Yes** to start the chat. [Yes] [No]"

- **This expires in well under 90 seconds.** A 90-second polling gap missed it; the chat auto-closed with "Thanks for chatting. If you need help later, you can start a new chat anytime." and the queue position was lost.
- Click **Yes** (or type `Yes` + Enter) immediately. Confirm your "Yes" bubble renders before doing anything else.
- If you missed it: send "Chat with an agent" again. You re-queue from zero.

## After Yes

- The human may take **3–6 minutes** to actually join, with no indicator. The pane just shows your messages.
- Send **one** short ping after ~3 min: "Hello — is an agent connected? Just need confirmation the note above is added to tomorrow's work order." Do not resend the full note.
- Join looks like a "Connected to an agent" banner followed by "Thank you for contacting <provider>. May I please have the name, number, and details…?"

## Keeping the session alive

- Agents warn: "Please make sure to chat with us every 2 minutes, otherwise our chat might disconnect." Treat it as real. Keep a one-word ack ready ("Understood", "Yes, that's fine", "Ready").
- Don't answer scripted reminders at length; a short ack and "please proceed" is enough.

## Transfers

- Before accepting a transfer to another department, ask for the case/interaction number.
- After a transfer, re-classify who you're talking to (bot / AI / human) and re-send identity + ask in one message.

## Timeouts and giving up

- No queue indicator and no response for >10 min → ask the user: keep holding, or switch to phone.
- Two consecutive missed accept prompts → recommend phone; chat tooling isn't keeping up.
- Chat auto-closed after the write was confirmed → fine; the confirmation stands. Chat auto-closed before confirmation → the write is unverified; say so.
