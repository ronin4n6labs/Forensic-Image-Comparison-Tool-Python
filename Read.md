# Image Comparison Tool

## Overview

The **Image Comparison Tool** is a Python script designed for forensic analysis of digital images. It compares a reference image with a questioned image to identify similarities and differences using image processing techniques. This tool can be used for various applications, including image authentication, detection of image alterations, and forensic image comparison.

## Features

- Performs dimensional analysis of images.
- Analyzes color spaces for compatibility.
- Computes absolute differences between images.
- Generates a detailed report with findings.
- Creates visual representations of image differences.
- Highlights areas of difference with red bounding boxes in the output image.
- Supports multiple image formats: PNG, JPG, JPEG, BMP, TIFF, TIF, GIF, JP2, JPX.

## Applications

1. Image authentication
2. Detection of image alterations
3. Forensic image comparison
4. Content verification

## Package Requirements

- numpy
- matplotlib
- Pillow (PIL)
- OpenCV (cv2)

## Installation

To install the required packages, you can use pip:

pip install numpy matplotlib Pillow opencv-python


## Usage

1. Clone this repository to your local machine:

git clone https://github.com/ronin4n6labs/Image-Comparison-Tool.git

2. Navigate to the project directory:

cd Image-Comparison-Tool

3. Run the script:

python your_script_name.py

4. Follow the prompts to select the reference and questioned images for analysis.

## Test Files

This repository includes three test files for your own testing and analysis:

1. `Reference.jpg`: The reference image for comparison.
2. `Questioned-Match.jpg`: A questioned image that matches the reference.
3. `Questioned-Not-Match.jpg`: A questioned image that does not match the reference.

Use these files to test the script and understand its output in different scenarios.

## Output

The script generates a comprehensive report and visual outputs:

- A detailed text report of the analysis.
- A montage of the reference and questioned images.
- An image difference visualization (`Image_Difference.png`) that highlights areas of difference with red bounding boxes if the images don't match.

All outputs are saved in a subfolder named "IMG-Comparison-Tool".

## Methodology

This script is based on the methodology described in:

Wales, G. S. Validation of image stream hashing: A forensic method for content verification. J Forensic Sci. 2024; 69: 515–28. [https://doi.org/10.1111/1556-4029.15432](https://doi.org/10.1111/1556-4029.15432)

## License

Please reference The MIT License file included with this script.


