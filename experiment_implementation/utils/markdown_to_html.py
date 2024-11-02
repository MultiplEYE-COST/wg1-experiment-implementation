import argparse
from pathlib import Path

from markdown_it import MarkdownIt

REPO_ROO = Path(__file__).parent.parent.parent


def markdown_to_html(md_file_path: str):
    """
    Convert a markdown file to a PDF file.
    """

    full_path = REPO_ROO / md_file_path

    with open(full_path, 'r', encoding='utf8') as md_file:
        md_content = md_file.read()

    md_convertor = MarkdownIt()

    md_content = md_content.replace('.md', '.html')
    md_content = md_content.replace('markdown', 'html')

    html_content = md_convertor.render(md_content)

    stem = full_path.stem

    if stem == 'README':
        results_path = REPO_ROO / stem

        with open(f'{results_path}.html', 'w', encoding='utf8') as html_file:
            html_file.write(html_content)

    else:
        results_path = REPO_ROO / 'guidelines' / 'html' / stem

        with open(f'{results_path}.html', 'w', encoding='utf8') as html_file:
            html_file.write(html_content)


if __name__ == '__main__':

    # add very simple parser for filename
    parser = argparse.ArgumentParser(description='Convert markdown file to PDF file.')

    parser.add_argument('md_file_path', type=str, help='Path to the markdown file.')

    args = parser.parse_args()

    markdown_to_html(args.md_file_path)
