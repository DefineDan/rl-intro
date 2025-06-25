let pyodidePromise = null;

export function getPyodide() {
  if (!pyodidePromise) {
    pyodidePromise = (async () => {
      console.log("Initializing Pyodide...");
      const pyodide = await window.loadPyodide();

      // Install packages once
      console.log("Installing packages...");
      await pyodide.loadPackage(["micropip"]);
      await pyodide.runPythonAsync(`
        import micropip
        await micropip.install("py/rl_intro-0.1.1-py3-none-any.whl")
        import rl_intro
      `);
      const response = await fetch("/py/simulation.py");
      const code = await response.text();
      await pyodide.runPythonAsync(code);
      console.log("Pyodide ready to go!");
      return pyodide;
    })();
  }
  return pyodidePromise;
} 