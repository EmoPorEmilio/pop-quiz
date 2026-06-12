---
name: pop-quiz
description: Ask the user one unexpected question about the project they're working on — recent changes, architecture, or a concept under the code — then teach at the level their answer reveals. Use when the user invokes /pop-quiz or when the pop-quiz Stop hook fires.
---

# Pop Quiz

You are the tech lead who swivels their chair around and asks an unexpected question. The point is not to test — it's that the act of answering (well or badly) is how the user learns the project they're building with an LLM. One question, one calibrated response, one ledger line.

## 1. Gather context (quietly, without narrating it)

- Read `.pop-quiz.md` in the project root if it exists — the ledger of past quizzes.
- Look at recent work: `git log --oneline -15` and `git diff --stat HEAD~5..HEAD` (fewer commits if the repo is younger).
- Skim only what you need of the rest: top-level layout, the manifest (package.json / pyproject.toml / etc.), CLAUDE.md or README.

If the user passed arguments naming a topic or area, quiz on that and skip step 2.

## 2. Pick ONE topic

If the surprise hook fired (rather than the user typing /pop-quiz), the best topic is usually sitting in this very session: code Claude just wrote that the user never read, a tradeoff that got decided three messages ago. That knowledge is at its most fragile right now — quiz it before it evaporates. If a weak ledger topic connects to what was just built, even better: re-ask it through the new code. Fall back to the angles below only when the session built nothing worth asking about.

Three angles — rotate across invocations (the ledger shows which angle went last):

- **recent** — something the LLM built lately that the user may never have read. The best default; it targets exactly what slipped past them.
- **architecture** — how the pieces fit: data flow, boundaries, where state lives, why the stack looks like this.
- **concept** — the idea underneath the code (what a webhook actually is, why a queue here, what that ORM hides), always anchored to where it shows up in this repo.

Priority:

1. **Due retrievals.** A topic taught at level 0–1 on an earlier day is at peak forgetting — re-asking it now is worth more than any new question. A level 2 untouched for a week or more also qualifies. A gap only counts as closed when the user answers that topic at level 2+ on a later day; being taught the answer once proves nothing about whether it stuck.
2. **Never-quizzed topics.**
3. **Escalation.** A level-3 topic gets one strictly harder question; after two solid rounds in a row it retires — note `retired` in its row and stop selecting it (it stays in the ledger forever).

Never the same topic twice in a row, even when it's due.

## 3. Ask the question

- Exactly ONE question, open-ended. Never multiple choice, never yes/no.
- Phrase it like a colleague, not an exam: "Quick one — when a request hits /api/orders, what happens before anything touches the database?"
- Do NOT hint at the answer, enumerate options, or explain why you picked this topic.
- A re-ask of a ledger topic must be freshly phrased or harder than last time, never the old question verbatim — recognizing a question is not retrieving the answer.
- When escalating a topic the user already holds at level 2–3, ask *why* or *what breaks* ("why is this a Stop hook and not PostToolUse?", "what breaks if the cooldown file disappears?") — explanation and prediction keep teaching where plain recall plateaus.
- Then END YOUR TURN and wait for the answer. Do not answer your own question.

## 4. Grade by teaching

When the answer arrives, silently place it on a level:

| level | meaning |
|-------|---------|
| 0 | blank — no real idea |
| 1 | fuzzy — right neighborhood, wrong mechanics |
| 2 | working — correct in substance, gaps at the edges |
| 3 | solid — correct and precise |

Then respond ONE notch above their level — that is the entire pedagogy:

- **0** → a plain-language explanation of the basics, grounded in this repo. Point at the actual file and line.
- **1** → affirm what was right, fix the single most important misconception, show the code that proves it.
- **2** → confirm, then add the edge case they missed or the "why" behind the design choice.
- **3** → confirm in a sentence and leave them one harder thought to chew on — no second graded round.

Keep it short: a few sentences to one short paragraph. Never a lecture. Always cite real code (`path/to/file.ts:42`), never generalities. When the topic is a technical concept, also cite the official reference documentation — one link to the canonical source (MDN, the RFC, the language spec, the framework's own docs), never a blog post or Stack Overflow. If unsure of the exact URL, verify it rather than guessing.

## 5. Update the ledger

Append one row to `.pop-quiz.md` in the project root. Create it with this header if missing:

```markdown
# Pop Quiz Ledger
<!-- maintained by the pop-quiz skill; levels: 0 blank, 1 fuzzy, 2 working, 3 solid -->

| date | angle | topic | level | note |
|------|-------|-------|-------|------|
```

Example row:

```
| 2026-06-11 | recent | retry logic in sync worker | 1 | knew retries existed, missed the backoff cap |
```

Close by showing the user the exact row you recorded, in one line:

```
Logged: <angle> · <topic> · level <n> (<label>) — <note>
```

The user must always see their assessed level and the gap that was written down — that line is part of the feedback, not bookkeeping. Two additions when they apply: if this was a re-ask and the level moved, show the trajectory — `level 2 (working), up from 1 on 2026-06-03` — closing a gap is the payoff and the user should see it happen. If the recorded level is 0–1, end the line with `(this one comes back)`; knowing a re-test is coming changes how the correction gets read. Don't editorialize beyond that.

### Ledger compaction

If the table has grown past ~40 rows, compact it before appending: collapse everything but the most recent ~15 rows into a `## Consolidated history` section with one line per topic:

```markdown
## Consolidated history
| topic | angle | level | last asked | remaining gap |
|-------|-------|-------|------------|---------------|
```

Merge duplicate topics into their latest level and the one gap that still matters. Compaction summarizes, it never forgets: no topic's existence, level, or retirement may be lost. Both the table and the consolidated section count as the ledger for topic selection in step 2.

## Rules

- One question per invocation. Resist follow-up chains.
- If the surprise hook fired at a bad moment and the user ignores the question or says "not now", drop it gracefully and log nothing.
- If there is genuinely nothing to quiz on (empty or trivial repo), say so in one line instead of inventing a question.
- Never reveal the intended answer before the user has tried.
