# Remarkable Watermarking Script

## Overview

The Remarkable Watermarking Script is a Python utility designed for batch watermarking of images within a specified directory. It efficiently processes multiple images by creating a single, large watermark that covers even the largest image in the directory. This approach ensures that the watermark is applied consistently to all images, maintaining both speed and quality.

## Features

- **Batch Processing**: Apply watermarks to all images in a specified directory with a single command.
- **Optimized Performance**: Generates one large watermark to efficiently process multiple images.
- **Customizable Watermark**: Allows customization of the watermark text, font size, color, opacity, and more.
- **Rotation for Coverage**: Rotates the watermark for aesthetic appeal and better coverage.
- **Flexible Spacing**: Adjustable horizontal and vertical spacing for repeated watermark text.

## Requirements

- Python 3.x
- Pillow library

## Installation

1. Ensure Python 3.x is installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

2. Install the Pillow library, a fork of PIL (Python Imaging Library), which provides extensive file format support and efficient internal representation. Install it using pip:

   ```bash
   pip install pillow
   ```

3. Clone the repository or download the script:

```bash
git clone https://github.com/mullinmax/remarkable.git
```

## Usage
Navigate to the script directory and run the script from the command line. The script requires specifying the directory containing the images and the watermark text. Additional optional arguments allow customization of the watermark.

```bash
python3 watermark.py <directory> <watermark_text> [options]
```

## Options
`--font_size` : Font size of the watermark text (default: 20)

`--h_spacing` : Horizontal spacing between watermark repeats (default: 100)

`--v_spacing` : Vertical spacing between watermark repeats (default: 100)

`--color` : Watermark text color as RGB (default: 255 255 255)

`--opacity` : Opacity of the watermark text (default: 0.5)

`--font_path` : Path to a custom font file (optional)

## Example
```bash
python3 watermark.py /path/to/images "Your Watermark" --font_size 30 --h_spacing 150 --v_spacing 120 --color 255 0 0 --opacity 0.8
```
This command applies the watermark "Your Watermark" with specified font size, spacing, color, and opacity to all images in /path/to/images.

### Contributing
Contributions to the Remarkable Watermarking Script are welcome! If you have suggestions for improvement or want to contribute to the code, please feel free to fork the repository, make changes, and submit a pull request.

### License
This project is licensed under the MIT License - see the LICENSE file in the repository for details.

