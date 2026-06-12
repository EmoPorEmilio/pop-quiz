# pop-quiz

## Why
I kept noticing I couldn't thoroughly explain everything about the architecture I was myself trying to steer, the colossal stack I was
piling on, or sometimes couldn't even be 100% sure the LLM didn't screw up the task I assigned it to (or if I even explained it unambiguously). 

Whether you build recklessly with no pants on ("vibecode") or build obsessively to the detail, chances are you still have tons of learning to do about your project or its underlying tech. 

What often fixed this is for me is a more experienced colleague, a tech lead or a professor who put me on the spot with an unexpected but related question. 
Just grasping to answer it while feeling the pressure leaves a physiological imprint that helps you learn it better for the next time. 

(I personally always find it best to try to balance answering succintly while maximizing technical correctness, Richard Feynman style, if you are up for an extra challenge) 

pop-quiz is an attempt to replicate that experience in Claude Code. 

## How

As you make progress and get features done alongside Claude, you'll be surprised on a random configurable cadence by a question. 
After your answer (no cheating!) you'll get the response: Respond poorly, you get the basics. If you almost had it, you get the piece you were
missing. If there's nothing to correct you about, get challenged with extra. 

I tried to write the skill as simple as possible:

- The `/pop-quiz` skill picks one topic (your recent commits, the architecture,
  or a concept underneath the code), asks one open question, and grades by
  teaching. Ideally gets you links for your reading homework.
- A Stop hook provides the surprise. Roughly 1 in 5 times Claude finishes a
  task, at most once every 30 minutes, only inside git repos, and only in
  sessions that actually edited files, you get ambushed — usually about the
  thing that was just built, while it's still fresh enough to lose.

Your record is a markdown table in `.pop-quiz.md` at the root of whatever
project you got quizzed in. 
The skill creates it, shows you every row it writes,
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

## Tuning the ambush

The hook reads three environment variables:

| variable | default | effect |
|----------|---------|--------|
| `POP_QUIZ_ODDS` | `5` | fires 1 in N times Claude stops |
| `POP_QUIZ_COOLDOWN` | `1800` | minimum seconds between ambushes |
| `POP_QUIZ_MIN_EDITS` | `3` | only ambush sessions with at least N file edits |
| `POP_QUIZ_OFF` | unset | disables the ambush; `/pop-quiz` still works |

The hook's only state is the mtime of `~/.cache/pop-quiz-last`, which is the
cooldown clock.

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


## Contributing
Ideally, this skill can remain simple, while getting better at doing the task it sets out to do. Any suggestions on that are welcome. 
