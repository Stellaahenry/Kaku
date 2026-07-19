const ARROW_KEYS = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight']

export default function Cell({ cell, r, c, onNavigate }) {
    if (cell.type === 'block') {
        return <div className="cell block" />
    }

    if (cell.type === 'clue') {
        return (
            <div className="cell clue">
                {cell.across != null && <span className="across">{cell.across}</span>}
                {cell.down != null && <span className="down">{cell.down}</span>}
            </div>
        )
    }

    return (
        <input
            id={`cell-${r}-${c}`}
            type="text"
            inputMode="numeric"
            maxLength={1}
            className="cell entry"
            onChange={(e) => {
                e.target.value = e.target.value.replace(/[^1-9]/g, '')
            }}
            onKeyDown={(e) => {
                if (e.key === 'Backspace' || e.key === 'Delete') {
                    e.preventDefault()
                    e.target.value = ''
                    return
                }
                if (ARROW_KEYS.includes(e.key)) {
                    e.preventDefault()
                    onNavigate(r, c, e.key)
                }
            }}
        />
    )
}