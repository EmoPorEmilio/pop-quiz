#!/usr/bin/env python3
"""Stop hook: once in a while, ambush the user with a pop quiz about the project.

Tuning via environment:
  POP_QUIZ_ODDS       fire 1 in N stops (default 5)
  POP_QUIZ_COOLDOWN   minimum seconds between quizzes (default 1800)
  POP_QUIZ_MIN_EDITS  only ambush sessions with at least N file edits (default 3)
  POP_QUIZ_OFF        set to anything to disable the ambush
"""

import json
import os
import random
import subprocess
import sys
import time

ODDS = int(os.environ.get("POP_QUIZ_ODDS", 5))
COOLDOWN = int(os.environ.get("POP_QUIZ_COOLDOWN", 1800))
MIN_EDITS = int(os.environ.get("POP_QUIZ_MIN_EDITS", 3))
STAMP = os.path.expanduser("~/.cache/pop-quiz-last")

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}

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


def wrote_code(transcript_path) -> bool:
    """A session that edited no files has nothing fresh to quiz on.

    If the transcript is missing or unreadable, fall back to the old
    always-eligible behavior rather than silently killing the ambush.
    """
    if not transcript_path:
        return True
    edits = 0
    try:
        with open(transcript_path) as transcript:
            for line in transcript:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                message = entry.get("message")
                content = message.get("content") if isinstance(message, dict) else None
                if not isinstance(content, list):
                    continue
                for block in content:
                    if (
                        isinstance(block, dict)
                        and block.get("type") == "tool_use"
                        and block.get("name") in EDIT_TOOLS
                    ):
                        edits += 1
                        if edits >= MIN_EDITS:
                            return True
    except OSError:
        return True
    return False


def should_fire(event: dict) -> bool:
    return (
        not event.get("stop_hook_active")  # we caused this stop; never re-fire
        and not os.environ.get("POP_QUIZ_OFF")
        and in_git_repo()
        and cooled_down()
        and random.randrange(ODDS) == 0
        and wrote_code(event.get("transcript_path"))  # last: it reads a file
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
