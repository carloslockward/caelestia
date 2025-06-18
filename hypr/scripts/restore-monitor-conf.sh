#!/bin/bash

config_file="$HOME/.config/hypr/monitors.conf"

if [ "$(wc -l < "$config_file")" -gt 1 ]; then
  while IFS= read -r line; do
    hyprctl keyword monitor "$line"
  done < "$config_file"
fi
