<script>
    import blogs from './blogs.json';
</script>

<h1>Blogs List</h1>
<ul>
    {#each blogs as blog}
        <li><a href="blog/{blog.name}">{blog.name}</a></li>
    {/each}
</ul>