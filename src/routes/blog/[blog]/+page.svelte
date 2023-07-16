<script>
    import blogs from '../blogs.json'

    export let data;

    const individualBlogs = {};

    blogs.forEach(blog => {
        const name = blog.name;
        const html = blog.html;

        individualBlogs[name] = html;
    });

    if(data.name in individualBlogs){
        data.content = true;
        data.html = individualBlogs[data.name];
    }
    else{
        data.content = false;
    }
    
</script>



<div class="bg-slate-800 min-h-screen flex">
    <div class="grow"></div>
    <div class="flex-none w-1/2">
        {#if data.content}
            {#each data.html as blogLine}
                {#if blogLine.html_tag == 'h1'}
                    <h1 class="text-3xl font-bold text-slate-400 mt-4 pb-2">{blogLine.content}</h1>
                {:else if blogLine.html_tag == 'p'}
                    <p class="text-slate-300 pb-2">{blogLine.content}</p>
                {/if}
            {/each}
        {:else}
            <p>Invalid URL for blog post.</p>
        {/if}
        <a class="text-slate-600 hover:text-slate-400" href='/blog'>Go Back</a>
    </div>
    <div class="grow"></div>
</div>