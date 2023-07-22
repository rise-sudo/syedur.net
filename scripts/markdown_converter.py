import pathlib, json

def define_markdown_to_html():
    """ define markdown to html
    links the markdown to the appropriate html equivalent
    if applicable otherwise a key term is used instead """

    markdown_to_html = {
        "simple": {
            "#": "h1",
            "##": "h2",
            "###": "h3",

        },
        "inline": {
            "**": "b",
            "_": "i"
        },
        "image": "!["
    }

    return markdown_to_html

def dump_blogs(blogs):
    """ dump blogs
    dump the blogs datastructure in the appropriate directory """

    filename = '../src/routes/blog/blogs.json'

    with open(filename, 'w') as fn:
        json.dump(blogs, fn, sort_keys=True, indent=4)

def markdown_converter():
    """ markdown converter
    converts md files into a datastructure """

    blogs = []

    markdown_to_html = define_markdown_to_html()

    blog_directory = '../blog'

    blog_extension = '*.md'

    located_blog_files = pathlib.Path(blog_directory).glob(blog_extension)

    for located_blog_file in located_blog_files:
        blog_name = str(located_blog_file).split('/')[-1].split('.')[0]

        blog_data = { 'name': blog_name, 'data': [] }

        with open(located_blog_file, 'r') as fn:
            
            for line in fn.readlines():
                simple_markdown = False
                html_line = line
                html_tag = ''

                if not line.strip():
                    continue

                for markdown in markdown_to_html['simple']:
                    if line.startswith(f'{markdown} '):
                        html_tag = markdown_to_html['simple'][markdown]
                        html_line = f'<{html_tag}>{line[len(markdown):].strip()}</{html_tag}>'
                        simple_markdown = True
                        break

                if simple_markdown:
                    blog_data['data'].append({'type': html_tag, 'content': html_line.strip()})
                    continue

                if line.startswith(markdown_to_html['image']):
                    alternate_text = line.split('](')[0][2:]
                    image_source = line.split('](')[-1][:-1]
                    html_line = f'<img alt="{alternate_text}" src="{image_source}">'
                    blog_data['data'].append({'type': 'img', 'content': html_line.strip()})
                    continue

                for markdown in markdown_to_html['inline']:
                    total_markdown_hits = line.count(markdown)

                    if total_markdown_hits == 1:
                        continue

                    while total_markdown_hits > 0:
                        total_markdown_hits -= 1
                        html_tag = markdown_to_html['inline'][markdown]

                        if total_markdown_hits % 2:
                            html_line = f'{html_line.replace(markdown, f"<{html_tag}>", 1)}'
                        else:
                            html_line = f'{html_line.replace(markdown, f"</{html_tag}>", 1)}'

                blog_data['data'].append({'type': 'p', 'content': f'<p>{html_line.strip()}</p>'})

            blogs.append(blog_data)

    dump_blogs(blogs)

if __name__ == '__main__':
    markdown_converter()