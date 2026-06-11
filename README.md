# pop-quiz

You build with an LLM, and the LLM ends up knowing your project better than you do —
the architecture, the stack, the features, the details. pop-quiz is the tech lead who
suddenly swivels around and asks you one question about it. Whatever you answer, the
response teaches you one notch above the level your answer revealed: know nothing and
you get the basics; know a bit and you get pushed deeper.

Two pieces, zero infrastructure — it runs inside the Claude Code session you're
already in:

- **`skill/SKILL.md`** — the `/pop-quiz` skill. It picks one topic from three angles
  (your recent commits, your architecture, or a concept underneath your code), asks
  one open question, grades by teaching, and appends a row to `.pop-quiz.md` in the
  project so future quizzes escalate known topics and revisit weak ones.
- **`hooks/pop-quiz-stop.sh`** — a Stop hook that puts the *pop* back in pop quiz:
  when Claude finishes a task, roughly 1 time in 5 (at most once per 30 minutes,
  only inside git repos) it ambushes you with a quiz before the session rests.

## Install

Link the skill into your personal skills directory:

```sh
ln -sfn ~/projects/pop-quiz/skill ~/.claude/skills/pop-quiz
```

Register the hook in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "~/projects/pop-quiz/hooks/pop-quiz-stop.sh" }
        ]
      }
    ]
  }
}
```

## Tuning

The hook reads three environment variables:

| variable | default | effect |
|----------|---------|--------|
| `POP_QUIZ_ODDS` | `5` | fires 1 in N times Claude stops |
| `POP_QUIZ_COOLDOWN` | `1800` | minimum seconds between ambushes |
| `POP_QUIZ_OFF` | unset | set to anything to disable the ambush (manual `/pop-quiz` still works) |

The per-project ledger lives at `.pop-quiz.md` in each repo's root — plain markdown,
readable and editable by hand. Delete it to reset your history; commit it if you want
your learning record versioned.
