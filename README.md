# pop-quiz

You build with an LLM, and the LLM ends up knowing your project better than you do —
the architecture, the stack, the features, the details. pop-quiz is the tech lead who
suddenly swivels around and asks you one question about it. Whatever you answer, the
response teaches you one notch above the level your answer revealed: know nothing and
you get the basics; know a bit and you get pushed deeper.

It's a Claude Code plugin with two pieces and zero infrastructure — it runs inside
the session you're already in:

- **`skills/pop-quiz/`** — the `/pop-quiz` skill. Picks one topic from three angles
  (your recent commits, your architecture, or a concept underneath your code), asks
  one open question, grades by teaching — citing your real code, and official
  reference docs for concepts — then shows you the level it recorded.
- **`hooks/`** — a Stop hook that puts the *pop* back in pop quiz: when Claude
  finishes a task, roughly 1 time in 5 (at most once per 30 minutes, only inside
  git repos) it ambushes you with a quiz before the session rests.

Your progress lives in `.pop-quiz.md` at the root of each quizzed project — a plain
markdown table the skill creates, appends to, shows you after every round, and
compacts when it grows long. Future quizzes read it to escalate topics you know and
revisit ones you don't. Delete it to reset; commit it to version your learning
record; gitignore it to keep it private.

## Install

```
/plugin marketplace add emoporemilio/pop-quiz
/plugin install pop-quiz@pop-quiz
```

That's the whole setup — the skill and the hook registration ship with the plugin.

**Updates:** the plugin is versioned by git commit SHA, so every push to this repo is
a new version. `/plugin marketplace update` pulls the latest; marketplaces with
auto-update enabled refresh on startup.

## Developing / running from a checkout

A symlink install reads straight from the working tree (skill body and hook script
are read per use, so edits take effect immediately, no reinstall):

```sh
ln -sfn "$(pwd)/skills/pop-quiz" ~/.claude/skills/pop-quiz
```

and register the hook in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "/absolute/path/to/pop-quiz/hooks/pop-quiz-stop.py" }
        ]
      }
    ]
  }
}
```

## Tuning the ambush

The hook reads three environment variables:

| variable | default | effect |
|----------|---------|--------|
| `POP_QUIZ_ODDS` | `5` | fires 1 in N times Claude stops |
| `POP_QUIZ_COOLDOWN` | `1800` | minimum seconds between ambushes |
| `POP_QUIZ_OFF` | unset | set to anything to disable the ambush (manual `/pop-quiz` still works) |

The cooldown clock is the mtime of `~/.cache/pop-quiz-last` — the hook's only state.
