#!/usr/bin/env python3
"""
Generate PDF report from markdown with embedded images
"""

import os
import markdown2
from weasyprint import HTML, CSS
from pathlib import Path

def generate_pdf_report(markdown_file, output_file):
    """
    Convert markdown report to PDF with proper styling
    
    Args:
        markdown_file: Path to markdown report
        output_file: Path to output PDF
    """
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        md_content,
        extras=['tables', 'fenced-code-blocks', 'math']
    )
    
    # Replace relative image paths to work with file:// URLs
    base_dir = Path(markdown_file).parent
    html_content = html_content.replace(
        'src="results/visualizations/',
        f'src="file://{base_dir}/results/visualizations/'
    )
    
    # Wrap with proper HTML structure and styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hong Kong Stock Market Trend Prediction Analysis</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.8;
                color: #333;
                background-color: #fff;
                padding: 40px;
                max-width: 1000px;
                margin: 0 auto;
            }}
            
            h1 {{
                color: #0066cc;
                border-bottom: 4px solid #0066cc;
                padding-bottom: 15px;
                margin: 40px 0 20px 0;
                font-size: 28px;
                page-break-after: avoid;
            }}
            
            h2 {{
                color: #0076ff;
                border-bottom: 2px solid #0066cc;
                padding-bottom: 8px;
                margin: 30px 0 15px 0;
                font-size: 22px;
                page-break-after: avoid;
            }}
            
            h3 {{
                color: #003d99;
                margin: 20px 0 10px 0;
                font-size: 18px;
                page-break-after: avoid;
            }}
            
            h4, h5, h6 {{
                color: #333;
                margin: 15px 0 8px 0;
                page-break-after: avoid;
            }}
            
            p {{
                margin: 10px 0;
                text-align: justify;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                page-break-inside: avoid;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            
            td, th {{
                border: 1px solid #ddd;
                padding: 12px 15px;
                text-align: left;
            }}
            
            th {{
                background-color: #0066cc;
                color: white;
                font-weight: 600;
            }}
            
            tr:nth-child(even) {{
                background-color: #f5f7fa;
            }}
            
            tr:hover {{
                background-color: #e3f2fd;
            }}
            
            img {{
                max-width: 100%;
                height: auto;
                margin: 25px 0;
                border: 1px solid #ddd;
                page-break-inside: avoid;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }}
            
            code {{
                background-color: #f5f5f5;
                padding: 3px 8px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }}
            
            pre {{
                background-color: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                margin: 15px 0;
                border-left: 4px solid #0066cc;
                page-break-inside: avoid;
            }}
            
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
            
            ul, ol {{
                margin: 15px 0 15px 30px;
            }}
            
            li {{
                margin: 8px 0;
            }}
            
            blockquote {{
                border-left: 4px solid #0066cc;
                margin: 15px 0;
                padding-left: 15px;
                color: #666;
            }}
            
            .page-break {{
                page-break-after: always;
            }}
            
            hr {{
                border: none;
                border-top: 2px solid #0066cc;
                margin: 30px 0;
            }}
            
            em {{
                color: #666;
                font-style: italic;
            }}
            
            strong {{
                color: #000;
                font-weight: 600;
            }}
            
            @media print {{
                body {{
                    padding: 20px;
                }}
                h1, h2, h3 {{
                    page-break-after: avoid;
                }}
                table {{
                    page-break-inside: avoid;
                }}
                img {{
                    page-break-inside: avoid;
                }}
            }}
        </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    HTML(string=full_html).write_pdf(output_file)
    
    return output_file


if __name__ == '__main__':
    markdown_file = '/workspaces/Neo-page/advanced DA project/report.md'
    output_file = '/workspaces/Neo-page/advanced DA project/Stock_Price_Prediction_Report.pdf'
    
    if os.path.exists(markdown_file):
        result = generate_pdf_report(markdown_file, output_file)
        file_size = os.path.getsize(result) / 1024  # Convert to KB
        print(f"✅ PDF generated successfully!")
        print(f"📄 Output: {result}")
        print(f"📊 File size: {file_size:.2f} KB")
    else:
        print(f"❌ Markdown file not found: {markdown_file}")
