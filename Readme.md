# Image Comparison Tool

![Version](https://img.shields.io/badge/version-1.3-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.6%2B-yellow)

## Overview

The Image Comparison Tool is a Python script designed for intermediate-level forensic analysis of digital images. It goes beyond basic metadata analysis to perform pixel-level comparisons between a reference image and a questioned image, identifying similarities and differences using advanced image processing techniques. While not exhaustive, this tool provides valuable insights for various applications, including image authentication, detection of image alterations, and forensic image comparison. It serves as a robust starting point for digital image forensics, offering quantitative and visual representations of image differences.

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

## How It Works

The tool uses OpenCV's cv2.absdiff() function to compute the absolute difference between the reference and questioned images. It then applies thresholding and contour detection to identify and highlight areas of significant difference. The results are presented both visually and in a detailed text report.

## Package Requirements

- numpy
- matplotlib
- Pillow (PIL)
- OpenCV (cv2)

## Installation

To install the required packages, use pip:

pip install numpy matplotlib Pillow opencv-python

## Usage

1. Clone this repository to your local machine:

git clone https://github.com/ronin4n6labs/IMG-Comparison-Tool-Python.git

2. Navigate to the project directory:

cd IMG-Comparison-Tool-Python

3. Run the script:

python image_comparison_tool.py

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

## Limitations

- This tool is designed for basic to intermediate forensic analysis and should not be considered a comprehensive forensic solution.
- Results may vary depending on image quality and the nature of alterations.
- The tool does not account for advanced image manipulation techniques.

## Methodology

This script is based on analysis methodology used in:

Wales, G. S. Validation of image stream hashing: A forensic method for content verification. J Forensic Sci. 2024; 69: 515–28. https://doi.org/10.1111/1556-4029.15432

**This Image Comparison Tool was developed and used as part of a larger, more complex image comparison analysis, the findings of which are reported in the published paper cited above.**

## Citation

If you use this tool in your research or professional work, please cite it as follows:

Wales, G. S. (2025). Image Comparison Tool (Version 1.3) [Computer software]. https://github.com/ronin4n6labs/IMG-Comparison-Tool-Python

## Author

Gregory S. Wales, DFS
Email: media4n6@gmail.com
GitHub: Ronin4n6labs

## Version

1.3 (February 21, 2025)

## License

Please reference The MIT License file included with this script.
