"""
Instagram grid and stripes

This script takes an image and splits it into a grid of rows and columns.

The user can choose between three modes:
- 'single-square': split the image into a single square.
- 'three-squares': split the image into three squares.
- 'grid': split the image into a grid of rows and columns.

The user can also choose to apply white horizontal stripes to the image.
"""

# TODO: Write tests
# TODO: Package the thing

import argparse
import sys
import os
import textwrap

from PIL import Image


def validate_path(file_path):
    """
    Validates if the input is a valid path to a file.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        return False, "File does not exist."

    # Check if it's a file
    if not os.path.isfile(file_path):
        return False, "Path is not a file."

    return True, None


def white_stripes(img, height):
    """
    Apply white horizontal stripes to the image.
    Cues in Seven Nation Army.
    """
    # Get image resolution
    img_width, img_height = img.size

    # Calculate the size of the stripes
    stripe_height = int(img_height * height)

    # Create a stripe image with the same width as the original image
    stripe = Image.new("RGB", (img_width, stripe_height), "white")

    # Paste the stripes into the original image (top and bottom)
    img.paste(stripe)
    img.paste(stripe, (0, img_height - stripe_height))

    return img

def split_to_grid(img, rows, columns):
    """
    Splits an image into a grid of rows and columns.
    """
    # Get image resolution
    img_width, img_height = img.size

    # Calculate the size of each cell (largest possible squares)
    col_width = img_width / columns
    row_height = img_height / rows

    cell_size = min(col_width, row_height)

    grid_height = cell_size * rows
    grid_width = cell_size * columns

    horziontal_padding = (img_width - grid_width) / 2
    vertical_padding = (img_height - grid_height) / 2

    # Create a list to store the cropped images
    images = []

    # crop and save each cell
    for i in range(rows):
        for j in range(columns):
            x0 = j * cell_size + horziontal_padding
            y0 = i * cell_size + vertical_padding
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            cell = img.crop((x0, y0, x1, y1))

            images.append(cell)

    return images


def main():
    """
    Main function to parse the arguments and call the appropriate function.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""Insta-splitter - Instagram grid and stripes"""),
    )

    # Mode
    parser.add_argument(
        "--mode",
        type=str,
        choices=["single-square", "three-squares", "grid"],
        help=textwrap.dedent(
            """\
                    Select the mode to split the image.
                    - single-square: split the image into a single square.
                    - three-squares: split the image horizontally into three squares.
                    - grid: split the image into a grid of rows and columns.
                    - If ommited, image will be left in original shape."""
        ),
    )

    # White stripes
    parser.add_argument(
        "--stripes",
        action="store_true",
        help="Apply white horizontal stripes to the image",
    )
    parser.add_argument(
        "--stripes-height",
        metavar="H",
        type=float,
        help=textwrap.dedent(
            """\
                Height of the white stripes as a decimal percentage of the image height.
                Default value is 0.16 (1/6)."""
        ),
    )

    # Rows and columns
    parser.add_argument(
        "--rows",
        metavar="R",
        type=int,
        help="Number of rows in the grid. Will be ignored if mode is not grid",
    )
    parser.add_argument(
        "--columns",
        metavar="C",
        type=int,
        help="Number of columns in the grid. Will be ignored if mode is not grid",
    )

    # Paths
    parser.add_argument("--src", metavar="IN", type=str, help="Path to the image file")
    parser.add_argument(
        "--out",
        metavar="OUT",
        type=str,
        help="Path to the output directory. If not specified, input directory will be used.",
    )

    args = parser.parse_args()

    # Validate path arguments
    image_path = args.src
    path_valid, error = validate_path(image_path)

    if not path_valid:
        print(error)
        sys.exit()

    if args.out is None:
        if os.path.dirname(image_path):
            args.out = os.path.dirname(image_path)
        else:
            args.out = os.getcwd()

    # Load an image from file
    img = Image.open(image_path)

    # Call the appropriate function based on the mode
    if args.mode == "single-square":
        images = split_to_grid(img, 1, 1)
    elif args.mode == "three-squares":
        images = split_to_grid(img, 1, 3)
    elif args.mode == "grid":
        images = split_to_grid(img, args.rows, args.columns)
    elif args.mode is None:
        images = [img]
    else:
        print(
            "Invalid mode. Ommit or select one of the following: single-square, three-squares, grid"
        )
        sys.exit()

    if args.stripes:
        # Set default value for stripes height
        if args.stripes_height is None:
            stripes_height = 1 / 6
        else:
            stripes_height = args.stripes_height

        # Apply white stripes to the image
        images = [white_stripes(img, stripes_height) for img in images]

    # Save the output to the specified directory
    for index, img in enumerate(images):
        img.save(f"{args.out}/output_{index}.jpeg")


if __name__ == "__main__":
    main()
