# Dispatch note / request templates

Fill the placeholders, keep each under ~90 words, show the user, get a yes, then paste as one message.

## Annotate an existing appointment

```
I have a technician appointment {DAY}, {DATE}, {WINDOW} ({NAME}, {PHONE}, order {ORDER_NO}).
Please add a note to the work order: {WHAT_HAPPENED — one concrete sentence}.
The tech will need to {WHAT_TECH_NEEDS — materials / access / expect}.
{ACCESS_CONSTRAINTS — pets, gate, who will be home}.
Please confirm once the note is on the dispatch ticket.
```

Example:

> I have a technician appointment tomorrow, Sun Nov 8, 12–4 p.m. (Travis James, 945-555-0100). Please add a note to the work order: my dog chewed through and severed the line where it runs under the edge of the gate. The tech will need to replace/re-run that section of drop and bring materials to bury or protect it where it crosses under the gate. Please confirm once the note is on the dispatch ticket.

## Request a new appointment

```
I need a technician visit for {SERVICE_LINE} at {SERVICE_ADDRESS_ON_FILE} ({NAME}, {PHONE}).
Problem: {SYMPTOM — concrete, observable}. Started {WHEN}.
Already tried: {STEPS — restart, check cables, etc.}; no change. Not a troubleshooting request.
Available: {APPROVED_WINDOWS — e.g., Tue 11/11 8–12, Wed 11/12 any time}.
Access notes: {PETS / GATE / WHO IS HOME}.
Please schedule and confirm the date, window, and ticket number.
```

## Reschedule

```
I need to move my technician appointment currently set for {OLD_DATE}, {OLD_WINDOW} ({NAME}, {PHONE}, order {ORDER_NO}).
Acceptable windows: {APPROVED_WINDOWS}. Please move it to the earliest of those and confirm the new date and window.
```

If the agent offers slots outside the approved list, stop and ask the user.

## Transfer / escalation lines

- "Chat with an agent"
- "Transfer me to a live agent. I need a note added to an existing technician work order."
- "Not a troubleshooting request. The issue is physical damage already known; I need a dispatch note."
- "Are you a human agent or an automated assistant?"
- "Before you transfer me, what is the case or interaction number?"

## Keep-alive acks

"Understood, I'm here and ready." · "Yes, that's fine." · "Desktop, stable connection — please proceed." · "Sounds good."
