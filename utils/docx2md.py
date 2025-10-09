import mammoth
from markdownify import markdownify as md


def docx_to_html(docx_path):
    try:
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html_content = result.value  # The generated HTML
            return html_content
    except Exception as e:
        print(f"Error converting DOCX to HTML: {e}")
        raise


def docx_to_markdown(docx_path, md_path="", verbose=False):
    try:
        # Convert DOCX to HTML
        if verbose:
            print(f"Converting '{docx_path}' to HTML...")
        html_content = docx_to_html(docx_path)

        # Convert HTML to Markdown
        if verbose:
            print(f"Converting HTML to Markdown...")
        md_content = md(html_content, strip=['img'], heading_style="ATX")

        # Save the Markdown content to a file
        if md_path != "":
            with open(md_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)
        if verbose:
            print(f"Markdown file saved to '{md_path}'")
        return md_content
    except Exception as e:
        print(f"Error converting DOCX to Markdown: {e}")
        raise

#
# # Example usage
# md_content = docx_to_markdown(os.path.join(os.getcwd(), '../uploads/7/hospital-doc-test.docx'))
# print(md_content)
# headers_to_split_on = [
#     ("#", "Header 1"),
#     ("##", "Header 2"),
#     ("###", "Header 3"),
# ]
# markdown_splitter = MarkdownHeaderTextSplitter(
#     headers_to_split_on=headers_to_split_on, strip_headers=False
# )
# md_header_splits = markdown_splitter.split_text(md_content)
# print([doc.page_content for doc in md_header_splits])
