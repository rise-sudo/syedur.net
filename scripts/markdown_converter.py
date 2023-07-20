import pathlib, json

def define_markdown_to_html():
    """ define markdown to html
    links the markdown to the appropriate html equivalent
    if applicable otherwise a key term is used instead """

    markdown_to_html = {
        "#": "h1",
        "##": "h2",
        "###": "h3",
        "![+]+(+)": "img",
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
    coverts md files to json """

    blogs = []

    markdown_to_html = define_markdown_to_html()

    blog_directory = '../blog'

    blog_extension = '*.md'

    located_blog_files = pathlib.Path(blog_directory).glob(blog_extension)

    for file in located_blog_files:
        blog_name = str(file).split('/')[-1].split('.')[0]

        blog_data = {
            'name': blog_name,
            'html': []
        }

        with open(file, 'r') as fn:
            
            for line in fn.readlines():                    
                if not line.strip():
                    continue

                content = []
                html_tag = ''

                for markdown in markdown_to_html.keys():

                    if line.split()[0] == markdown:
                        content = [' '.join(line.split()[1:])]
                        html_tag = markdown_to_html[markdown]

                        break

                    elif '+' in markdown:
                        markdown_components = markdown.split('+')
                        block_content = ''
                        start_of_block = True

                        for markdown_component in markdown_components:
                            if markdown_component in line and start_of_block:
                                block_content = line.split(markdown_component, 1)[-1]
                                start_of_block = False
                            elif markdown_component in line:
                                block_content = block_content.split(markdown_component, 1)[0]
                                start_of_block = True
                                content.append(block_content)

                        if len(content) > 0:
                            html_tag = markdown_to_html[markdown]

                html_tag = html_tag if html_tag else 'p'
                content = content if len(content) > 0 else [line.strip()]
                blog_data['html'].append({'html_tag': html_tag, 'content': content})

        blogs.append(blog_data)

    dump_blogs(blogs)

if __name__ == '__main__':
    markdown_converter()