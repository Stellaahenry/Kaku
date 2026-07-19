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