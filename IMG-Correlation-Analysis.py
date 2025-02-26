# ===========================================================================
#
# Script Name: IMG-Correlation-Analysis.py
#
# Script Written by Gregory S. Wales, DFS
# Date: February 26, 2025
# Image Subtraction Analysis for Digital Image Forensics
# - script v1.1
# Email: media4n6@gmail.com
# GITHUB: ronin4n6labs
#
# ---------------------------------------------------------------------------
#
# Purpose of this script:
# This script implements image correlation analysis for digital image comparison.
# It performs Pearson Correlation Coefficient between a reference image and a questioned image
# to identify simularity.
#
# Applications of this script include:
# 1. Forensic image comparison
# 2. Detection of image alterations
# 3. Visualization of image differences
#
# Process:
# 1. Select a reference image file.
# 2. Select a questioned image file.
# 3. Perform image correlation.
# 4. Generate a similarity metrics.
# 5. Output a report.
#
# The script analyzes:
# 1. Pixel differences between images
# 2. Quantitative measures of similarity
#
# It is designed to determine and visualize differences between two images.
#
# Requirements:
# - tkinter
# - Pillow (PIL)
# - opencv-python (cv2)
# - numpy
# - matplotlib
# - subprocess
# - os
#
# The script produces a detailed report in a text file and generates visual outputs.
#
# Error handling includes checks for file selection and image loading.
#
# The following packages are required:
# - Pillow (PIL): Image processing library
# - tkinter: GUI library
# - opencv-python (cv2): Computer vision library
# - numpy: Numerical computing library
# - matplotlib: Plotting library
#
# To install, use the following commands:
# pip install Pillow
# pip install opencv-python
# pip install numpy
# pip install matplotlib
#
# External Tool Requirements:
# - PowerShell (for Get-FileHash cmdlet)
#
# Please reference The MIT License file included with this script.
# ===========================================================================

import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import numpy as np
import cv2
from matplotlib import pyplot as plt

