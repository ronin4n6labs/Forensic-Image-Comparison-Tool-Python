# ===========================================================================
#
# Script Name: IMG-Stream-Hash-Comparison.py
#
# Script Written by Gregory S. Wales, DFS
# Date: February 26, 2025
# Image Stream Hash Comparison Analysis for Digital Image Forensics
# - script v1.1
# Email: media4n6@gmail.com
# GITHUB: ronin4n6labs
#
# ---------------------------------------------------------------------------
#
# Purpose of this script:
# This script implements the image stream hashing method for digital image comparison.
# It computes SHA256 hashes of image streams and compares them to determine similarity.
#
# Applications of this script include:
# 1. Forensic image comparison
# 2. Content verification
# 3. Detection of image alterations
#
# Process:
# 1. Select a reference image file.
# 2. Select a questioned image file.
# 3. Generate stream hashes for both files using ffmpeg.
# 4. Compare the generated stream hashes.
# 5. Output a report indicating whether the image streams are similar or not.
#
# The script analyzes:
# 1. File hashes (MD5, SHA-1, SHA-256)
# 2. Image stream hashes (SHA256)
#
# It is designed to determine if the image streams are similar or not.
#
# Requirements:
# - ffmpeg (accessible via command line)
# - Pillow (PIL)
# - tkinter
# - subprocess
# - os
#
# The script produces a detailed report in a text file.
#
# Error handling includes checks for file selection, hash generation, and comparison.
#
# The following packages are required:
# - Pillow (PIL): Image processing library
# - tkinter:  GUI library
#
# To install, use the following commands:
# pip install Pillow
#
# External Tool Requirements:
# - PowerShell (for Get-FileHash cmdlet)
# - FFmpeg: (for streamhash)
#
# Please reference The MIT License file included with this script.
# ===========================================================================


import os
import tkinter as tk
from tkinter import filedialog
import subprocess

# Create the analysis folder
script_dir = os.path.dirname(os.path.abspath(__file__))
analysis_folder = os.path.join(script_dir, "IMG-Stream-Hash-Comparison-Analysis")
os.makedirs(analysis_folder, exist_ok=True)

# Create the report file
report_file_path = os.path.join(analysis_folder, "IMG-Stream-Hash-Comparison-Analysis-Report.txt")

# Write the initial content to the report
with open(report_file_path, 'w') as report_file:
    report_file.write("Image Stream Hash Comparison Analysis Report\n")
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
    report_file.write("This script implements the image stream hashing method developed and validated in the aforementioned study,\n")
    report_file.write("incorporating the recommended error mitigation techniques.\n\n")
    report_file.write("=============================================\n")
    report_file.write("The script conducted a test of two images stream hashes and compared them for similarity.\n\n")
    report_file.write("The testing hypothesis:\n\n")
    report_file.write("Null (Ho) - Image streams are similar.\n")
    report_file.write("Alternative (Ha) - Image streams are not similar.\n\n")
    report_file.write("=============================================\n")
    report_file.write("Preprocessing\n")
    report_file.write("=============================================\n\n")

# Image stream analysis began
print("Image stream analysis began...\n")

# Prompt the user to select the reference file
print("Loading reference and questioned files...")
root = tk.Tk()
root.withdraw()  # Hide the root window
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

# Check if the user selected a reference file
if ref_full_file_path == '':
    print('User canceled reference file selection')
    with open(report_file_path, 'a') as report_file:
        report_file.write('User canceled reference file selection\n')
