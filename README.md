# Insta Splitter CLI

A simple wrapper around Pillow library to automate picture edits I often found myself doing before Instagram uploads

- splitting a picture into a grid of square cutouts
- adding horizontal white stripes over the top and bottom of the image.

## Installation

You can simply install the CLI via pip:

`pip install insta-splitter`

## Usage

You can call the CLI by typing `insta-splitter` into the command line.
You can use following arguments to process your image:

- `--mode`: expects a string value

  1. single-square: split the image into a single square
  2. three-squares: split the image horizontally into three squares
  3. grid: split the image into a grid of rows and columns

  If ommited, image will be left in original shape.

- `--stripes`: Apply white horizontal stripes to the image

- `--stripes-height`: Height of the white stripes as a decimal percentage of the image height. Default value is 0.16 (1/6 of the image height).

- `--rows`: Number of rows in the grid. Will be ignored if mode is not grid

- `--columns`: Number of columns in the grid. Will be ignored if mode is not grid

- `--out`: Path to the output directory. If not specified, input directory will be used.
