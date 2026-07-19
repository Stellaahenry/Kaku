export async function fetchToday() {
    try {
        const response = await fetch('/puzzles/today');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching today:', error);
        throw error;
    }
}

export async function checkSolution(dateStr, grid) {
    try {
        const response = await fetch(`/puzzles/${dateStr}/check`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ grid }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.correct;
    } catch (error) {
        console.error('Error checking solution:', error);
        throw error;
    }
}