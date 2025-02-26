# Forensic Image Comparison Tool

[![Version](https://img.shields.io/badge/version-1.4-blue)](https://github.com/ronin4n6labs/IMG-Comparison-Tool-Python/releases/tag/v1.4)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-yellow)](https://www.python.org/)

## Overview

The Forensic Image Comparison Tool is a Python script designed for basic level Image Quality Assessment (IQA) forensic analysis of digital images. It performs pixel-by-pixel comparisons between a reference image and a questioned image, identifying similarities and differences using fundamental image processing techniques. This tool provides valuable insights for various applications, including image authentication, detection of image alterations, and forensic image comparison. It serves as a robust starting point for digital image forensics, offering both quantitative and visual representations of image differences. The tool generates detailed reports and visual outputs, such as image difference visualizations, to aid in forensic analysis.

The development of this tool was informed by the validation study and methodology described in Wales, G. S. Validation of image stream hashing: A forensic method for content verification. J Forensic Sci. 2024; 69: 515–28. https://doi.org/10.1111/1556-4029.15432. This study aimed to ensure the method's reliability and admissibility under Daubert and Federal Rule of Evidence (FRE) 702 standards, emphasizing peer review, testability, and error mitigation.

## Legal and Scientific Validation

The Forensic Image Comparison Tool was developed with considerations for Daubert standards [1] and Federal Rule of Evidence (FRE) 702 requirements [2]. The underlying methodology has been peer-reviewed and published, ensuring that the tool meets standards for reliability and admissibility in legal proceedings. The tool's design incorporates error mitigation techniques and provides detailed outputs to assist in understanding the evidence.

## Key Features

- Performs dimensional analysis of images.
- Analyzes color spaces for compatibility.
- Computes absolute differences between images.
- Generates a detailed report with findings.
- Creates visual representations of image differences.
- Supports multiple image formats: PNG, JPG, JPEG, BMP, TIFF, TIF, JP2, JPX.
- Generates detailed reports with quantitative conclusions for each analysis method.
- Incorporates hypothesis testing in the analysis process.
- Provides clear interpretation of results based on established similarity scales (for correlation analysis).

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Installation

1. Clone this repository:

```bash
git clone https://github.com/ronin4n6labs/IMG-Comparison-Tool-Python.git
cd IMG-Comparison-Tool-Python
```

2. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Analysis Methods

This tool suite includes four different analysis methods:

1. Control Methods (`control_methods.py`): Assesses image compatibility for comparison, including file format, dimensions, color space, and bit depth.
2. Stream Hash Comparison (`IMG-Stream-Hash-Comparison.py`): Compares SHA256 hash values of image streams to detect differences.
3. Subtraction Analysis (`IMG-Subtraction-Analysis.py`): Performs pixel-by-pixel comparison to quantify differences between images.
4. Correlation Analysis (`IMG-Correlation-Analysis.py`): Uses Pearson Correlation Coefficient to measure similarity between images.

Each method provides a unique perspective on image comparison, allowing for a comprehensive forensic analysis.

## Documentation

Each script generates a comprehensive report that includes:

- Preprocessing information: File names, sizes, and hash values (MD5, SHA-1, SHA-256) for both reference and questioned images.
- Analysis methodology: Description of the specific analysis technique used.
- Hypothesis testing: Clear statement of null and alternative hypotheses.
- Detailed analysis results: Quantitative measures specific to each method.
- Conclusion: Interpretation of results in relation to the hypotheses.
- References: Citations to relevant scientific literature supporting the methodology.

## Scripts Overview

This repository contains scripts that implement the image stream hashing method, incorporating recommended error mitigation techniques.

### `control_methods.py`

- **Description:** Implements standard control methods for image stream hashing to mitigate potential errors. Tests the dimensions, color space compatibility, and bit depth of two images, rendering a conclusion on the best method for overall image quality assessment comparisons.
- **Usage:** `python control_methods.py`
 - Follow the prompts to select the reference and questioned images for analysis.
- **Output:** Recommendations for the best image comparison method based on compatibility checks.

### `IMG-Stream-Hash-Comparison.py`

- **Description:** Performs image stream hashing if the color space and bit depth of the two images are compatible.
- **Usage:** `python IMG-Stream-Hash-Comparison.py`
 - Follow the prompts to select the reference and questioned images for analysis.
- **Output:** Hash comparison results for the two images.

### `IMG-Subtraction-Analysis.py`

- **Description:** Conducts image subtraction analysis with quantitative measurements when the color space or bit depth of the images are not compatible.
- **Usage:** `python IMG-Subtraction-Analysis.py`
 - Follow the prompts to select the reference and questioned images for analysis.
- **Output:** Subtraction analysis results and quantitative measurements.

### `IMG-Correlation-Analysis.py`

- **Description:** Performs correlation analysis using the Pearson Correlation Coefficient with quantitative measurements for image comparison.
- **Usage:** `python IMG-Correlation-Analysis.py`
 - Follow the prompts to select the reference and questioned images for analysis.
- **Output:** Correlation analysis results and quantitative measurements.

## Test Files

The repository includes test files for testing and analysis:

1. `Reference.jpg`: The reference image for comparison.
2. `Questioned-Match.jpg`: A questioned image that matches the reference.
3. `Questioned-Not-Match.jpg`: A questioned image that does not match the reference.

Use these files to test the script and understand its output in different scenarios.

## Applications

1. Image authentication
2. Detection of image alterations
3. Forensic image comparison
4. Content verification

## Limitations

- This tool is designed for basic forensic analysis and should not be considered a comprehensive forensic solution.
- Results may vary depending on image quality and the nature of alterations.
- The tool does not account for advanced image manipulation techniques.
- Users should interpret results in conjunction with other forensic methods and expert knowledge.
- The tool's outputs should be verified and corroborated by qualified forensic experts before use in legal proceedings.

## Methodology

This script is based on analysis methodology used in:

Wales, G. S. Validation of image stream hashing: A forensic method for content verification. J Forensic Sci. 2024; 69: 515–28. https://doi.org/10.1111/1556-4029.15432

## Citation

If you use this tool in your research or professional work, please cite it as follows:

Wales, G. S. (2025). Image Comparison Tool (Version 1.4) \[Computer software]. https://github.com/ronin4n6labs/IMG-Comparison-Tool-Python

## Author

Gregory S. Wales, DFS

Email: media4n6@gmail.com

GitHub: [Ronin4n6labs](https://github.com/ronin4n6labs)

## Version

1.4 (February 26, 2025)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

[1] Daubert v. Merrell Dow Pharmaceuticals, Inc., 509 U.S. 579 (1993).

[2] Federal Rule of Evidence 702, as amended December 1, 2023.
