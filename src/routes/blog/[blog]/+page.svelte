<script>
    import blogs from '../blogs.json'

    export let data;

    const individualBlogs = {};

    blogs.forEach(blog => {
        individualBlogs[blog.name] = blog.data;
    });

    if(data.name in individualBlogs){
        data.content = true;
    }
    else{
        data.content = false;
    }
    
</script>



<div class="bg-slate-800 min-h-screen flex">
    <div class="grow"></div>
    <div class="flex-none w-1/2">
        {#if data.content}
            {#each individualBlogs[data.name] as html}
                {#if html.type == 'h1'}
                    <div class="text-3xl font-bold text-slate-400 mt-4 pb-2">{@html html.content}</div>
                {:else if html.type == 'h2'}
                    <div class="text-2xl font-bold text-slate-400 mt-4 pb-2">{@html html.content}</div>
                {:else if html.type == 'h3'}
                    <div class="text-xl font-bold text-slate-400 mt-4 pb-2">{@html html.content}</div>
                {:else if html.type == 'img'}
                    <div class="bg-white mt-4 pb-2">{@html html.content}</div>
                {:else if html.type == 'li'}
                    <ul class="text-sky-500 pl-4 list-disc">
                        {#each html.content as listItem}
                            {@html listItem}
                        {/each}
                    </ul>
                {:else}
                    <div class="text-slate-300 pb-2">{@html html.content}</div>
                {/if}
            {/each}
        {:else}
            <p>Invalid URL for blog post.</p>
        {/if}
        <a class="text-slate-600 hover:text-slate-400" href='/blog'>Go Back</a>
    </div>
    <div class="grow"></div>
</div>