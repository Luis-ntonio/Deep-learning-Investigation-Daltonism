#!/bin/bash

# Define the options
options=("p" "d" "t")

# Loop through each option and call data_formatted.py
for option in "${options[@]}"; do
    python data_formatted.py --option "$option"
done