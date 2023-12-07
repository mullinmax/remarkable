import argparse
from PIL import Image, ImageDraw, ImageFont
import os
import sys

def create_watermark(watermark_size, watermark_text, font_size, h_spacing, v_spacing, color, opacity, font_path):
    # Create a watermark canvas
    watermark = Image.new('RGBA', watermark_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    # Choose a font for the watermark
    if font_path and os.path.exists(font_path):
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # Set text color and opacity
    text_color = (color[0], color[1], color[2], int(255 * opacity))

    # Tile the watermark text across the watermark canvas
    for x in range(0, watermark_size[0], h_spacing):
        for y in range(0, watermark_size[1], v_spacing):
            draw.text((x, y), watermark_text, fill=text_color, font=font)

    # Rotate the watermark
    watermark = watermark.rotate(45, expand=1)

    return watermark

def apply_watermark_to_image(image_path, watermark):
    # Load the original image
    original = Image.open(image_path)

    # Calculate the position to overlay the watermark on the original image
    wx, wy = (watermark.size[0] - original.size[0]) // 2, (watermark.size[1] - original.size[1]) // 2

    # Create a new image by combining original and watermark
    watermarked = Image.new('RGBA', original.size)
    watermarked.paste(original, (0, 0))
    watermarked.paste(watermark, (-wx, -wy), mask=watermark)

    # Save the result in the same directory as the original image
    output_path = os.path.join(os.path.dirname(image_path), f"watermarked_{os.path.basename(image_path)}")
    watermarked.convert('RGB').save(output_path, 'JPEG')

    print(f"Watermarked image created: {output_path}")

def find_largest_image_size(directory):
    max_width, max_height = 0, 0
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(directory, filename)
            with Image.open(image_path) as img:
                width, height = img.size
                max_width, max_height = max(max_width, width), max(max_height, height)
    return max_width * 2, max_height * 2  # Quadruple the size for rotation and complete coverage

def apply_watermark_to_images(directory, watermark_text, font_size, h_spacing, v_spacing, color, opacity, font_path):
    # Find the size of the largest image
    watermark_size = find_largest_image_size(directory)

    # Create the watermark
    watermark = create_watermark(watermark_size, watermark_text, font_size, h_spacing, v_spacing, color, opacity, font_path)

    # Iterate over files in the specified directory and apply watermark
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and not filename.startswith("watermarked_"):
            image_path = os.path.join(directory, filename)
            apply_watermark_to_image(image_path, watermark)

def main():
    parser = argparse.ArgumentParser(description='Apply a watermark to images in a directory.')
    parser.add_argument('directory', type=str, help='Directory containing images to watermark')
    parser.add_argument('watermark_text', type=str, help='Text to use as the watermark')
    parser.add_argument('--font_size', type=int, default=20, help='Font size of the watermark text (default: 20)')
    parser.add_argument('--h_spacing', type=int, default=100, help='Horizontal spacing between watermark repeats (default: 100)')
    parser.add_argument('--v_spacing', type=int, default=100, help='Vertical spacing between watermark repeats (default: 100)')
    parser.add_argument('--color', type=int, nargs=3, default=[255, 255, 255], help='Watermark text color as RGB (default: 255 255 255)')
    parser.add_argument('--opacity', type=float, default=0.5, help='Opacity of the watermark text (default: 0.5)')
    parser.add_argument('--font_path', type=str, default='', help='Path to a custom font file (optional)')

    args = parser.parse_args()

    apply_watermark_to_images(args.directory, args.watermark_text, args.font_size, args.h_spacing, args.v_spacing, args.color, args.opacity, args.font_path)

if __name__ == "__main__":
    main()
