#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ===========================================================================
#
# Script Name: control_methods.py
#
# Script Written by Gregory S. Wales, DFS
# Date: February 26, 2025
# Image Comparison Control Methods Analysis for Digital Image Forensics
# - script v1.4
# Email: media4n6@gmail.com
# GITHUB: ronin4n6labs
#
# ---------------------------------------------------------------------------
#
# Purpose of this script:
# This script implements standard control methods for image stream hashing to mitigate errors
# in method operations from a method validation study.
# It checks image compatibility for image comparison techniques.
#
# Applications of this image format analysis include:
# 1. Determining if image stream hashing can be performed
# 2. Recommending alternative methods if image stream hashing is not suitable
# 3. Preventing false positive and false negative errors in image comparison
#
# Process:
# 1. Select a reference image file.
# 2. Select a questioned image file.
# 3. Analyze the file format, dimensions, color space, and bit depth of both images.
# 4. Generate a report indicating compatibility and any discrepancies found.
#
# The script analyzes:
# 1. File Format
# 2. Image Dimensions
# 3. Color Space
# 4. Bit Depth
#
# It is designed to help determine if a potential for errors exist from:
# 1. False Negatives
# 2. False Positives
#
# Requirements:
# - Pillow (PIL)
# - tkinter
# - subprocess
# - imghdr
# - os
#
# The script produces a detailed report in a text file.
#
# Error handling includes checks for file selection and format identification.
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
#
# Please reference The MIT License file included with this script.
# ===========================================================================


import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import imghdr
from PIL import Image
from PIL import TiffImagePlugin

