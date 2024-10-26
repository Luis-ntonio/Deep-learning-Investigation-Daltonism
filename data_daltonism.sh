#!/bin/bash

# Create the output directory if it doesn't exist
mkdir -p Daltonism

# Define the types of daltonism
types=("d" "p" "t")

# Loop through all images in the circle_images folder
for input_image in circle_images/*; do
    # Extract the base name of the image
    base_name=$(basename "$input_image")
    
    # Loop through each type of daltonism
    for type in "${types[@]}"; do
        # Define the output image path with the type identifier
        output_image="Daltonism/${base_name%.*}_$type.${base_name##*.}"
        # Execute the daltonize command with specified parameters
        daltonize -d -t="$type" -g=1.5 "$input_image" "$output_image"
    done
done