else:
    # Process reference file
    ref_file_name = os.path.basename(ref_full_file_path)
    ref_file_size = os.path.getsize(ref_full_file_path)
    
    with open(report_file_path, 'a') as report_file:
        report_file.write("Reference File\n")
        report_file.write("------------------------------------\n")
        report_file.write(f"File Name: {ref_file_name}\n")
        report_file.write(f"File Size: {ref_file_size} bytes\n")
    
    ps_command_md5_ref = f'Get-FileHash "{ref_full_file_path}" -Algorithm MD5 | Select-Object -ExpandProperty Hash'
    ps_command_sha1_ref = f'Get-FileHash "{ref_full_file_path}" -Algorithm SHA1 | Select-Object -ExpandProperty Hash'
    ps_command_sha256_ref = f'Get-FileHash "{ref_full_file_path}" -Algorithm SHA256 | Select-Object -ExpandProperty Hash'
    
    result_md5_ref = subprocess.run(['pwsh', '-Command', ps_command_md5_ref], capture_output=True, text=True)
    result_sha1_ref = subprocess.run(['pwsh', '-Command', ps_command_sha1_ref], capture_output=True, text=True)
    result_sha256_ref = subprocess.run(['pwsh', '-Command', ps_command_sha256_ref], capture_output=True, text=True)
    
    with open(report_file_path, 'a') as report_file:
        if result_md5_ref.returncode == 0:
            report_file.write(f"File hash (MD5): {result_md5_ref.stdout.strip()}\n")
        else:
            report_file.write(f"Error computing MD5 hash: {result_md5_ref.stderr.strip()}\n")
        
        if result_sha1_ref.returncode == 0:
            report_file.write(f"File hash (SHA-1): {result_sha1_ref.stdout.strip()}\n")
        else:
            report_file.write(f"Error computing SHA-1 hash: {result_sha1_ref.stderr.strip()}\n")
        
        if result_sha256_ref.returncode == 0:
            report_file.write(f"File hash (SHA-256): {result_sha256_ref.stdout.strip()}\n")
        else:
            report_file.write(f"Error computing SHA-256 hash: {result_sha256_ref.stderr.strip()}\n")

    # Prompt the user to select the questioned file
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

    # Check if the user selected a questioned file
    if ques_full_file_path == '':
        print('User canceled questioned file selection')
        with open(report_file_path, 'a') as report_file:
            report_file.write('\nUser canceled questioned file selection\n')
    else:
        # Process questioned file
        ques_file_name = os.path.basename(ques_full_file_path)
        ques_file_size = os.path.getsize(ques_full_file_path)
        
        with open(report_file_path, 'a') as report_file:
            report_file.write("\nQuestioned File\n")
            report_file.write("------------------------------------\n")
            report_file.write(f"File Name: {ques_file_name}\n")
            report_file.write(f"File Size: {ques_file_size} bytes\n")
        
        ps_command_md5_ques = f'Get-FileHash "{ques_full_file_path}" -Algorithm MD5 | Select-Object -ExpandProperty Hash'
        ps_command_sha1_ques = f'Get-FileHash "{ques_full_file_path}" -Algorithm SHA1 | Select-Object -ExpandProperty Hash'
        ps_command_sha256_ques = f'Get-FileHash "{ques_full_file_path}" -Algorithm SHA256 | Select-Object -ExpandProperty Hash'
        
        result_md5_ques = subprocess.run(['pwsh', '-Command', ps_command_md5_ques], capture_output=True, text=True)
        result_sha1_ques = subprocess.run(['pwsh', '-Command', ps_command_sha1_ques], capture_output=True, text=True)
        result_sha256_ques = subprocess.run(['pwsh', '-Command', ps_command_sha256_ques], capture_output=True, text=True)
        
        with open(report_file_path, 'a') as report_file:
            if result_md5_ques.returncode == 0:
                report_file.write(f"File hash (MD5): {result_md5_ques.stdout.strip()}\n")
            else:
                report_file.write(f"Error computing MD5 hash: {result_md5_ques.stderr.strip()}\n")
            
            if result_sha1_ques.returncode == 0:
                report_file.write(f"File hash (SHA-1): {result_sha1_ques.stdout.strip()}\n")
            else:
                report_file.write(f"Error computing SHA-1 hash: {result_sha1_ques.stderr.strip()}\n")
            
            if result_sha256_ques.returncode == 0:
                report_file.write(f"File hash (SHA-256): {result_sha256_ques.stdout.strip()}\n")
            else:
                report_file.write(f"Error computing SHA-256 hash: {result_sha256_ques.stderr.strip()}\n")
                
        # Test files loaded
        print("Test files loaded successfully.\n")

        with open(report_file_path, 'a') as report_file:
            report_file.write("\n=============================================\n")
            report_file.write("Image Stream Analysis\n")
            report_file.write("=============================================\n\n")

            # Generate stream hash for reference file
            ref_streamhash_path = os.path.join(analysis_folder, "ref_streamhash.sha256")
            ffmpeg_command_ref = f'ffmpeg -i "{ref_full_file_path}" -f streamhash - > "{ref_streamhash_path}"'
            
            # Printing stream hash generation messages
            print("Generating stream hash for reference file...")
            result_ffmpeg_ref = subprocess.run(ffmpeg_command_ref, shell=True, capture_output=True, text=True)
            
            if result_ffmpeg_ref.returncode == 0:
                try:
                    with open(ref_streamhash_path, 'r') as streamhash_file:
                        stream_hash_ref = streamhash_file.read().strip()
                    report_file.write("Stream hash for reference file:\n")
                    report_file.write("------------------------------------\n")
                    report_file.write(f"{stream_hash_ref}\n\n")
                    print("Stream hash for reference file generated successfully.\n")
                except:
                    report_file.write("Error reading stream hash file for reference file\n\n")
                    stream_hash_ref = None
                    print("Error reading stream hash file for reference file.\n")
            else:
                report_file.write("Error generating stream hash for reference file\n\n")
                stream_hash_ref = None
                print("Error generating stream hash for reference file.\n")

            # Generate stream hash for questioned file
            ques_streamhash_path = os.path.join(analysis_folder, "ques_streamhash.sha256")
            ffmpeg_command_ques = f'ffmpeg -i "{ques_full_file_path}" -f streamhash - > "{ques_streamhash_path}"'
            
            # Printing stream hash generation messages
            print("Generating stream hash for questioned file...")
            result_ffmpeg_ques = subprocess.run(ffmpeg_command_ques, shell=True, capture_output=True, text=True)
            
            if result_ffmpeg_ques.returncode == 0:
                try:
                    with open(ques_streamhash_path, 'r') as streamhash_file:
                        stream_hash_ques = streamhash_file.read().strip()
                    report_file.write("Stream hash for questioned file:\n")
                    report_file.write("------------------------------------\n")
                    report_file.write(f"{stream_hash_ques}\n\n")
                    print("Stream hash for questioned file generated successfully.\n")
                except:
                    report_file.write("Error reading stream hash file for questioned file\n\n")
                    stream_hash_ques = None
                    print("Error reading stream hash file for questioned file.\n")
            else:
                report_file.write("Error generating stream hash for questioned file\n\n")
                stream_hash_ques = None
                print("Error generating stream hash for questioned file.\n")

            # Comparison Analysis
            report_file.write("------------------------------------\n")
            report_file.write("Comparison Analysis Finding:\n\n")

            if stream_hash_ref is not None and stream_hash_ques is not None:
                if stream_hash_ref == stream_hash_ques:
                    report_file.write("Image streams are similar - We fail to reject the Null (Ho) hypothesis.\n")
                    print("Image streams are similar.\n")
                else:
                    report_file.write("Image streams are not similar - We reject the Null (Ho) hypothesis and accept the Alternative (Ha) hypothesis.\n")
                    print("Image streams are not similar.\n")
            else:
                report_file.write("Unable to perform comparison due to errors in generating or reading stream hashes.\n")
                print("Unable to perform comparison due to errors in generating or reading stream hashes.\n")

            # Image Stream hashing completed
            print("Image Stream hashing completed.\n")

            # Conclusion section
            report_file.write("\n=============================================\n")
            report_file.write("Conclusion\n")
            report_file.write("=============================================\n\n")
            report_file.write("The forensic analysis conducted on the image streams of the reference file and the questioned file involved computing the SHA256 hash values for both files.\n\n")

            if stream_hash_ref is not None and stream_hash_ques is not None:
                if stream_hash_ref == stream_hash_ques:
                    report_file.write("Image streams are similar - We fail to reject the Null (Ho) hypothesis:\n")
                    report_file.write("   - The computed hash values for the reference and questioned files are identical. ")
                    report_file.write("Therefore, the data suggests that the image streams of the two files are similar. ")
                    report_file.write("Consequently, we fail to reject the Null (Ho) hypothesis, indicating no significant ")
                    report_file.write("difference between the image streams.\n")
                else:
                    report_file.write("Image streams are not similar - We reject the Null (Ho) hypothesis and accept the Alternative (Ha) hypothesis:\n")
                    report_file.write("   - The computed hash values for the reference and questioned files differ. ")
                    report_file.write("The analysis indicates that the image streams are not similar. ")
                    report_file.write("In this case, we reject the Null (Ho) hypothesis and accept the Alternative (Ha) hypothesis, ")
                    report_file.write("signifying a significant difference between the image streams.\n")
            else:
                report_file.write("Unable to reach a conclusion due to errors in generating or reading stream hashes.\n")

            # Add Caveat
            report_file.write("\nCaveat (Control of Method Operations):\n\n")
            report_file.write("It is important to note that the effective use of the image stream hashing method in forensic science requires\n")
            report_file.write("the implementation of error mitigation techniques. These techniques are detailed in the image stream control\n")
            report_file.write("of method operations script (control_methods.py). To obtain a decision on whether the potential for error in\n")
            report_file.write("image stream hashing has been mitigated, or if alternative methods are recommended, users must ensure they\n")
            report_file.write("incorporate these error mitigation practices.\n\n")
            report_file.write("In a validation study [2], it was concluded that examiners could use the image stream hashing method for\n")
            report_file.write("forensic science only by adhering to the proposed standard control of method operations.\n\n")

            # Add References
            report_file.write("=============================================\n")
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

print(f"See analysis report in folder IMG-Stream-Hash-Comparison-Analysis\n")

# Image stream analysis finished
print("Image stream analysis finished.\n")
