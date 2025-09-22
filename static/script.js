// script.js
let zodiacSigns = {};

async function loadZodiacSigns() {
    const response = await fetch('static/zodiac_signs.json');
    zodiacSigns = await response.json();
}

async function fetchChartData(formData) {
    if (Object.keys(zodiacSigns).length === 0) {
        await loadZodiacSigns();
    }
    const response = await fetch('/api/chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });
    if (!response.ok) {
        document.getElementById('chart-data').innerHTML = '<p>Error loading chart data.</p>';
        return;
    }
    const data = await response.json();
    renderChart(data);
}

document.getElementById('chartForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    let valid = true;
    Array.from(e.target.elements).forEach(el => {
        if (el.name && el.required) {
            if (!el.value || (el.type === 'number' && isNaN(el.value))) {
                el.style.border = '2px solid red';
                valid = false;
            } else {
                el.style.border = '';
            }
        }
    });
    if (!valid) {
        return;
    }
    const formData = {};
    Array.from(e.target.elements).forEach(el => {
        if (el.name) formData[el.name] = el.value;
    });
    await fetchChartData(formData);
});

function formatDegree(degree) {
    const deg = Math.floor(degree);
    const min = Math.round((degree - deg) * 60);
    const degStr = deg.toString().padStart(2, '0');
    const minStr = min.toString().padStart(2, '0');
    return `${degStr}°${minStr}`;
}

function formatDegreeInSign(degree) {
    // Zodiac signs start every 30 degrees
    const degInSign = degree % 30;
    const deg = Math.floor(degInSign);
    const min = Math.round((degInSign - deg) * 60);
    const degStr = deg.toString().padStart(2, '0');
    const minStr = min.toString().padStart(2, '0');
    return `${degStr}º${minStr}'`;
}

function getHouseRoman(houseNameOrNum) {
    // Accepts either number (1-12) or string like 'Seventh_House'
    const houseMap = {
        "First_House": "I",
        "Second_House": "II",
        "Third_House": "III",
        "Fourth_House": "IV",
        "Fifth_House": "V",
        "Sixth_House": "VI",
        "Seventh_House": "VII",
        "Eighth_House": "VIII",
        "Ninth_House": "IX",
        "Tenth_House": "X",
        "Eleventh_House": "XI",
        "Twelfth_House": "XII"
    };
    if (typeof houseNameOrNum === "string" && houseMap[houseNameOrNum]) {
        return houseMap[houseNameOrNum];
    }
    // If it's a number 1-12
    const roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];
    let num = parseInt(houseNameOrNum);
    if (!isNaN(num) && num >= 1 && num <= 12) {
        return roman[num - 1];
    }
    return houseNameOrNum;
}

function renderChart(data) {
    const container = document.getElementById('chart-data');
    let html = '<h2>Planetary Positions</h2><ul>';
    data.planets.forEach(planet => {
        const signData = zodiacSigns[planet.sign] || {};
        const signIcon = signData.icon || "";
        const signFull = signData.name || planet.sign;
        let houseLabel = getHouseRoman(planet.house);
        html += `<li><strong>${planet.name}</strong>: ${signIcon} ${signFull} (${formatDegreeInSign(planet.degree)}), House ${houseLabel}</li>`;
    });
    html += '</ul>';
    const houseLabels = ["Ascendant", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];
    html += '<h2>House Cusps</h2><ul>';
    data.houses.forEach((house, idx) => {
        const signData = zodiacSigns[house.sign] || {};
        const signIcon = signData.icon || "";
        const signFull = signData.name || house.sign;
        const label = houseLabels[idx] || `House ${idx + 1}`;
        html += `<li><strong>${label}</strong>: ${signIcon} ${signFull} (${formatDegreeInSign(house.degree)})</li>`;
    });
    html += '</ul>';
    container.innerHTML = html;
}

async function populateCountries() {
    const select = document.getElementById('country');
    const url = 'static/countries.json';
    try {
        const response = await fetch(url);
        let countries = await response.json();
        countries = countries.sort((a, b) => a.name.localeCompare(b.name));
        select.innerHTML = '';
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country.code;
            option.textContent = country.name;
            if (country.code === 'BR') option.selected = true;
            select.appendChild(option);
        });
    } catch (err) {
        select.innerHTML = '<option value="BR" selected>Brazil</option>';
    }
}

async function populateCities(countryCode) {
    const citySelect = document.getElementById('city');
    citySelect.innerHTML = '<option value="">Loading...</option>';
    try {
        const response = await fetch('static/cities.json');
        const citiesData = await response.json();
        let cities = citiesData[countryCode] || [];
        cities = cities.sort((a, b) => a.name.localeCompare(b.name));
        citySelect.innerHTML = '';
        if (cities.length === 0) {
            citySelect.innerHTML = '<option value="">No cities found</option>';
            return;
        }
        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city.name;
            option.textContent = city.name;
            citySelect.appendChild(option);
        });
    } catch (err) {
        citySelect.innerHTML = '<option value="">Error loading cities</option>';
    }
}

async function autofillCityData(countryCode, cityName) {
    try {
        const response = await fetch('static/cities.json');
        const citiesData = await response.json();
        const cities = citiesData[countryCode] || [];
        const city = cities.find(c => c.name === cityName);
        if (!city) return;
        document.getElementById('lat').value = city.lat;
        document.getElementById('lng').value = city.lon;
        // Timezone
        const tzKey = `${countryCode}:${cityName}`;
        const tzResp = await fetch('static/city_timezones.json');
        const tzData = await tzResp.json();
        document.getElementById('tz_str').value = tzData[tzKey] || '';
    } catch (err) {
        // Do nothing, allow manual entry
    }
}

window.onload = async function () {
    await loadZodiacSigns();
    populateCountries().then(() => {
        // Show Brazilian cities by default
        populateCities('BR');
    });
    // When country changes, populate cities
    document.getElementById('country').addEventListener('change', function () {
        populateCities(this.value);
        // Reset city/lat/lon/tz fields
        document.getElementById('city').innerHTML = '<option value="">Select a city</option>';
        document.getElementById('lat').value = '';
        document.getElementById('lng').value = '';
        document.getElementById('tz_str').value = '';
    });
    // When city changes, autofill lat/lon/tz
    document.getElementById('city').addEventListener('change', function () {
        const countryCode = document.getElementById('country').value;
        autofillCityData(countryCode, this.value);
    });
    // Always keep timezone input disabled
    document.getElementById('tz_str').disabled = true;
    document.getElementById('tz_str').style.background = '#f0f0f0';
    document.getElementById('tz_str').style.color = '#888';
    // Optionally, auto-load chart on page load
    // fetchChartData();
};
