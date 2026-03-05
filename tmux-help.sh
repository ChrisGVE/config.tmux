#!/usr/bin/env bash
tmpfile=$(mktemp /tmp/tmux-help-XXXXXX)
python3 ~/.config/tmux/tmux-help.py > "$tmpfile"

content_width=$(awk '{ print length }' "$tmpfile" | sort -n | tail -1)
content_lines=$(wc -l < "$tmpfile" | tr -d ' ')

term_height=$(tmux display-message -p '#{client_height}')
term_width=$(tmux display-message -p '#{client_width}')

padding=6
popup_w=$((content_width + padding))
popup_h=$((content_lines + 4))
max_h=$((term_height - 4))
max_w=$((term_width - 4))
[ "$popup_h" -gt "$max_h" ] && popup_h=$max_h
[ "$popup_w" -gt "$max_w" ] && popup_w=$max_w

tmux display-popup -E -w "$popup_w" -h "$popup_h" "less -S -Ps' ' -Pm' ' -PM' ' $tmpfile; rm -f $tmpfile"
