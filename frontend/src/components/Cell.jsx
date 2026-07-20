import { useState } from 'react'

const GRID_FORMAT = [5, 6, 2, 9, 1, 7, 4, 8, 3]
const ARROW_KEYS = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight']
const DIGIT_KEY = /^[1-9]$/

export default function Cell({ cell, r, c, mode, onNavigate }) {
    const [candidates, setCandidates] = useState(new Set())
    const [entry, setEntry] = useState('')

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
        <div className="cell entry-wrap">
            <input
                id={`cell-${r}-${c}`}
                type="text"
                inputMode="numeric"
                maxLength={1}
                className="entry-input"
                onChange={(e) => {
                    e.target.value = e.target.value.replace(/[^1-9]/g, '')
                }}
                onKeyDown={(e) => {
                    if (e.key === 'Backspace' || e.key === 'Delete') {
                        e.preventDefault()
                        e.target.value = ''
                        setEntry('')
                        return
                    }
                    if (ARROW_KEYS.includes(e.key)) {
                        e.preventDefault()
                        onNavigate(r, c, e.key)
                        return
                    }
                    if (mode === 'candidate' && DIGIT_KEY.test(e.key)) {
                        e.preventDefault()
                        setCandidates((prev) => {
                            const next = new Set(prev)
                            if (next.has(e.key)) {
                                next.delete(e.key)
                            } else {
                                next.add(e.key)
                            }
                            return next
                        })
                    }
                    if (mode === 'normal' && DIGIT_KEY.test(e.key)) {
                        e.preventDefault()
                        e.target.value = e.key
                        setEntry(e.key)
                    }
                }}
            />
            {candidates.size > 0 && entry === '' && (
                <div className="candidates">
                    {GRID_FORMAT.map((digit) => (
                        <span key={digit} className="candidate-slot">
                            {candidates.has(String(digit)) ? digit : ''}
                        </span>
                    ))}
                </div>
            )}
        </div>
    )
}
