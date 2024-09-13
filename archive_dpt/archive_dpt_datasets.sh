#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Input CSV file
CSV_FILE="datasets-to-archive.csv"

# Extract 'name' column (assuming first row is header)
while IFS=, read -r name other_columns; do
  # Skip the header
  if [[ "$name" != "name" ]]; then
    # Run the hdx-toolkit command with the name
    hdx-toolkit update --dataset_filter="$name" --hdx_site=prod --key=archived --value=True
  fi
done < <(tail -n +2 "$CSV_FILE") # Skip header row in the CSV
