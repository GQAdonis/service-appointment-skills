# Report-back template

Bottom line first. Short. Quote, don't paraphrase, the confirmation.

```
Done. {ONE-LINE OUTCOME — e.g., "The note is on the dispatch ticket for tomorrow's appointment."}

Confirmed by {human agent | AI assistant (unverified)} at {TIME}:
  "{EXACT CONFIRMATION SENTENCE}"
  Read-back: {verbatim | by reference to first message | not provided}

Appointment: {DAY}, {DATE}, {WINDOW} · contact {PHONE} · order/ticket {NUMBER} · {SERVICE LINE}

Declined / not done:
  - {ITEM — e.g., "Agent asked for an email to send an app guide; declined, not needed for the task."}

Next steps:
  - Expect the provider's post-chat {SMS | email} summary; it's your written record.
  - When the "tech is on the way" text arrives, reply with the key detail once more.
  - {Anything the user must do — sign in, be present, unlock gate}

Chat pane left open in your tab.
```

## Human-in-the-loop question format

When pausing for a decision, use this shape (as `AskUserQuestion` when available):

```
The agent said: "{EXACT WORDING}"
Options:
  1. {OPTION A}
  2. {OPTION B}
  3. Hold / switch to phone
Recommendation: {ONE LINE, or "none — your call"}
```
