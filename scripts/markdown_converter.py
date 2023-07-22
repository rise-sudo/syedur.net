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
            "b": {
                "start": "**",
                "end": "**"
            },
            "i": {
                "start": "_",
                "end": "_",
            }
        },
        "block": {
            "![+]+(+)": "img",
        }
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

    for file in located_blog_files:
        blog_name = str(file).split('/')[-1].split('.')[0]

        blog_data = {
            'name': blog_name,
            'html': []
        }

        with open(file, 'r') as fn:
            
            for markdown_line in fn.readlines():
                if not markdown_line.strip():
                    continue

                simple_markdown = False
                html_tag = ''
                special_format = ''
                line = []
                block_markdown_history = []
                block_content = ''
                completed_block = ''
                maybe_image = False
                uncategorized_block_content = ''
                start_of_block = True

                for index, word in enumerate(markdown_line.split()):
                    categorized = False

                    if index == 0:
                        for markdown in markdown_to_html['simple'].keys():

                            if word == markdown:
                                line_component = {
                                    'content': ' '.join(markdown_line.split()[1:]),
                                }
                                
                                line = [line_component]

                                html_tag = markdown_to_html['simple'][markdown]

                                simple_markdown = True

                                break

                        if simple_markdown:
                            break

                    for markdown, location in markdown_to_html['inline'].items():

                        markdown_start = location['start']
                        markdown_end = location['end']

                        if word.startswith(markdown_start) and start_of_block:
                            if word.endswith(markdown_end):
                                completed_block = f'{word[len(markdown_start):len(word)-len(markdown_end)]}'
                                special_format = markdown
                                categorized = True
                                break

                            word = word[len(markdown_start):]
                            block_markdown_history.append(markdown)
                            start_of_block = False
                        
                        if word.endswith(markdown_end) and markdown == block_markdown_history[-1]:
                            completed_block = block_content + f' {word[:len(word)-len(markdown_end)]}'
                            special_format = block_markdown_history[-1]
                            start_of_block = True
                            block_content = ''
                            categorized = True
                        elif not start_of_block:
                            if markdown == block_markdown_history[-1]:
                                block_content += f' {word}'
                                categorized = True

                    for markdown in markdown_to_html['block']:
                        markdown_components = markdown.split('+')
                        teststart_of_block = True

                        for markdown_component in markdown_components:
                            if markdown_component in word and teststart_of_block:
                                teststart_of_block = False
                            elif markdown_component in word:
                                maybe_image = True
                                teststart_of_block = True

                        if maybe_image:
                            html_tag = markdown_to_html['block'][markdown]


                    if not categorized:
                        uncategorized_block_content += f' {word}'
                    elif uncategorized_block_content:
                        line.append({
                            'content': uncategorized_block_content.lstrip(),
                        })
                        uncategorized_block_content = ''
                    if completed_block:
                        line.append({
                            'content': completed_block.lstrip(),
                            'special_format': special_format,
                        })
                        completed_block = ''

                html_tag = html_tag if html_tag else 'p'

                if html_tag == 'img':
                    line.append({
                        'content': markdown_line[2:].split(']')[0]
                    })
                    line.append({
                        'content': markdown_line.split('(')[-1][:-1]
                    })

                line = line if len(line) > 0 else [{'content': markdown_line.strip()}]



                blog_data['html'].append({'html_tag': html_tag, 'line': line})

            blogs.append(blog_data)

    dump_blogs(blogs)


if __name__ == '__main__':
    markdown_converter()