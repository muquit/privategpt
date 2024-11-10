#!/usr/bin/env python3

########################################################################
# PDF to Text Converter
# Part of https://github.com/muquit/privategpt
#
# usage: pdf2txt.py [-h] input_pdf output_txt
#
# Implemented by Claude AI (Anthropic, 2024)
# Nov-10-2024 
########################################################################

import fitz  # PyMuPDF
import argparse
import sys

def convert_pdf_to_text(pdf_path, output_path):
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        
        # Extract text
        full_text = ""
        for page in doc:
            full_text += page.get_text()
            
        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
            
        doc.close()
        print(f"Successfully converted {pdf_path} to {output_path}")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert PDF to text file')
    parser.add_argument('input_pdf', help='Path to the input PDF file')
    parser.add_argument('output_txt', help='Path for the output text file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert PDF to text
    convert_pdf_to_text(args.input_pdf, args.output_txt)

if __name__ == "__main__":
    main()
