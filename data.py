from PIL import Image, ImageDraw, ImageFont
import os

# Create a directory to save the images
output_dir = "data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set the size of the images (squared)
image_size = (1920, 1920)
font_size = 1700

# Create images for numbers from 1 to 1000
for i in range(1, 1001):
    # Create a blank white image
    img = Image.new('RGB', image_size, color='white')
    
    # Initialize ImageDraw to add text
    d = ImageDraw.Draw(img)
    
    # Use a basic font (Pillow default)
    try:
        font = ImageFont.truetype("arial.ttf", font_size - 300*(len(str(i)) - 1))  # Try using a system font
    except IOError:
        font = ImageFont.load_default()  # Fall back to default font if system font is not available
    
    # Get the bounding box of the text to center it
    text = str(i)
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Font metrics for better vertical centering
    ascent, descent = font.getmetrics()
    
    # Calculate the vertical position adjustment based on ascent and descent
    total_text_height = ascent + descent
    position = ((image_size[0] - text_width) // 2, (image_size[1] - total_text_height) // 2)
    
    # Add the number to the image
    d.text(position, text, fill="black", font=font)
    
    # Save the image
    img.save(os.path.join(output_dir, f'{i}.png'))

print(f"Images generated in the '{output_dir}' directory.")
