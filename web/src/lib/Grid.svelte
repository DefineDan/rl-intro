<script>
    import { StateKind, stateBootstrapClasses, GridMode } from './constants.js';
    import { interpolateViridis, interpolateInferno } from 'd3-scale-chromatic';

    let {
        grid,
        mode = GridMode.CONFIG,
        agentValues = null,
        agentVisits = null,
        agentPos = null,
        onclick,
    } = $props()

    let gridWidth = $derived(grid[0].length)


    function getCellStyle(kind, row, col) {
        const data = (mode === GridMode.VALUES && agentValues) ? agentValues : 
                     (mode === GridMode.VISITS && agentVisits) ? agentVisits : null;    
        if (data) {
            const idx = row * gridWidth + col;
            const value = data[idx] || 0;
            const min = Math.min(...data);
            const max = Math.max(...data);
            const norm = max > min ? (value - min) / (max - min) : 0;
            const color = mode === GridMode.VALUES ? interpolateViridis(norm) : interpolateInferno(norm);
            return `background: ${color}; border: 2px solid ${color}; color: #fff;`;
        }
        return '';
    }

    function getCellClass(kind) {
        if (mode === GridMode.VALUES && agentValues || mode === GridMode.VISITS && agentVisits) {
            return "btn btn-outline-primary";
        }
        return `btn ${stateBootstrapClasses[kind] || "btn-secondary"}`;
    }

    function getCellContent(row, col) {
        if (agentPos && row === agentPos.row && col === agentPos.col) {
            return '🤖';
        }
        if (mode === GridMode.VALUES && agentValues) {
            const idx = row * gridWidth + col;
            return agentValues[idx].toFixed(1);
        }
        if (mode === GridMode.VISITS && agentVisits) {
            const idx = row * gridWidth + col;
            return agentVisits[idx] || 0;
        }
        const kind = grid[row][col];
        switch (kind) {
            case StateKind.START:
                return 'S';
            case StateKind.TERMINAL:
                return 'T';
            case StateKind.CLIFF:
                return 'C';
            case StateKind.WALL:
                return 'W';
            default:
                return '';
        }
    }
</script>

<div class="grid" style="grid-template-columns: repeat({gridWidth}, 40px)">
    {#each grid as row, i}
        {#each row as cell, j}
            <button
                type="button"
                class={"cell btn "+ getCellClass(cell)}
                style={getCellStyle(cell, i, j)}
                onclick={() => {
                    if (mode === GridMode.CONFIG) {
                        onclick(i, j);
                    }
                }}
            >
                {@html getCellContent(i, j)}
            </button>
        {/each}
    {/each}
</div>

<style>
    .grid {
        display: grid;
    }
    .cell {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2em;
        cursor: pointer;
        user-select: none;
        font: inherit;
    }
</style> 