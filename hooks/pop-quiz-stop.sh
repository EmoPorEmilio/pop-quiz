#!/usr/bin/env bash
# Stop hook: once in a while, ambush the user with a pop quiz about the project.
# Tuning via env: POP_QUIZ_ODDS (default 5 -> fires 1 in 5), POP_QUIZ_COOLDOWN
# seconds (default 1800), POP_QUIZ_OFF=1 to disable entirely.

input=$(cat)

# Never re-fire while Claude is already continuing because of this hook.
case "$input" in
  *'"stop_hook_active":true'* | *'"stop_hook_active": true'*) exit 0 ;;
esac

[ -n "$POP_QUIZ_OFF" ] && exit 0

# Only quiz inside real projects.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

odds="${POP_QUIZ_ODDS:-5}"
cooldown="${POP_QUIZ_COOLDOWN:-1800}"
stamp="$HOME/.cache/pop-quiz-last"

now=$(date +%s)
if [ -f "$stamp" ]; then
  last=$(cat "$stamp" 2>/dev/null || echo 0)
  [ $((now - last)) -lt "$cooldown" ] && exit 0
fi

[ $((RANDOM % odds)) -ne 0 ] && exit 0

mkdir -p "$(dirname "$stamp")"
echo "$now" >"$stamp"

cat <<'EOF'
{"decision": "block", "reason": "Pop-quiz hook fired — a ritual the user set up on purpose. Use the Skill tool to invoke the 'pop-quiz' skill, ask the user exactly ONE question about this project per that skill's instructions, then end your turn and wait for their answer. Exception: if the session is clearly mid-incident or the user is in a hurry, skip with the single line 'Dodged the pop quiz.' and stop."}
EOF
exit 0
