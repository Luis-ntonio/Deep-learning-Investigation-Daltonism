import argparse
import random
from PIL import Image, ImageDraw
import math
import os



# Function to generate random circles
def draw_random_circle(draw_obj, x, y, radius, color):
    draw_obj.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color)

# Function to check if the new circle collides with any existing circles
def is_colliding(x, y, radius, existing_circles):
    for cx, cy, cr in existing_circles:
        distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        if distance - 2 < radius + cr:  # If distance is less than the sum of radii, they collide
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Generate images with random circles.")
    parser.add_argument("--option", type=str, required=True, help="Option to specify the behavior of the script.")
    args = parser.parse_args()
    option = args.option

    # Directories for input and output
    input_image_path = "data"  # Input folder containing number images
    output_image_path = f"./dataset/circle_images_{option}"  # Output folder to save the results

    # Ensure the output directory exists
    if not os.path.exists(output_image_path):
        os.makedirs(output_image_path)

    # Image size (assuming all input images are the same size)
    image_size = 1920  # Larger size for better detail

    # Process each image in the input directory
    for filename in os.listdir(input_image_path):
        if filename.endswith(".png"):  # Process only PNG images
            input_file = os.path.join(input_image_path, filename)
            output_file = os.path.join(output_image_path, f"circles_{filename}")

            # Load the number image and resize to fit within the circle
            number_img = Image.open(input_file).convert("L")  # Convert to grayscale
            number_img = number_img.resize((image_size, image_size))

            # Create a mask for where the number is (anything not white)
            number_mask = number_img.point(lambda p: p < 200 and 255)  # Adjust threshold to catch the number

            # Create a new image with a white background
            output_img = Image.new("RGB", (image_size, image_size), "white")
            draw = ImageDraw.Draw(output_img)

            # List to store the existing circles' positions and radii to prevent collisions
            circles = []

            # Generate random circles across the entire image
            for _ in range(100000):  # Number of circles to be generated
                # Randomize the circle's position and size
                r = random.randint(3, 30)  # Random radius between 3 and 30
                x = random.randint(r, image_size - r)
                y = random.randint(r, image_size - r)

                # Check if the new circle collides with any existing circles
                if is_colliding(x, y, r, circles):
                    continue  # Skip this circle if it collides

                # Check if any part of the circle is within the number by sampling the circle's area
                touching_number = False
                for dx in range(-r, r + 1, r // 2):  # Check at multiple points in the circle
                    for dy in range(-r, r + 1, r // 2):
                        if 0 <= x + dx < image_size and 0 <= y + dy < image_size:  # Check within bounds
                            if number_mask.getpixel((x + dx, y + dy)) == 255:  # Pixel belongs to number
                                touching_number = True
                                break
                    if touching_number:
                        break

                # Choose a random color based on overlap with the number
                if touching_number:
                    if option == "p":
                        color = (random.randint(150,255), random.randint(0,100), random.randint(0,100))  # Random Protanopia number
                    if option == "d":
                        color = (random.randint(0,150), random.randint(100,255), random.randint(0,150))  # Random Deuteranopia number
                    if option == "t":
                        color = (random.randint(150,255), random.randint(150,255), random.randint(0,100))  # Random Tritanopia number
                else:
                    if option == "p":
                        color = (random.randint(0,150), random.randint(100,255), random.randint(0,150))
                    if option == "d":
                        color = (random.randint(150,255), random.randint(0,100), random.randint(0,100))
                    if option == "t":
                        color = (random.randint(0,100), random.randint(0,150), random.randint(150,255))

                # Draw the circle
                draw_random_circle(draw, x, y, r, color)

                # Store the circle's position and radius to check for future collisions
                circles.append((x, y, r))

            # Save the final image to the output folder
            output_img.save(output_file)
            print(f"Image saved as {output_file}")


if __name__ == "__main__":
    main()