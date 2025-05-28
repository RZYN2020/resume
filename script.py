import markdown
import argparse
import os
import sys
import traceback
import logging
import asyncio
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('pdf_generation.log'),
                        logging.StreamHandler(sys.stdout) # Also output to console
                    ])

class MyHTMLConverter:
    def convert(self, text):
        html = markdown.markdown(text, extensions=['fenced_code', 'tables', 'attr_list'])
        return html

def generate_pdf_from_html(html_file_path, pdf_output_path):
    logging.info(f"Attempting to generate PDF from {html_file_path} to {pdf_output_path}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Navigate to the local HTML file
            page.goto(f"file:///{os.path.abspath(html_file_path)}")
            
            # Generate PDF with Chrome-like print settings
            page.pdf(path=pdf_output_path, 
                     format="A4", 
                     print_background=True, 
                     margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"})
            
            browser.close()
            logging.info(f"PDF generated successfully: {pdf_output_path}")
            print(f"PDF resume generated: {pdf_output_path}")
    except Exception as e:
        logging.error(f"Failed to generate PDF: {e}", exc_info=True)
        print(f"Error generating PDF: {e}")
        sys.exit(1)

parser = argparse.ArgumentParser(description="Convert Markdown resume to HTML and optionally PDF.")
parser.add_argument('--path', type=str, help='Path to the Markdown resume file', default="resume_zh.md")
parser.add_argument('--output', type=str, help='Output HTML file path', default="resume.html")
parser.add_argument('--pdf', action='store_true', help='Generate PDF from the HTML output')
parser.add_argument('--pdf_output', type=str, help='Output PDF file path', default="resume.pdf")
args = parser.parse_args()

try:
    # Read Markdown content
    with open(args.path, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    converter = MyHTMLConverter()
    html_content = converter.convert(markdown_text)

    # Define the CSS file path
    css_file_path = "styles.css"

    # Check if CSS file exists
    if not os.path.exists(css_file_path):
        logging.error(f"Error: CSS file '{css_file_path}' not found. Please ensure it's in the same directory.")
        sys.exit(1)

    # Construct the final HTML output, including the photo placeholder
    final_html_output = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
    <link rel="stylesheet" type="text/css" href="{css_file_path}">
</head>
<body>
    <div class="resume-container">
        <div class="resume-content">
            <div class="profile-photo-container">
                <img src="./photo.jpg" alt="Profile Photo" class="profile-photo">
            </div>
            {html_content}
        </div>
    </div>
</body>
</html>
'''

    # Write HTML to output file
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(final_html_output)
    print(f"HTML resume generated: {args.output}")
    logging.info(f"HTML resume generated successfully at {args.output}")

    # Generate PDF if --pdf argument is present
    if args.pdf:
        generate_pdf_from_html(args.output, args.pdf_output)

except FileNotFoundError:
    logging.error(f"Error: The Markdown file '{args.path}' was not found.")
    sys.exit(1)
except Exception as e:
    logging.critical(f"An unexpected error occurred: {e}", exc_info=True)
    sys.exit(1)