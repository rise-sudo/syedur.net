import pathlib, json

def define_markdown_to_html():
    """ define markdown to html
    defines how to convert markdown to html tags """

    markdown_to_html = {
        "#": "h1",
    }

    return markdown_to_html

def dump_blogs(blogs):
    """ dump blogs
    dump the blogs data in src/data """

    filename = '../src/routes/blog/blogs.json'

    with open(filename, 'w') as fn:
        json.dump(blogs, fn, sort_keys=True, indent=4)

def converter():
    """ converter
    this coverts md files to json """

    blogs = []

    target_directory = '../blog'

    target_extension = '*.md'

    located_files = pathlib.Path(target_directory).glob(target_extension)

    markdown_to_html = define_markdown_to_html()

    for file in located_files:
        blog_name = str(file).split('/')[-1].split('.')[0]

        blog_data = {
            'name': blog_name,
            'html': []
        }

        with open(file, 'r') as fn:
            for line in fn.readlines():
                if not line.strip():
                    continue

                provided_markdown = line.split()[0]

                html_tag = markdown_to_html.get(provided_markdown, 'p')

                content = line[1:].strip() if html_tag != 'p' else line.strip()

                blog_data['html'].append({'html_tag': html_tag, 'content': content})

        blogs.append(blog_data)

    dump_blogs(blogs)

if __name__ == '__main__':
    converter()