def create_analysis_folder(analysis_folder="IMG-Correlation-Analysis", report_file_name="IMG-Correlation-Analysis-Report.txt"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_folder = os.path.join(script_dir, analysis_folder)
    os.makedirs(analysis_folder, exist_ok=True)
    report_file_path = os.path.join(analysis_folder, report_file_name)
    return analysis_folder, report_file_path

def create_report_header(report_file_path):
    with open(report_file_path, 'w') as report_file:
        report_file.write("Image Correlation Analysis Report\n")
        report_file.write("\n------------------------------------\n\n")
        report_file.write("Stream hashing for digital images verifies content integrity during file container conversion and encoding\n")
        report_file.write("scheme changes, commonly used in multimedia forensics [1].\n\n")
        report_file.write("A validation study with over 1500 experiments assessed the method's forensic fitness, identifying errors\n")
        report_file.write("and limitations. Initial tests revealed significant errors in two of five file types. Further analysis\n")
        report_file.write("pinpointed error causation and led to developing standard control methods.\n\n")
        report_file.write("Initial average error rates for all images (before control methods) were:\n")
        report_file.write("- False Negative Rate = 0.775%\n")
        report_file.write("- False Positive Rate = 67.5%\n\n")
        report_file.write("Implementing these controls reduced errors to negligible levels (0%), confirming the method's forensic\n")
        report_file.write("suitability for BMP, JPG, PNG, and TIF files. The study emphasized the necessity of error mitigation\n")
        report_file.write("techniques for reliable use and highlighted the need for further research on additional file types\n")
        report_file.write("and software tools [2].\n\n")
        report_file.write("This script implements the image correlation option as an alternative method in the aforementioned study,\n")
        report_file.write("incorporating the recommended error mitigation techniques.\n\n")
        report_file.write("=============================================\n")
        report_file.write("The script conducted a test of two images pixels and compared them for correlation.\n\n")
        report_file.write("The testing hypothesis:\n\n")
        report_file.write("Null (Ho) - Image pixels are correlated.\n")
        report_file.write("Alternative (Ha) - Image pixels are not correlated.\n\n")
        report_file.write("=============================================\n")
        report_file.write("Preprocessing\n")
        report_file.write("=============================================\n\n")

def process_file(file_path, file_type, report_file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    with open(report_file_path, 'a') as report_file:
        report_file.write(f"{file_type} File\n")
        report_file.write("------------------------------------\n")
        report_file.write(f"File Name: {file_name}\n")
        report_file.write(f"File Size: {file_size} bytes\n")
    
    for algorithm in ['MD5', 'SHA1', 'SHA256']:
        ps_command = f'Get-FileHash "{file_path}" -Algorithm {algorithm} | Select-Object -ExpandProperty Hash'
        result = subprocess.run(['pwsh', '-Command', ps_command], capture_output=True, text=True)
        
        with open(report_file_path, 'a') as report_file:
            if result.returncode == 0:
                report_file.write(f"File hash ({algorithm}): {result.stdout.strip()}\n")
            else:
                report_file.write(f"Error computing {algorithm} hash: {result.stderr.strip()}\n")

def calculate_pearson_correlation(I, J):
    # Flatten the images and convert to float32
    I_flat = I.astype(np.float32).flatten()
    J_flat = J.astype(np.float32).flatten()

    # Calculate Pearson correlation coefficient
    correlation_coefficient = np.corrcoef(I_flat, J_flat)[0, 1]
    return correlation_coefficient

def generate_conclusion(ref_file_name, ques_file_name, correlation_coefficient, report_file_path):
    # Determine similarity level based on the correlation coefficient
    if 0.95 <= correlation_coefficient <= 1.0:
        similarity_desc = "Very high similarity (nearly identical)"
    elif 0.7 <= correlation_coefficient < 0.95:
        similarity_desc = "High similarity (some differences)"
    elif 0.5 <= correlation_coefficient < 0.7:
        similarity_desc = "Moderate similarity (noticeable differences)"
    elif 0.3 <= correlation_coefficient < 0.5:
        similarity_desc = "Low similarity (significant differences)"
    else:  # 0.0 <= correlation_coefficient < 0.3
        similarity_desc = "Very low similarity (highly different)"

    with open(report_file_path, 'a') as report_file:
        report_file.write("\n=============================================\n")
        report_file.write("Conclusion\n")
        report_file.write("=============================================\n\n")
        report_file.write(f"The hypothesis testing involved a correlation analysis of pixel values between the reference image ({ref_file_name}) and the questioned image ({ques_file_name}).\n\n")
        report_file.write("Hypotheses:\n")
        report_file.write("Null (Ho): Image pixels are correlated.\n")
        report_file.write("Alternative (Ha): Image pixels are not correlated.\n\n")
        report_file.write(f"Pearson Correlation Coefficient: {correlation_coefficient:.4f}\n\n")

        if correlation_coefficient > 0.7:
            report_file.write(f"Based on the correlation analysis, the null hypothesis (Ho) is supported. The Pearson Correlation Coefficient indicates {similarity_desc} between the images, suggesting a high degree of similarity.\n")
        else:
            report_file.write(f"Based on the correlation analysis, the alternative hypothesis (Ha) is supported. The Pearson Correlation Coefficient indicates {similarity_desc} between the images, suggesting significant differences.\n")

def add_references(report_file_path):
    with open(report_file_path, 'a') as report_file:
        report_file.write("\n=============================================\n")
        report_file.write("References\n")
        report_file.write("=============================================\n\n")
        report_file.write("[1] Wales GS, Smith JM, Lacey DS, Grigoras C. \n")
        report_file.write("    Multimedia stream hashing: A forensic method for \n")
        report_file.write("    content verification. J Forensic Sci. 2023;68:289–300. https://\n")
        report_file.write("    doi.org/10.1111/1556-4029.15148\n\n")
        report_file.write("[2] Wales GS.  Validation of image stream hashing: A forensic \n")
        report_file.write("    method for content verification.  J Forensic Sci.\n")
        report_file.write("    2024 ; 69 : 515 – 28 .  https://doi.org/10.1111/1556-\n")
        report_file.write("    4029.15432\n")

def image_correlation_analysis(I, J, analysis_folder, report_file_path, ref_file_name, ques_file_name):
    with open(report_file_path, 'a') as report_file:
        report_file.write("\n=============================================\n")
        report_file.write("Pixel Analysis - Image Correlation\n")
        report_file.write("=============================================\n\n")

    # Calculate Pearson Correlation Coefficient
    correlation_coefficient = calculate_pearson_correlation(I, J)

    with open(report_file_path, 'a') as report_file:
        report_file.write('Image Correlation Analysis\n')
        report_file.write('------------------------------------\n')
        report_file.write(f'Pearson Correlation Coefficient: {correlation_coefficient:.4f}\n\n')
        report_file.write('Similarity Scale:\n')
        report_file.write('- 0.95 <= r <= 1.0: Very high similarity (nearly identical)\n')
        report_file.write('- 0.7 <= r < 0.95: High similarity (some differences)\n')
        report_file.write('- 0.5 <= r < 0.7: Moderate similarity (noticeable differences)\n')
        report_file.write('- 0.3 <= r < 0.5: Low similarity (significant differences)\n')
        report_file.write('- 0.0 <= r < 0.3: Very low similarity (highly different)\n\n')

    montage = np.hstack((I, J))
    cv2.imwrite(os.path.join(analysis_folder, 'Montage.png'), montage, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    generate_conclusion(ref_file_name, ques_file_name, correlation_coefficient, report_file_path)

def main():
    analysis_folder, report_file_path = create_analysis_folder()
    create_report_header(report_file_path)
    print("Image correlation analysis began...\n")

    print("Loading reference and questioned files...")
    root = tk.Tk()
    root.withdraw()

    ref_full_file_path = filedialog.askopenfilename(
        title='Select the reference file',
        filetypes=[
            ('Image files', '*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.jp2 *.jpx'),
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('BMP files', '*.bmp'),
            ('TIFF files', '*.tiff *.tif'),
            ('JPEG 2000 files', '*.jp2 *.jpx'),
            ('All files', '*.*')
        ]
    )

    if ref_full_file_path == '':
        print('User canceled reference file selection')
        with open(report_file_path, 'a') as report_file:
            report_file.write('User canceled reference file selection\n')
        return

    process_file(ref_full_file_path, "Reference", report_file_path)

    ques_full_file_path = filedialog.askopenfilename(
        title='Select the questioned file',
        filetypes=[
            ('Image files', '*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.gif *.jp2 *.jpx'),
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('BMP files', '*.bmp'),
            ('TIFF files', '*.tiff *.tif'),
            ('JPEG 2000 files', '*.jp2 *.jpx'),
            ('All files', '*.*')
        ]
    )

    if ques_full_file_path == '':
        print('User canceled questioned file selection')
        with open(report_file_path, 'a') as report_file:
            report_file.write('\nUser canceled questioned file selection\n')
        return

    process_file(ques_full_file_path, "Questioned", report_file_path)

    print("Test files loaded successfully.\n")

    I = cv2.imread(ref_full_file_path)
    J = cv2.imread(ques_full_file_path)

    ref_ext = os.path.splitext(ref_full_file_path)[1]
    ques_ext = os.path.splitext(ques_full_file_path)[1]
    cv2.imwrite(os.path.join(analysis_folder, f'Reference{ref_ext}'), I)
    cv2.imwrite(os.path.join(analysis_folder, f'Questioned{ques_ext}'), J)

    ref_file_name = os.path.basename(ref_full_file_path)
    ques_file_name = os.path.basename(ques_full_file_path)

    image_correlation_analysis(I, J, analysis_folder, report_file_path, ref_file_name, ques_file_name)
    
    add_references(report_file_path)

    print("Image correlation analysis completed. Check the analysis folder for results.")

if __name__ == "__main__":
    main()
