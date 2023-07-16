<script>
    import blogs from './blogs.json';
</script>

<div class="bg-slate-800 min-h-screen flex">
    <div class="grow"></div>
    <div class="flex-none w-1/2">
        <h1 class="text-3xl font-bold text-slate-400 mt-4">Blogs</h1>
        <p class="text-slate-300 pb-2">Here are the available blogs:</p>
        <ul>
            {#each blogs as blog}
                <li class="text-slate-600 hover:text-slate-400"><a href="blog/{blog.name}">{blog.name}</a></li>
            {/each}
        </ul>
    </div>
    <div class="grow"></div>
</div>