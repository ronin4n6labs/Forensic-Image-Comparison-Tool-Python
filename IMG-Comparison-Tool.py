# ===========================================================================
#
# Script Name: IMG-Comparison-Tool.py
#
# Script Written by Gregory S. Wales, DFS
# Date: February 21, 2025
# Image Comparison Analysis for Image Differences
# - script v1.3
# Email: media4n6@gmail.com
# GITHUB: ronin4n6labs
#
# ---------------------------------------------------------------------------
#
# Purpose of this script:
# This script performs a comprehensive comparison of two digital images for
# forensic analysis. It compares a reference image with a questioned image to
# identify similarities and differences using image processing techniques.
#
# Applications of this image comparison analysis include:
# 1. Image authentication
# 2. Detection of image alterations
# 3. Forensic image comparison
# 4. Content verification
#
# Package Requirements:
# - numpy
# - matplotlib
# - Pillow (PIL)
# - OpenCV (cv2)
#
# Process:
# 1. Select reference image file
# 2. Select questioned image file for analysis
# 3. Perform dimensional analysis of both images
# 4. Analyze color spaces of both images
# 5. Conduct image comparison using absolute difference
# 6. Generate a comprehensive report with findings
# 7. Create visual representations of image differences
# 8. Save results in a subfolder titled "IMG-Comparison-Tool"
#
# Requirements:
# - Reference image file
# - Questioned image file for comparison
# - Sufficient computational resources for processing large images
#
# Key points:
# - Dimensional analysis compares image sizes and resizes if necessary
# - Color space analysis ensures compatibility
# - Absolute difference is used for image comparison
# - Percentage of different pixels is calculated
# - A montage of reference and questioned images is created
# - An image highlighting differences with bounding boxes is generated
# - Results are saved in a detailed text report
# - The script supports various image formats: PNG, JPG, JPEG, BMP, TIFF, TIF, GIF, JP2, JPX
#
# Error handling:
# - The script includes checks for image dimension mismatches and resizes if needed
# - Color space incompatibilities are reported
#
# Performance:
# - The script processes images efficiently using OpenCV and numpy arrays
# - Total processing time may vary based on image sizes
#
# This script compares two images and generates a report of the differences.
# It is based on the methodology described in:
# Wales, G. S. Validation of image stream hashing: A forensic method for content verification. 
# J Forensic Sci. 2024; 69: 515–28. https://doi.org/10.1111/1556-4029.15432
#
# Please reference The MIT License file included with this script.
# ===========================================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
from PIL import Image
from datetime import datetime
import shutil
import cv2

def get_color_space(image):
    if image.shape[2] == 3:
        return 'RGB'
    elif image.shape[2] == 1:
        return 'Grayscale'
    elif image.shape[2] == 4:
        return 'CMYK'
    else:
        return 'Unknown'

def load_image(file_type):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=f"Select {file_type}", filetypes=[
        ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif;*.gif;*.jp2;*.jpx")
    ])
    return file_path

