import argparse
from PIL import Image, ImageDraw, ImageFont
import os
import sys

def create_watermark(watermark_size, watermark_text, font_size, h_spacing, v_spacing, color, opacity, font_path):
    print(f"Creating watermark canvas of size: {watermark_size}")
    watermark = Image.new('RGBA', watermark_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    font = ImageFont.truetype(font_path, font_size) if font_path and os.path.exists(font_path) else ImageFont.load_default()
    text_color = (color[0], color[1], color[2], int(255 * opacity))

    print(f"Adding watermark text '{watermark_text}' with font size {font_size}, spacing {h_spacing}x{v_spacing}, color {color}, opacity {opacity}")
    for x in range(0, watermark_size[0], h_spacing):
        for y in range(0, watermark_size[1], v_spacing):
            draw.text((x, y), watermark_text, fill=text_color, font=font)

    print("Rotating watermark")
    watermark = watermark.rotate(45, expand=1)

    return watermark

def apply_watermark_to_image(image_path, watermark):
    print(f"Loading image: {image_path}")
    original = Image.open(image_path)

    # Convert original image to 'RGBA' if it's not already in that mode
    if original.mode != 'RGBA':
        original = original.convert('RGBA')

    wx, wy = (watermark.size[0] - original.size[0]) // 2, (watermark.size[1] - original.size[1]) // 2
    watermarked = Image.new('RGBA', original.size, (255, 255, 255, 0))
    watermarked.paste(original, (0, 0), original)
    watermarked.paste(watermark, (-wx, -wy), watermark)

    # Determine output format based on the original image format and if it supports transparency
    output_format = 'PNG' if original.format in ['PNG', 'GIF'] or original.mode == 'RGBA' else 'JPEG'
    output_path = os.path.join(os.path.dirname(image_path), f"watermarked_{os.path.basename(image_path)}")
    watermarked.save(output_path, output_format)

    print(f"Watermarked image saved: {output_path}")



def find_largest_image_size(directory):
    print(f"Scanning directory {directory} for largest image size")
    max_width, max_height = 0, 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and not filename.startswith("watermarked_"):
                image_path = os.path.join(root, filename)
                try:
                    with Image.open(image_path) as img:
                        width, height = img.size
                        max_width, max_height = max(max_width, width), max(max_height, height)
                except IOError:
                    print(f"Skipping non-image file: {image_path}")
    print(f"Largest image size found: {max_width}x{max_height}")
    return max_width * 2, max_height * 2


def apply_watermark_to_images(directory, watermark_text, font_size, h_spacing, v_spacing, color, opacity, font_path):
    watermark_size = find_largest_image_size(directory)
    watermark = create_watermark(watermark_size, watermark_text, font_size, h_spacing, v_spacing, color, opacity, font_path)

    print(f"Applying watermark to images in {directory}")
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and not filename.startswith("watermarked_"):
                image_path = os.path.join(root, filename)
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