class ControlMethods:
    """
    Implements standard control methods for image stream hashing to mitigate errors
    in method operations from a method validation study.
    """

    def __init__(self, analysis_folder="IMG-Comparison-Control-Methods-Analysis", report_file_name="IMG-Comparison-Control-Methods-Analysis-Report.txt"):
        """
        Initializes the ControlMethods class with the analysis folder and report file.
        """
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.analysis_folder = os.path.join(self.script_dir, analysis_folder)
        os.makedirs(self.analysis_folder, exist_ok=True)
        self.report_file_path = os.path.join(self.analysis_folder, report_file_name)
        self.create_report_header()
        print("Image comparison control method analysis began...\n")

    def create_report_header(self):
        """
        Writes the initial content to the report file.
        """
        with open(self.report_file_path, 'w') as report_file:
            report_file.write("Image Comparison Control Methods Analysis Report\n")
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
            report_file.write("This script implements the standard control methods developed and validated in the aforementioned study,\n")
            report_file.write("incorporating the recommended error mitigation techniques.\n\n")
            report_file.write("=============================================\n")
            report_file.write("Preprocessing\n")
            report_file.write("=============================================\n\n")

    def select_file(self, title, file_types):
        """
        Opens a file dialog and returns the selected file path.
        """
        print("Loading reference and questioned files...")
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(title=title, filetypes=file_types)
        if file_path == '':
            print('User canceled file selection')
            self.write_to_report('User canceled file selection\n')
            return None
        return file_path

    def get_file_hash(self, file_path, algorithm):
        """
        Computes the hash of the file using the specified algorithm.
        """
        ps_command = f'Get-FileHash "{file_path}" -Algorithm {algorithm} | Select-Object -ExpandProperty Hash'
        result = subprocess.run(['pwsh', '-Command', ps_command], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            self.write_to_report(f"Error computing {algorithm} hash: {result.stderr.strip()}\n")
            return None

    def process_file(self, file_path, file_type):
        """
        Processes the selected file, retrieves file information, and computes its hashes.
        """
        if file_path:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            self.write_to_report(f"{file_type} File\n")
            self.write_to_report("------------------------------------\n")
            self.write_to_report(f"File Name: {file_name}\n")
            self.write_to_report(f"File Size: {file_size} bytes\n")
            
            md5_hash = self.get_file_hash(file_path, 'MD5')
            sha1_hash = self.get_file_hash(file_path, 'SHA1')
            sha256_hash = self.get_file_hash(file_path, 'SHA256')
            
            if md5_hash:
                self.write_to_report(f"File hash (MD5): {md5_hash}\n")
            if sha1_hash:
                self.write_to_report(f"File hash (SHA-1): {sha1_hash}\n")
            if sha256_hash:
                self.write_to_report(f"File hash (SHA-256): {sha256_hash}\n")

    def write_to_report(self, text):
        """
        Writes the given text to the report file.
        """
        with open(self.report_file_path, 'a') as report_file:
            report_file.write(text)

    def analyze_file_format(self, file_path):
        """
        Analyzes a file to determine its format and description.
        """
        try:
            file_format = imghdr.what(file_path)
            if file_format:
                description = self.get_format_description(file_format)
                return file_format.upper(), "0x0", description
            return "Unknown", "N/A", "Unknown file format"
        except Exception as e:
            return "Error", "N/A", f"Error analyzing file: {str(e)}"

    def get_format_offset(self, file_path):
        """
        Find the hex offset of the detected file type's header in the file.
        """
        try:
            with open(file_path, 'rb') as f:
                header = f.read(2048)
                detected_format = self.analyze_file_format(file_path)[0]
                if "JPEG" in detected_format.upper():
                    offset = header.find(b'\xFF\xD8\xFF\xE0')
                    if offset != -1:
                        return detected_format, hex(offset), "JFIF"
                offset = header.find(detected_format.encode())
                if offset != -1:
                    return detected_format, hex(offset), detected_format
                else:
                    return detected_format, "Not Found", "Not Found"
        except Exception as e:
            return "Unknown", f"Error: {str(e)}", "Error"

    def get_format_description(self, file_format):
        """
        Provides a description for a given file format.
        """
        descriptions = {
            'jpeg': 'JPEG image file',
            'png': 'PNG image file',
            'bmp': 'BMP image file',
            'tiff': 'TIFF image file',
            'jp2': 'JPEG 2000 image file',
            'jpx': 'JPEG 2000 image file'
        }
        return descriptions.get(file_format.lower(), 'Unknown image file format')

    def get_image_dimensions(self, image_path):
        """
        Retrieves the dimensions (width, height) of an image.
        """
        try:
            img = Image.open(image_path)
            width, height = img.size
            return width, height
        except Exception as e:
            print(f"Error getting dimensions for {image_path}: {e}")
            return None, None

    def compare_image_dimensions(self, ref_dims, ques_dims):
        """
        Compares the dimensions of two images.
        """
        if ref_dims == (None, None) or ques_dims == (None, None):
            return False, None, None
        dimension_match = ref_dims == ques_dims
        height_diff = abs(ref_dims[1] - ques_dims[1])
        width_diff = abs(ref_dims[0] - ques_dims[0])
        return dimension_match, height_diff, width_diff

    def get_image_color_space(self, image_path):
        """
        Retrieves the color space of an image.
        """
        try:
            img = Image.open(image_path)
            return img.mode
        except Exception as e:
            print(f"Error getting color space for {image_path}: {e}")
            return None

    def _read_bmp_bit_depth(self, file_path):
        """
        Reads the bit depth directly from a BMP file's BITMAPINFOHEADER.
        """
        try:
            with open(file_path, 'rb') as f:
                f.seek(28)  # Offset 28 is biBitCount in BITMAPINFOHEADER
                bit_count = int.from_bytes(f.read(2), 'little')
                return bit_count
        except Exception as e:
            print(f"Error reading BMP header for {file_path}: {e}")
            return None

    def get_image_bit_depth(self, image_path):
        """
        Retrieves the total bit depth of an image across all channels.
        """
        try:
            with Image.open(image_path) as img:
                # Handle BMP files by reading the header directly
                if img.format == 'BMP':
                    bit_depth = self._read_bmp_bit_depth(image_path)
                    if bit_depth is not None:
                        return bit_depth
                    # Fallback if header read fails
                    if 'bits' in img.info:
                        return img.info['bits']
                    mode_to_bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32}
                    return mode_to_bpp.get(img.mode, 16)  # Default to 16 if unknown
                
                # Handle TIFF files
                elif img.format == 'TIFF':
                    bits_per_sample = img.tag_v2.get(258, [8])
                    samples_per_pixel = img.tag_v2.get(277, 1)
                    if isinstance(bits_per_sample, (list, tuple)):
                        total_bits = sum(bits_per_sample)
                    else:
                        total_bits = bits_per_sample * samples_per_pixel
                    return total_bits
                
                # Default for other formats
                mode_to_bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32, 'CMYK': 32}
                return mode_to_bpp.get(img.mode, None)
        except Exception as e:
            print(f"Error getting bit depth for {image_path}: {e}")
            return None

    def check_image_compatibility(self, ref_path, ques_path):
        """
        Checks the compatibility of two images based on file format, dimensions, color space, and bit depth.
        """
        results = {}

        # File Format Analysis
        ref_format, ref_offset, ref_description = self.get_format_offset(ref_path)
        ques_format, ques_offset, ques_description = self.get_format_offset(ques_path)
        format_match = ref_format == ques_format
        results['file_format'] = {
            'reference': ref_format,
            'reference_offset': ref_offset,
            'ref_description': ref_description,
            'questioned': ques_format,
            'questioned_offset': ques_offset,
            'ques_description': ques_description,
            'file_match': format_match
        }

        # Dimensional Analysis
        ref_dims = self.get_image_dimensions(ref_path)
        ques_dims = self.get_image_dimensions(ques_path)
        dimension_match, height_diff, width_diff = self.compare_image_dimensions(ref_dims, ques_dims)
        results['dimensions'] = {
            'reference': ref_dims,
            'questioned': ques_dims,
            'dimension_match': dimension_match,
            'height_diff': height_diff,
            'width_diff': width_diff
        }

        # Color Space Analysis
        ref_color_space = self.get_image_color_space(ref_path)
        ques_color_space = self.get_image_color_space(ques_path)
        color_space_match = ref_color_space == ques_color_space
        results['color_space'] = {
            'reference': ref_color_space,
            'questioned': ques_color_space,
            'color_space_match': color_space_match
        }

        # Bit Depth Analysis
        ref_bit_depth = self.get_image_bit_depth(ref_path)
        ques_bit_depth = self.get_image_bit_depth(ques_path)
        bit_depth_match = ref_bit_depth == ques_bit_depth
        results['bit_depth'] = {
            'reference': ref_bit_depth,
            'questioned': ques_bit_depth,
            'bit_depth_match': bit_depth_match
        }

        # Determine overall compatibility
        can_proceed = all([dimension_match, color_space_match, bit_depth_match, format_match])
        return results, dimension_match, color_space_match, bit_depth_match, format_match, format_match

    def write_bit_depth_analysis(self, results):
        self.write_to_report("Bit Depth Analysis:\n")
        ref_depth = results['bit_depth']['reference']
        ques_depth = results['bit_depth']['questioned']
        self.write_to_report(f"  Reference Bit Depth: {ref_depth} (total across all channels)\n")
        self.write_to_report(f"  Questioned Bit Depth: {ques_depth} (total across all channels)\n")
        self.write_to_report(f"  Bit Depths Match: {results['bit_depth']['bit_depth_match']}\n\n")

    def run_analysis(self):
        """
        Runs the image comparison control method analysis.
        """
        image_file_types = [
            ('Image files', '*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.jp2 *.jpx'),
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('BMP files', '*.bmp'),
            ('TIFF files', '*.tiff *.tif'),
            ('JPEG 2000 files', '*.jp2 *.jpx'),
            ('All files', '*.*')
        ]

        print("Beginning control methods testing...")
        ref_full_file_path = self.select_file('Select the reference file', image_file_types)
        ques_full_file_path = self.select_file('Select the questioned file', image_file_types)

        if not ref_full_file_path or not ques_full_file_path:
            print("Both reference and questioned files must be selected to proceed.")
            return

        self.process_file(ref_full_file_path, "Reference")
        self.process_file(ques_full_file_path, "Questioned")

        self.write_to_report("\n=============================================\n")
        self.write_to_report("Control of Methods Analysis\n")
        self.write_to_report("=============================================\n\n")

        compatibility_results, dimension_match, color_space_match, bit_depth_match, format_match, _ = self.check_image_compatibility(ref_full_file_path, ques_full_file_path)

        self.write_to_report("File Format Compatibility Analysis:\n")
        self.write_to_report(f"  Reference File Format: {compatibility_results['file_format']['reference']}\n")
        self.write_to_report(f"  Questioned File Format: {compatibility_results['file_format']['questioned']}\n")
        self.write_to_report(f"  File Formats Match: {compatibility_results['file_format']['file_match']}\n\n")

        self.write_to_report("------------------------------------\n")

        self.write_to_report("Dimensional Analysis:\n")
        self.write_to_report(f"  Reference Dimensions: {compatibility_results['dimensions']['reference']}\n")
        self.write_to_report(f"  Questioned Dimensions: {compatibility_results['dimensions']['questioned']}\n")
        self.write_to_report(f"  Dimensions Match: {compatibility_results['dimensions']['dimension_match']}\n")
        self.write_to_report(f"  Height Difference: {compatibility_results['dimensions']['height_diff']}\n")
        self.write_to_report(f"  Width Difference: {compatibility_results['dimensions']['width_diff']}\n\n")

        self.write_to_report("------------------------------------\n")

        self.write_to_report("Color Space Analysis:\n")
        self.write_to_report(f"  Reference Color Space: {compatibility_results['color_space']['reference']}\n")
        self.write_to_report(f"  Questioned Color Space: {compatibility_results['color_space']['questioned']}\n")
        self.write_to_report(f"  Color Spaces Match: {compatibility_results['color_space']['color_space_match']}\n\n")

        self.write_to_report("------------------------------------\n")

        self.write_bit_depth_analysis(compatibility_results)

        self.write_to_report("\n=============================================\n")
        self.write_to_report("Conclusion\n")
        self.write_to_report("=============================================\n\n")
        self.write_to_report("The analysis tested the reference file and the questioned file against known potential causes of errors in image stream hash comparison analysis.\n\n")
        self.write_to_report("The test used standard controls of method operations and determined ")

        if not dimension_match:
            self.write_to_report("a critical failure: the images cannot be compared from a forensic perspective using image stream hashing or other image quality assessment methods (image difference/subtraction or correlation analysis).\n")
        elif not color_space_match or not bit_depth_match or not format_match:
            self.write_to_report("that image stream hashing method cannot be used, but alternative image quality assessment methods (image difference/subtraction or correlation analysis) are recommended.\n")
        else:
            self.write_to_report("that the image stream hashing method can be used, and image quality assessment methods (image difference/subtraction or correlation analysis) are potential verification methods to support image stream hashing findings.\n")

        self.write_to_report("\nCaveat (Control of Method Operations):\n\n")
        self.write_to_report("It is important to note that the effective use of the image stream hashing method in forensic science requires\n")
        self.write_to_report("the implementation of error mitigation techniques. These techniques are detailed in the image stream control\n")
        self.write_to_report("of method operations script (control_methods.py). To obtain a decision on whether the potential for error in\n")
        self.write_to_report("image stream hashing has been mitigated, or if alternative methods are recommended, users must ensure they\n")
        self.write_to_report("incorporate these error mitigation practices.\n\n")
        self.write_to_report("In a validation study [2], it was concluded that examiners could use the image stream hashing method for\n")
        self.write_to_report("forensic science only by adhering to the proposed standard control of method operations.\n\n")

        self.write_to_report("=============================================\n")
        self.write_to_report("References\n")
        self.write_to_report("=============================================\n\n")
        self.write_to_report("[1] Wales GS, Smith JM, Lacey DS, Grigoras C. \n")
        self.write_to_report("    Multimedia stream hashing: A forensic method for \n")
        self.write_to_report("    content verification. J Forensic Sci. 2023;68:289–300. https://\n")
        self.write_to_report("    doi.org/10.1111/1556-4029.15148\n\n")
        self.write_to_report("[2] Wales GS.  Validation of image stream hashing: A forensic \n")
        self.write_to_report("    method for content verification.  J Forensic Sci.\n")
        self.write_to_report("    2024 ; 69 : 515 – 28 .  https://doi.org/10.1111/1556-\n")
        self.write_to_report("    4029.15432\n")

        print("Control methods testing completed.")
        print(f"See the '{self.analysis_folder}' folder for the analysis report.")

if __name__ == "__main__":
    control_methods = ControlMethods()
    image_file_types = [
        ('Image files', '*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.jp2 *.jpx'),
        ('PNG files', '*.png'),
        ('JPEG files', '*.jpg *.jpeg'),
        ('BMP files', '*.bmp'),
        ('TIFF files', '*.tiff *.tif'),
        ('JPEG 2000 files', '*.jp2 *.jpx'),
        ('All files', '*.*')
    ]
    control_methods.run_analysis()
