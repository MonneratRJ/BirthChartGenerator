// script.js
// This script expects chart data to be available as a JSON file or via an API endpoint.
// For demonstration, we'll use a sample data object.

const sampleChartData = {
    planets: [
        { name: "Sun", sign: "Scorpio", degree: 11.23, house: 5 },
        { name: "Moon", sign: "Leo", degree: 19.45, house: 2 },
        // ... add more planets as needed
    ],
    houses: [
        { name: "First House", degree: 22.1 },
        { name: "Second House", degree: 5.3 },
        // ... add more houses as needed
    ]
};

function renderChart(data) {
    const container = document.getElementById('chart-data');
    let html = '<h2>Planetary Positions</h2><ul>';
    data.planets.forEach(planet => {
        html += `<li><strong>${planet.name}</strong>: ${planet.sign} (${planet.degree}°), House ${planet.house}</li>`;
    });
    html += '</ul>';
    html += '<h2>House Cusps</h2><ul>';
    data.houses.forEach(house => {
        html += `<li><strong>${house.name}</strong>: ${house.degree}°</li>`;
    });
    html += '</ul>';
    container.innerHTML = html;
}

async function fetchChartData() {
    const response = await fetch('/api/chart');
    if (!response.ok) {
        document.getElementById('chart-data').innerHTML = '<p>Error loading chart data.</p>';
        return;
    }
    const data = await response.json();
    renderChart(data);
}

document.getElementById('loadChart').addEventListener('click', fetchChartData);

// Optionally, auto-load chart on page load
// window.onload = fetchChartData;
