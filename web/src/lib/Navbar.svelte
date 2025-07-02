<script>
  import { base } from '$app/paths';
</script>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
  <div class="container-fluid">
    <a class="navbar-brand" href="{base}/">RL Intro</a>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
      aria-controls="navbarNav"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <a class="nav-link" href="{base}/">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{base}/tabular-methods">Tabular Methods</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{base}/model-based-methods">Model-based RL</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{base}/function-approximation"
            >Function Approximation</a
          >
        </li>
      </ul>
    </div>
  </div>
</nav>
