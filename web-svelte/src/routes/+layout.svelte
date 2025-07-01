<script>
    import "../app.css";
    import Navbar from '../lib/Navbar.svelte';
</script>

<div class="layout">
    <Navbar />
    <main class="main-content">
        <div class="page-container">
            <slot />
        </div>
    </main>
    <footer class="footer">
        <div class="footer-content">
            <p>&copy; 2025 Reinforcement Learning Introduction on <a href="https://github.com/DefineDan/rl-intro">Github</a>. </p>
        </div>
    </footer>
</div>

<style>
    .layout {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .page-container {
        max-width: 66rem;
        margin-left: auto;
        margin-right: auto;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 4rem;
        flex: 1;
    }

    .footer {
        margin-top: auto;
    }

    .footer-content {
        max-width: 66rem;
        margin-left: auto;
        margin-right: auto;
        color: #888;
    }

    .footer-content p {
        text-align: center;
    }
</style>