def create_report_folder():
    script_name = "IMG-Comparison-Tool"
    folder_path = os.path.join(os.getcwd(), script_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_report(folder_path, report_content):
    report_file_path = os.path.join(folder_path, "Image-Comparison-Report.txt")
    with open(report_file_path, "w") as file:
        file.write(report_content)

def copy_and_rename_image(source_path, destination_folder, new_name):
    _, ext = os.path.splitext(source_path)
    new_path = os.path.join(destination_folder, f"{new_name}{ext}")
    shutil.copy2(source_path, new_path)
    return new_path

def create_montage(ref_path, ques_path, output_path):
    ref_img = Image.open(ref_path)
    ques_img = Image.open(ques_path)
    
    max_width = max(ref_img.width, ques_img.width)
    max_height = max(ref_img.height, ques_img.height)
    ref_img = ref_img.resize((max_width, max_height))
    ques_img = ques_img.resize((max_width, max_height))
    
    montage = Image.new('RGB', (max_width * 2, max_height))
    montage.paste(ref_img, (0, 0))
    montage.paste(ques_img, (max_width, 0))
    
    montage.save(output_path, dpi=(600, 600))

def compute_image_difference(ref_img, ques_img):
    # Compute absolute difference
    diff = cv2.absdiff(ref_img, ques_img)
    
    # Convert to grayscale
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh_diff = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a copy of the reference image to draw on
    result = ref_img.copy()
    
    # Draw contours and bounding boxes
    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:  # Adjust this threshold as needed
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # Calculate percentage of different pixels
    total_pixels = ref_img.shape[0] * ref_img.shape[1]
    different_pixels = np.count_nonzero(thresh_diff)
    percentage_diff = (different_pixels / total_pixels) * 100
    
    return result, percentage_diff

def main():
    print("Image Comparison Analysis started...")
    
    ref_image_path = load_image("Reference File")
    ques_image_path = load_image("Questioned File")

    ref_image_name = os.path.basename(ref_image_path)
    ques_image_name = os.path.basename(ques_image_path)

    I = cv2.imread(ref_image_path)
    J = cv2.imread(ques_image_path)

    if I.shape != J.shape:
        J = cv2.resize(J, (I.shape[1], I.shape[0]))

    color_space_I = get_color_space(I)
    color_space_J = get_color_space(J)

    folder_path = create_report_folder()

    ref_copy_path = copy_and_rename_image(ref_image_path, folder_path, "reference")
    ques_copy_path = copy_and_rename_image(ques_image_path, folder_path, "questioned")

    montage_path = os.path.join(folder_path, "ref_v_q-montage.png")
    create_montage(ref_copy_path, ques_copy_path, montage_path)

    diff_image, percentage_diff = compute_image_difference(I, J)

    report_content = []
    report_content.append(f"Analysis Report")
    report_content.append(f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_content.append(f"Reference File (I): {ref_image_name}")
    report_content.append(f"Questioned File (J): {ques_image_name}\n")
    report_content.append("Testing Hypothesis:")
    report_content.append("Null Hypothesis (H0): The image pixels are the same.")
    report_content.append("Alternative Hypothesis (Ha): The image pixels are different.")
    report_content.append("----------------------------------------------------------\n")
    report_content.append("Note: This analysis is based on the methodology described in Wales (2024).")
    report_content.append("----------------------------------------------------------\n")
    report_content.append("---------- Begin Image Comparison Analysis ---------------\n")

    report_content.append("------------ Dimensional Difference Evaluation -----------")
    report_content.append(f"Dimensions of Reference Image (I): {I.shape[0]} x {I.shape[1]} pixels")
    report_content.append(f"Dimensions of Questioned Image (J): {J.shape[0]} x {J.shape[1]} pixels")
    report_content.append(f"Height Difference: {abs(I.shape[0] - J.shape[0])} pixels")
    report_content.append(f"Width Difference: {abs(I.shape[1] - J.shape[1])} pixels")
    
    if I.shape == J.shape:
        dimensional_finding = "The dimensions of both images are identical."
    else:
        dimensional_finding = "The dimensions of the images do not match. The questioned image was resized to match the reference image."
    report_content.append(f"Finding: {dimensional_finding}")
    report_content.append("----------------------------------------------------------\n")

    report_content.append("------------- Color Space Analysis -----------------------")
    report_content.append(f"Color spaces of both images (I and J) are: {color_space_I}")
    report_content.append("----------------------------------------------------------\n")

    report_content.append("----------- Image Difference Comparison Analysis ---------")
    report_content.append(f'Percentage of Different Pixels: {percentage_diff:.2f}%')
    report_content.append(f'Percentage of Similar Pixels: {100 - percentage_diff:.2f}%')
    
    if percentage_diff == 0:
        pixel_finding = "The images are identical at the pixel level."
    else:
        pixel_finding = f"The images show differences. {percentage_diff:.2f}% of pixels are different."
    report_content.append(f"Finding: {pixel_finding}")
    report_content.append("----------------------------------------------------------\n")

    report_content.append("--------------- Testing Conclusion -----------------------")
    if percentage_diff == 0:
        conclusion = "We fail to reject the null hypothesis. The images appear to be identical."
    else:
        conclusion = "We reject the null hypothesis. The images show differences."
    report_content.append(conclusion)
    report_content.append("----------------------------------------------------------\n")

    image_diff_path = os.path.join(folder_path, 'Image_Difference.png')
    cv2.imwrite(image_diff_path, diff_image)

    report_content.append(f"Report & Test Images saved to IMG-Comparison-Tool subfolder.")
    report_content.append("\n------------------ End Image Comparison Analysis ----------")

    report_content.append("\n--------------------- References ------------------------")
    report_content.append("Wales, G. S. Validation of image stream hashing: A forensic method for content verification. J Forensic Sci. 2024; 69: 515–28. https://doi.org/10.1111/1556-4029.15432")
    report_content.append("----------------------------------------------------------")

    save_report(folder_path, "\n".join(report_content))

    print(f"Image Comparison Analysis completed. Results saved in {folder_path}")

if __name__ == "__main__":
    main()
