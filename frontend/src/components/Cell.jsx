export default function Cell({ cell }) {
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

    return <div className="cell entry" />
}