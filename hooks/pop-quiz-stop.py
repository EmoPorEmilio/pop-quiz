#!/usr/bin/env python3
"""Stop hook: once in a while, ambush the user with a pop quiz about the project.

Tuning via environment:
  POP_QUIZ_ODDS      fire 1 in N stops (default 5)
  POP_QUIZ_COOLDOWN  minimum seconds between quizzes (default 1800)
  POP_QUIZ_OFF       set to anything to disable the ambush
"""

import json
import os
import random
import subprocess
import sys
import time

ODDS = int(os.environ.get("POP_QUIZ_ODDS", 5))
COOLDOWN = int(os.environ.get("POP_QUIZ_COOLDOWN", 1800))
STAMP = os.path.expanduser("~/.cache/pop-quiz-last")

REASON = (
    "Pop-quiz hook fired — a ritual the user set up on purpose. Use the Skill "
    "tool to invoke the 'pop-quiz' skill, ask the user exactly ONE question "
    "about this project per that skill's instructions, then end your turn and "
    "wait for their answer. Exception: if the session is clearly mid-incident "
    "or the user is in a hurry, skip with the single line 'Dodged the pop "
    "quiz.' and stop."
)


def in_git_repo() -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True
    )
    return result.returncode == 0


def cooled_down() -> bool:
    try:
        return time.time() - os.path.getmtime(STAMP) >= COOLDOWN
    except OSError:
        return True


def should_fire(event: dict) -> bool:
    return (
        not event.get("stop_hook_active")  # we caused this stop; never re-fire
        and not os.environ.get("POP_QUIZ_OFF")
        and in_git_repo()
        and cooled_down()
        and random.randrange(ODDS) == 0
    )


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}

    if not should_fire(event):
        return

    os.makedirs(os.path.dirname(STAMP), exist_ok=True)
    with open(STAMP, "w"):
        pass  # the stamp's mtime is the cooldown clock

    print(json.dumps({"decision": "block", "reason": REASON}))


if __name__ == "__main__":
    main()
