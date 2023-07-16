<script>
    import blogs from '../blogs.json'

    const individualBlogs = {};

    blogs.forEach(blog => {
        const name = blog.name;
        const html = blog.html;

        individualBlogs[name] = html;
    });

    export let data;

    if(data.name in individualBlogs){
        data.content = true;
        data.html = individualBlogs[data.name];
    }
    else{
        data.content = false;
    }
    
</script>

{#if data.content}
    {#each data.html as blogLine}
        {#if blogLine.html_tag == 'h1'}
            <h1>{blogLine.content}</h1>
        {:else if blogLine.html_tag == 'p'}
            <p>{blogLine.content}</p>
        {/if}
    {/each}
{:else}
    <p>Invalid URL for blog post.</p>
{/if}