import pathlib, json

def dump_blogs(blogs):
    """ dump blogs
    dump the blogs datastructure in the appropriate directory """

    filename = '../src/routes/blog/blogs.json'

    with open(filename, 'w') as fn:
        json.dump(blogs, fn, sort_keys=True, indent=4)

def _header_markdown_parser(blog_data, html_line):
    """ header markdown parser
    parses header related markdown """

    markdown_to_html = {
        "#": "h1",
        "##": "h2",
        "###": "h3",
    }

    header_exists = False

    for markdown, html_tag in markdown_to_html.items():
        if html_line.startswith(f'{markdown} '):
            html_line = f'<{html_tag}>{html_line[len(markdown):].strip()}</{html_tag}>'
            header_exists = True
            break

    if header_exists:
        blog_data['data'].append({'type': html_tag, 'content': html_line.strip()})
    
    return header_exists

def _image_markdown_parser(blog_data, html_line):
    """ image markdown parser
    parses image related markdown """

    image_markdown = '!['
    image_exists = False

    if html_line.startswith(image_markdown):
        alternate_text = html_line.split('](')[0][2:]
        image_source = html_line.strip().split('](')[-1][:-1]
        html_line = f'<img alt="{alternate_text}" src="{image_source}">'
        blog_data['data'].append({'type': 'img', 'content': html_line.strip()})
        image_exists = True

    return image_exists

def _inline_markdown_parser(html_line):
    """ inline markdown parser
    parses inline styling related markdown """

    markdown_to_html = {
        "**": "b",
        "_": "i",
    }

    for markdown, html_tag in markdown_to_html.items():
        total_markdown_hits = html_line.count(markdown)

        if total_markdown_hits == 1:
            continue

        while total_markdown_hits > 0:
            total_markdown_hits -= 1

            if total_markdown_hits % 2:
                html_line = f'{html_line.replace(markdown, f"<{html_tag}>", 1)}'
            else:
                html_line = f'{html_line.replace(markdown, f"</{html_tag}>", 1)}'

    return html_line

def _list_markdown_parser(blog_data, list_items, index, html_line, lines):
    """ list markdown parser
    parses list related markdown """

    list_markdown = '-'
    list_continues = False

    if html_line.startswith(f"{list_markdown} "):
        html_line = f'<li>{html_line[1:].strip()}</li>'
        list_items.append(html_line)
        list_continues = True

        if index < len(lines)-1:
            next_line = lines[index+1]
            
            if not next_line.startswith(f"{list_markdown} "):
                blog_data['data'].append({'type': 'li', 'content': list_items})
                list_continues = False

        else:
            blog_data['data'].append({'type': 'li', 'content': list_items})
            list_continues = False

    return list_continues

def _code_markdown_parser(blog_data, code_items, code_block, html_line):
    """ code markdown parser
    parses code related markdown """

    code_markdown = '```'
    code_exists = False

    if html_line.strip() == code_markdown:
        code_exists = True

        if code_block:
            code_block = False
            blog_data['data'].append({'type': 'code', 'content': code_items})
            code_items = []

        else:
            code_block = True

    elif code_block:
        html_line = f'<p>{html_line.strip()}</p>'
        code_items.append(html_line)

    return code_exists, code_block, code_items

def markdown_converter():
    """ markdown converter
    converts md files into a datastructure """

    blogs = []

    blog_directory = '../blog'

    blog_extension = '*.md'

    located_blog_files = pathlib.Path(blog_directory).glob(blog_extension)

    for located_blog_file in located_blog_files:
        blog_name = str(located_blog_file).split('/')[-1].split('.')[0]

        blog_data = { 'name': blog_name, 'data': [] }

        with open(located_blog_file, 'r') as fn:
            lines = fn.readlines()
            list_items, code_items = [], []
            code_block = False
            
            for index, line in enumerate(lines):
                html_line = line
                html_tag = ''

                if not line.strip():
                    continue

                header_exists = _header_markdown_parser(blog_data, html_line)

                if header_exists:
                    continue

                image_exists = _image_markdown_parser(blog_data, html_line)

                if image_exists:
                    continue

                html_line = _inline_markdown_parser(html_line)

                list_continues = _list_markdown_parser(blog_data, list_items, index, html_line, lines)

                if list_continues:
                    continue
                elif list_items:
                    list_items = []
                    continue

                code_exists, code_block, code_items = _code_markdown_parser(blog_data, code_items, code_block, html_line)

                if code_exists:
                    continue
                elif code_items:
                    continue

                blog_data['data'].append({'type': 'p', 'content': f'<p>{html_line.strip()}</p>'})

            blogs.append(blog_data)

    dump_blogs(blogs)

if __name__ == '__main__':
    markdown_converter()