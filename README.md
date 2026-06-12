# pop-quiz

When you build with an LLM, the LLM ends up knowing your project better than you
do. I kept noticing I couldn't explain my own architecture, the stack I was
standing on, half the features I'd shipped. In real life the thing that fixes
this is a tech lead or a professor who puts you on the spot: one question you
didn't expect, and answering it (well or badly) is how you actually learn.

pop-quiz is that, inside Claude Code. One question about your own project, then a
reply that teaches one notch above whatever your answer revealed. If you knew
nothing, you get the basics. If you almost had it, you get the piece you were
missing, pointed at the actual file and line.

## How it works

Two pieces, no infrastructure:

- The `/pop-quiz` skill picks one topic (your recent commits, the architecture,
  or a concept underneath the code), asks one open question, and grades by
  teaching. Concepts come with a link to the official reference docs, not
  someone's blog.
- A Stop hook provides the surprise. Roughly 1 in 5 times Claude finishes a
  task, at most once every 30 minutes and only inside git repos, you get
  ambushed.

Your record is a markdown table in `.pop-quiz.md` at the root of whatever
project you got quizzed in. The skill creates it, shows you every row it writes,
and compacts it when it grows long. Later quizzes read it to escalate the topics
you know and come back to the ones you don't. Delete it to start over; commit or
gitignore it as you like.

## Install

```
/plugin marketplace add EmoPorEmilio/pop-quiz
/plugin install pop-quiz@pop-quiz
```

The surprise hook needs `python3` on PATH (any 3.x, stdlib only). On native
Windows without Git Bash the ambush won't fire; `/pop-quiz` itself works
everywhere.

There are no versioned releases. The plugin is versioned by commit SHA, so every
push here is a new version: `/plugin marketplace update pop-quiz` pulls the
latest, and with auto-update on it refreshes at startup.

## Running from a checkout

A symlink install reads straight from the working tree, so edits to the skill or
the hook take effect immediately:

```sh
ln -sfn "$(pwd)/skills/pop-quiz" ~/.claude/skills/pop-quiz
```

Then register the hook in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python3 /absolute/path/to/pop-quiz/hooks/pop-quiz-stop.py" }
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
| `POP_QUIZ_OFF` | unset | disables the ambush; `/pop-quiz` still works |

The hook's only state is the mtime of `~/.cache/pop-quiz-last`, which is the
cooldown clock.
