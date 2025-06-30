<script>
  import { onMount } from 'svelte';
  import hljs from 'highlight.js/lib/core';
  import python from 'highlight.js/lib/languages/python';
  import 'highlight.js/styles/github-dark.css'; // Import CSS theme

  hljs.registerLanguage('python', python);
  let {code='', language='python', sourceUrl=''} = $props()
  let codeElement;

  onMount(() => {
    hljs.highlightElement(codeElement);
  });
</script>

<div class="code-block-container">
  {#if sourceUrl}
    <div class="source-link">
      <a href={sourceUrl} target="_blank" rel="noopener noreferrer" class="source-link-anchor">
        Source
      </a>
    </div>
  {/if}
  <pre><code bind:this={codeElement} class="language-{language}">{code}</code></pre>
</div>

<style>
  .code-block-container {
    position: relative;
  }
  
  .source-link {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    z-index: 10;
  }
  
  .source-link-anchor {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background-color: rgba(0, 0, 0, 0.7);
    text-decoration: none;
    border-radius: 0.25rem;
    font-size: 0.75rem;
  }
  
</style>