#!/bin/bash

# Define an array of mode values
MODES=("default" "default_short" "technical" "stability")

# Loop over each mode value
for MODE in "${MODES[@]}"
do
    # Run the command with the current mode
    python nethack_tileset/Data_Gathering/get_gpt4_descriptions.py --input_csv tileset_vanilla_titles.csv --output_csv tileset_gpt4_"$MODE".csv --mode "$MODE"
done

