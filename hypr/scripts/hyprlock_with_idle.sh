#!/bin/bash

# Run hyprlock
hyprlock &

# Only run hypridle if not already running
if ! pgrep -x hypridle > /dev/null; then
    hypridle &
fi

