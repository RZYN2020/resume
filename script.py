import markdown
import argparse

class MyHTMLConverter:
    def convert(self, text):
        html = markdown.markdown(text)
        return html

parser = argparse.ArgumentParser(description="Convert Markdown resume to HTML or PDF.")
parser.add_argument('--path', type=str, help='Path to the Markdown resume file', default="resume.md")
parser.add_argument('--output', type=str, help='Output file path', default="resume.html")
parser.add_argument('--theme', type=str, choices=['default', 'dark', 'compact'], default='default', help='Style theme (default, dark, compact)')
args = parser.parse_args()

with open(args.path, 'r', encoding='utf-8') as file:
    markdown_text = file.read()


converter = MyHTMLConverter()
html_content = converter.convert(markdown_text)


theme_classes = {
    'default': '',
    'dark': 'dark-theme',
    'compact': 'compact-theme'
}
body_class = theme_classes.get(args.theme, '')


html_content = f'''
<!DOCTYPE html>
  <html lang="en">
    <head><meta charset="UTF-8">
      <title>Resume</title>
      <link rel="stylesheet" type="text/css" href="styles.css">
    </head>
    <body class-"{body_class}">
      <div class="resume-container">
        <div class="resume-content">
          {html_content}
        </div>
      </div>
    </body>
  </html>
'''

with open(args.output, 'w', encoding='utf-8') as file:
    file.write(html_content)
print(f"HTML简历已生成：{args.output}")

