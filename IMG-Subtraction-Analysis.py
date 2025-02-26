# ===========================================================================
#
# Script Name: IMG-Subtraction-Analysis.py
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
# This script implements image subtraction analysis for digital image comparison.
# It performs pixel-by-pixel subtraction between a reference image and a questioned image
# to identify differences.
#
# Applications of this script include:
# 1. Forensic image comparison
# 2. Detection of image alterations
# 3. Visualization of image differences
#
# Process:
# 1. Select a reference image file.
# 2. Select a questioned image file.
# 3. Perform image subtraction.
# 4. Generate a difference image and quantitative similarity metrics.
# 5. Output a report including the difference image, histograms, and similarity percentage.
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
from PIL import Image

def create_analysis_folder(analysis_folder="IMG-Subtraction-Analysis", report_file_name="IMG-Subtraction-Analysis-Report.txt"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_folder = os.path.join(script_dir, analysis_folder)
    os.makedirs(analysis_folder, exist_ok=True)
    report_file_path = os.path.join(analysis_folder, report_file_name)
    return analysis_folder, report_file_path

def create_report_header(report_file_path):
    with open(report_file_path, 'w') as report_file:
        report_file.write("Image Subtraction Analysis Report\n")
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
        report_file.write("This script implements the image subtraction option as an alternative method in the aforementioned study,\n")
        report_file.write("incorporating the recommended error mitigation techniques.\n\n")
        report_file.write("=============================================\n")
        report_file.write("The script conducted a test of two images pixels and compared them for similarity.\n\n")
        report_file.write("The testing hypothesis:\n\n")
        report_file.write("Null (Ho) - Image pixels are similar.\n")
        report_file.write("Alternative (Ha) - Image pixels are not similar.\n\n")
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

def get_color_space(image):
    if image.shape[2] == 4:
        return 'CMYK'
    elif image.shape[2] == 3:
        return 'RGB'
    elif len(image.shape) == 2 or image.shape[2] == 1:
        return 'Grayscale'
    else:
        return 'Unknown'

def create_combined_histogram(I, J, analysis_folder):
    I_rgb = cv2.cvtColor(I, cv2.COLOR_BGR2RGB) if len(I.shape) == 3 else cv2.cvtColor(I, cv2.COLOR_GRAY2RGB)
    J_rgb = cv2.cvtColor(J, cv2.COLOR_BGR2RGB) if len(J.shape) == 3 else cv2.cvtColor(J, cv2.COLOR_GRAY2RGB)

    colors = ('r', 'g', 'b')
    plt.figure(figsize=(15, 5))

    for i, color in enumerate(colors):
        I_hist = cv2.calcHist([I_rgb], [i], None, [256], [0, 256])
        J_hist = cv2.calcHist([J_rgb], [i], None, [256], [0, 256])
        
        plt.subplot(1, 3, i+1)
        plt.plot(I_hist, color=color, alpha=0.5, label='Reference')
        plt.plot(J_hist, color=color, linestyle='dashed', alpha=0.5, label='Questioned')
        plt.xlim([0, 256])
        plt.title(f'{color.upper()} Channel')
        plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, 'Combined_Histogram.png'), dpi=600)
    plt.close()

def generate_conclusion(ref_file_name, ques_file_name, percentage_similar, report_file_path):
    with open(report_file_path, 'a') as report_file:
        report_file.write("\n=============================================\n")
        report_file.write("Conclusion\n")
        report_file.write("=============================================\n\n")
        report_file.write(f"The hypothesis testing involved a detailed comparison of pixel values between the reference image ({ref_file_name}) and the questioned image ({ques_file_name}).\n\n")
        report_file.write("Hypotheses:\n")
        report_file.write("Null (Ho): Image pixels are similar.\n")
        report_file.write("Alternative (Ha): Image pixels are not similar.\n\n")

        if percentage_similar == 100:
            report_file.write("Matched Images:\n\n")
            report_file.write(f"Based on the image subtraction analysis, the null hypothesis (Ho) is supported. The comparison revealed that {percentage_similar:.2f}% of the pixels in the questioned image matched those in the reference image. This indicates that the images are identical in pixel values, suggesting that they are either the same image or identical copies.\n")
        else:
            report_file.write("Non-Matched Images:\n\n")
            report_file.write(f"The alternative hypothesis (Ha) is supported. The analysis showed that {100-percentage_similar:.2f}% of pixels did not match, indicating discrepancies between the questioned and reference images. These discrepancies could suggest different origins, alterations, or modifications. For a forensic examination, further investigation would be required to determine the reasons for these differences.\n")

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

def image_subtraction(I, J, analysis_folder, report_file_path, ref_file_name, ques_file_name):
    with open(report_file_path, 'a') as report_file:
        report_file.write("\n=============================================\n")
        report_file.write("Pixel Analysis - Image Subtraction\n")
        report_file.write("=============================================\n\n")

    img_diff = np.abs(I.astype(int) - J.astype(int))
    img_diff = np.clip(img_diff, 0, 255).astype(np.uint8)
    diff_img = Image.fromarray(img_diff)

    diff_img.save(os.path.join(analysis_folder, 'Image_Difference.png'))

    total_pixels = I.size // I.shape[2]
    different_pixels = np.sum(img_diff != 0) // I.shape[2]
    similar_pixels = total_pixels - different_pixels
    percentage_similar = (similar_pixels / total_pixels) * 100

    with open(report_file_path, 'a') as report_file:
        report_file.write('Image Subtraction Analysis\n')
        report_file.write('------------------------------------\n')
        report_file.write(f'Total Pixels in Reference File (I): {total_pixels}\n')
        report_file.write(f'Total Pixels in Questioned File (J): {total_pixels}\n\n')
        
        report_file.write('Image Subtraction Findings\n')
        report_file.write('------------------------------------\n')
        report_file.write(f'Number of Different Pixels: {different_pixels}\n')
        report_file.write(f'Percentage of Same or Similar Pixels: {percentage_similar:.6f}%\n')

    montage = np.hstack((I, J))
    cv2.imwrite(os.path.join(analysis_folder, 'Montage.png'), montage, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    create_combined_histogram(I, J, analysis_folder)

    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(I, cv2.COLOR_BGR2RGB))
    plt.title('Reference Image')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(J, cv2.COLOR_BGR2RGB))
    plt.title('Questioned Image')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(img_diff)
    plt.title('Image Difference')
    plt.axis('off')
    
    plt.savefig(os.path.join(analysis_folder, 'Image_Comparison_Plot.png'), dpi=600, bbox_inches='tight')
    plt.close()

    generate_conclusion(ref_file_name, ques_file_name, percentage_similar, report_file_path)

def main():
    analysis_folder, report_file_path = create_analysis_folder()
    create_report_header(report_file_path)
    print("Image subtraction analysis began...\n")

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

    image_subtraction(I, J, analysis_folder, report_file_path, ref_file_name, ques_file_name)
    
    add_references(report_file_path)

    print("Image subtraction analysis completed. Check the analysis folder for results.")

if __name__ == "__main__":
    main()
