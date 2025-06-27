<script>
    import { StateKind, stateBootstrapClasses, GridMode } from './constants.js';
    import { interpolateViridis } from 'd3-scale-chromatic';

    let {
        grid,
        mode = GridMode.CONFIG,
        agentValues = null,
        agentPos = null,
        onclick,
    } = $props()

    let gridWidth = $derived(grid[0].length)


    function getCellStyle(kind, row, col) {
        if (mode === GridMode.VALUES && agentValues) {
            const idx = row * gridWidth + col;
            const value = agentValues[idx];
            const min = Math.min(...agentValues);
            const max = Math.max(...agentValues);
            const norm = (value - min) / (max - min || 1);
            const color = interpolateViridis(norm);
            return `background: ${color}; border: 2px solid ${color}; color: #fff;`;
        }
        return '';
    }

    function getCellClass(kind) {
        if (mode === GridMode.VALUES && agentValues) {
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