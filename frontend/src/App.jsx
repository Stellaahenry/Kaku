import { useEffect, useState } from 'react'
import { fetchToday } from './api'
import Cell from './components/Cell'
import './App.css'

export default function App() {
    const [puzzle, setPuzzle] = useState(null)
    const [error, setError] = useState(null)

    useEffect(() => {
        fetchToday()
            .then(setPuzzle)
            .catch((err) => setError(err.message))
    }, [])

    if (error) {
        return <div className="status">Failed to load puzzle: {error}</div>
    }

    if (!puzzle) {
        return <div className="status">Loading puzzle...</div>
    }

    return (
        <div className="page">
            <h1>Kaku</h1>
            <div className="details">
                {puzzle.date} &middot; {puzzle.difficulty}
            </div>
            <div
                className="grid"
                style={{ gridTemplateColumns: `repeat(${puzzle.cols}, 40px)` }}
            >
                {puzzle.cells.flatMap((row, r) =>
                    row.map((cell, c) => (
                        <Cell key={`${r}-${c}`} cell={cell} />
                    ))
                )}
            </div>
        </div>
    )
}
