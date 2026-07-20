import { useEffect, useState } from 'react'
import { fetchToday, checkSolution } from './api'
import Cell from './components/Cell'
import './App.css'

function formatTime(totalSeconds) {
    const m = Math.floor(totalSeconds / 60).toString().padStart(2, '0')
    const s = (totalSeconds % 60).toString().padStart(2, '0')
    return `${m}:${s}`
}

function formatDate(dateStr) {
    const date = new Date(dateStr)
    return date.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })
}

export default function App() {
    const [puzzle, setPuzzle] = useState(null)
    const [error, setError] = useState(null)
    const [seconds, setSeconds] = useState(0)
    const [paused, setPaused] = useState(false)
    const [solved, setSolved] = useState(false)
    const [submitError, setSubmitError] = useState(false)
    const [mode, setMode] = useState('normal')
    const [resetKey, setResetKey] = useState(0)
    const [showInfo, setShowInfo] = useState(false)

    useEffect(() => {
        fetchToday()
            .then(setPuzzle)
            .catch((err) => setError(err.message))
    }, [])

    useEffect(() => {
        if (!puzzle || paused || solved) return
        const id = setInterval(() => setSeconds((s) => s + 1), 1000)
        return () => clearInterval(id)
    }, [puzzle, paused, solved])

    if (error) {
        return <div className="status">Failed to load puzzle: {error}</div>
    }

    if (!puzzle) {
        return <div className="status">Loading puzzle...</div>
    }

    const handleNavigate = (r, c, key) => {
        const [dr, dc] = {
            ArrowUp: [-1, 0],
            ArrowDown: [1, 0],
            ArrowLeft: [0, -1],
            ArrowRight: [0, 1],
        }[key]

        let nr = r + dr
        let nc = c + dc
        while (nr >= 0 && nr < puzzle.rows && nc >= 0 && nc < puzzle.cols) {
            if (puzzle.cells[nr][nc].type === 'entry') {
                document.getElementById(`cell-${nr}-${nc}`)?.focus()
                return
            }
            nr += dr
            nc += dc
        }
    }

    const handleReset = () => {
        setResetKey((k) => k + 1)
        setSubmitError(false)
    }

    const handleSubmit = async () => {
        const grid = puzzle.cells.map((row, r) =>
            row.map((cell, c) => {
                if (cell.type !== 'entry') return 0
                const value = document.getElementById(`cell-${r}-${c}`)?.value
                const digit = parseInt(value, 10)
                return Number.isNaN(digit) ? 0 : digit
            })
        )

        try {
            const correct = await checkSolution(puzzle.date, grid)
            if (correct) {
                setSubmitError(false)
                setSolved(true)
            } else {
                setSubmitError(true)
            }
        } catch {
            setSubmitError(true)
        }
    }

    return (
        <div className="page">
            <div className='title-wrapper'>
                <span className="title-spacer" aria-hidden="true" />
                <h1>Kaku.</h1>
                <button className='more-info-button' 
                onClick={() => setShowInfo(true)}
                aria-label="Show Instructions">?</button>
            </div>
            <div className="details">
                {formatDate(puzzle.date)}
            </div>
            <div className="grid-wrap">
                <div className="toolbar">
                        <button className="reset-button toolbar-left" onClick={handleReset}>Reset Puzzle</button>
                    <div className="mode-toggle" role="group" aria-label="Entry mode">
                        <button
                            type="button"
                            className={`mode-button ${mode === 'normal' ? 'active' : ''}`}
                            onClick={() => setMode('normal')}
                        >
                            Normal
                        </button>
                        <button
                            type="button"
                            className={`mode-button ${mode === 'candidate' ? 'active' : ''}`}
                            onClick={() => setMode('candidate')}
                        >
                            Candidate
                        </button>
                    </div>
                    <div className="timer-wrap">
                        <span className="timer">{formatTime(seconds)}</span>
                        <button
                            className="pause-button"
                            onClick={() => setPaused(true)}
                            aria-label="Pause"
                        >
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                                <rect x="6" y="5" width="4" height="14" />
                                <rect x="14" y="5" width="4" height="14" />
                            </svg>
                        </button>
                    </div>
                </div>
                <div
                    className="grid"
                    style={{ gridTemplateColumns: `repeat(${puzzle.cols}, var(--cell-size))` }}
                >
                    {puzzle.cells.flatMap((row, r) =>
                        row.map((cell, c) => (
                            <Cell
                                key={`${r}-${c}-${resetKey}`}
                                cell={cell}
                                r={r}
                                c={c}
                                mode={mode}
                                onNavigate={handleNavigate}
                            />
                        ))
                    )}
            </div>
            </div>
            <button className="submit-button" onClick={handleSubmit}>Submit</button>
            {submitError && <div className="submit-error">Not quite - keep trying!</div>}
            {paused && (
                <div className="modal-overlay">
                    <div className="modal">
                        <p>Paused</p>
                        <button className="resume-button" onClick={() => setPaused(false)}>Resume</button>
                    </div>
                </div>
            )}
            {solved && (
                <div className="modal-overlay">
                    <div className="modal">
                        <p>Correct!</p>
                        <p>Final time: {formatTime(seconds)}</p>
                        <button className="resume-button" onClick={() => window.location.reload()}>
                            Play Again
                        </button>
                    </div>
                </div>
            )}
            {showInfo && (
                <div className="modal-overlay">
                <div className="modal">
                    <button
                        className="modal-close"
                        onClick={() => setShowInfo(false)}
                        aria-label="Close"
                    >
                        &times;
                    </button>
                    <h1>Kaku. Instructions</h1>
                    <p>Kakuro puzzles have been played for around 76 years when a Canadian puzzle writer created them for American puzzle magazines. Since then these puzzles have been a worldwide craze!</p>
                </div>
                </div>
            )}
        </div>
    )
}
