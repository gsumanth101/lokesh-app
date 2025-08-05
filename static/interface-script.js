// Smart Farming Assistant JavaScript
// Global variables
let currentLanguage = 'en';
let cropListings = [
    {
        crop_name: 'rice',
        quantity: 1000,
        price: 45.0,
        contact_info: '+91-9876543210',
        location_detail: 'Kurnool, Andhra Pradesh'
    },
    {
        crop_name: 'wheat',
        quantity: 750,
        price: 35.0,
        contact_info: '+91-9876543211',
        location_detail: 'Ludhiana, Punjab'
    },
    {
        crop_name: 'sugarcane',
        quantity: 2000,
        price: 25.0,
        contact_info: '+91-9876543212',
        location_detail: 'Kolhapur, Maharashtra'
    },
    {
        crop_name: 'tomato',
        quantity: 500,
        price: 60.0,
        contact_info: '+91-9876543213',
        location_detail: 'Nashik, Maharashtra'
    },
    {
        crop_name: 'cotton',
        quantity: 800,
        price: 55.0,
        contact_info: '+91-9876543214',
        location_detail: 'Warangal, Telangana'
    },
    {
        crop_name: 'maize',
        quantity: 1200,
        price: 30.0,
        contact_info: '+91-9876543215',
        location_detail: 'Davangere, Karnataka'
    }
];

// Sample market prices
let marketPrices = [
    { crop: 'Rice', price: 45.0, trend: 'up', change: 2.5 },
    { crop: 'Wheat', price: 35.0, trend: 'down', change: -1.2 },
    { crop: 'Maize', price: 30.0, trend: 'stable', change: 0.1 },
    { crop: 'Cotton', price: 55.0, trend: 'up', change: 3.8 },
    { crop: 'Sugarcane', price: 25.0, trend: 'stable', change: 0.5 },
    { crop: 'Tomato', price: 60.0, trend: 'up', change: 5.2 }
];

// Pest control information
let pestControlInfo = {
    wheat: {
        common_pests: ['Aphids', 'Rust', 'Smut'],
        prevention: 'Regular field inspection, crop rotation, use of resistant varieties',
        treatment: 'Apply neem oil, use biological control agents, fungicide spray if needed'
    },
    rice: {
        common_pests: ['Brown Planthopper', 'Stem Borer', 'Blast'],
        prevention: 'Proper water management, balanced fertilization, resistant varieties',
        treatment: 'Use pheromone traps, apply organic pesticides, fungicide treatment'
    },
    maize: {
        common_pests: ['Fall Armyworm', 'Corn Borer', 'Cutworm'],
        prevention: 'Early planting, intercropping, field sanitation',
        treatment: 'Apply Bt spray, use entomopathogenic fungi, targeted insecticides'
    },
    cotton: {
        common_pests: ['Bollworm', 'Aphids', 'Whitefly'],
        prevention: 'Bt cotton varieties, trap crops, beneficial insects',
        treatment: 'IPM approach, selective insecticides, biological control'
    },
    sugarcane: {
        common_pests: ['Sugarcane Borer', 'Aphids', 'Scale Insects'],
        prevention: 'Healthy seedlings, proper spacing, field hygiene',
        treatment: 'Release parasitoids, apply neem products, systemic insecticides'
    },
    tomato: {
        common_pests: ['Tomato Hornworm', 'Whitefly', 'Late Blight'],
        prevention: 'Crop rotation, mulching, resistant varieties',
        treatment: 'Hand picking, sticky traps, copper-based fungicides'
    },
    potato: {
        common_pests: ['Colorado Potato Beetle', 'Late Blight', 'Aphids'],
        prevention: 'Crop rotation, certified seeds, proper storage',
        treatment: 'Bt spray, fungicide application, beneficial insects'
    },
    onion: {
        common_pests: ['Thrips', 'Onion Fly', 'Purple Blotch'],
        prevention: 'Proper spacing, field sanitation, resistant varieties',
        treatment: 'Blue sticky traps, neem oil, copper fungicides'
    }
};

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Load marketplace listings
    loadMarketplaceListing();
    
    // Load market prices
    loadMarketPrices();
    
    // Set default language
    changeLanguage();
    
    // Load user info
    loadUserInfo();
}

// Load user info
function loadUserInfo() {
    // This would typically come from session/server
    const userName = document.getElementById('user-name');
    if (userName) {
        userName.textContent = 'Welcome, User!';
    }
}

// Logout function
async function logout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Logout error:', error);
        window.location.href = '/login';
    }
}

// Tab switching functionality
function showTab(tabId) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => button.classList.remove('active'));
    
    // Show selected tab content
    document.getElementById(tabId).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Language change functionality
function changeLanguage() {
    const languageSelect = document.getElementById('languageSelect');
    currentLanguage = languageSelect.value;
    
    // Update all elements with data-lang attribute
    const elements = document.querySelectorAll('[data-lang]');
    elements.forEach(element => {
        const key = element.getAttribute('data-lang');
        if (translations[currentLanguage] && translations[currentLanguage][key]) {
            element.textContent = translations[currentLanguage][key];
        }
    });
}

// Toggle manual soil input
function toggleManualSoil() {
    const checkbox = document.getElementById('manual-soil');
    const manualSoilInputs = document.getElementById('manual-soil-inputs');
    
    if (checkbox.checked) {
        manualSoilInputs.style.display = 'block';
    } else {
        manualSoilInputs.style.display = 'none';
    }
}

// Show loading spinner
function showLoading() {
    document.getElementById('loading-spinner').style.display = 'flex';
}

// Hide loading spinner
function hideLoading() {
    document.getElementById('loading-spinner').style.display = 'none';
}

// Get crop recommendation
async function getCropRecommendation() {
    const location = document.getElementById('location').value;
    const apiKey = document.getElementById('weather-api-key').value;
    
    if (!location || !apiKey) {
        alert('Please enter both location and Weather API key');
        return;
    }
    
    showLoading();
    
    try {
        // Simulate API call to get weather data
        const weatherData = await getWeatherData(location, apiKey);
        
        if (weatherData) {
            // Get soil data (manual or automatic)
            const soilData = getManualSoilData();
            
            // Simulate crop recommendation
            const recommendation = await getCropRecommendationFromData(weatherData, soilData);
            
            displayCropRecommendation(recommendation, location);
        }
    } catch (error) {
        console.error('Error getting crop recommendation:', error);
        alert('Error getting crop recommendation. Please try again.');
    } finally {
        hideLoading();
    }
}

// Get manual soil data if checkbox is checked
function getManualSoilData() {
    const manualSoilCheckbox = document.getElementById('manual-soil');
    
    if (manualSoilCheckbox.checked) {
        return {
            N: parseFloat(document.getElementById('nitrogen').value) || 80,
            P: parseFloat(document.getElementById('phosphorus').value) || 40,
            K: parseFloat(document.getElementById('potassium').value) || 60,
            pH: parseFloat(document.getElementById('ph').value) || 6.5
        };
    }
    
    return null;
}

// Get weather data from Flask backend
async function getWeatherData(location, apiKey) {
    try {
        const response = await fetch('/api/weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ location, api_key: apiKey })
        });
        
        const result = await response.json();
        
        if (result.success) {
            return result.data;
        } else {
            throw new Error(result.message || 'Weather API error');
        }
    } catch (error) {
        console.error('Weather API error:', error);
        throw error;
    }
}

// Get crop recommendation from Flask backend
async function getCropRecommendationFromData(weatherData, soilData) {
    try {
        const response = await fetch('/api/crop-recommendation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                temperature: weatherData.temperature,
                humidity: weatherData.humidity,
                soil_data: soilData || {
                    N: 80,
                    P: 40,
                    K: 60,
                    pH: 6.5,
                    rainfall: 800
                }
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            return result.data;
        } else {
            throw new Error(result.message || 'Crop recommendation error');
        }
    } catch (error) {
        console.error('Crop recommendation error:', error);
        throw error;
    }
}

// Display crop recommendation
function displayCropRecommendation(recommendation, location) {
    const resultContainer = document.getElementById('recommendation-result');
    
    resultContainer.innerHTML = `
        <div class="recommendation-card">
            <h3>🌾 Recommended Crop: ${recommendation.crop.charAt(0).toUpperCase() + recommendation.crop.slice(1)}</h3>
            <p>Confidence: ${recommendation.confidence.toFixed(1)}%</p>
            <p>Location: ${location}</p>
        </div>
        
        <div class="data-section">
            <div class="weather-info">
                <h4>🌤️ Weather Conditions</h4>
                <p>Temperature: ${recommendation.weather.temperature.toFixed(1)}°C</p>
                <p>Humidity: ${recommendation.weather.humidity.toFixed(1)}%</p>
                <p>Condition: ${recommendation.weather.condition}</p>
            </div>
            
            <div class="soil-info">
                <h4>🌱 Soil Analysis</h4>
                <p>Nitrogen (N): ${recommendation.soil.N}</p>
                <p>Phosphorus (P): ${recommendation.soil.P}</p>
                <p>Potassium (K): ${recommendation.soil.K}</p>
                <p>pH Level: ${recommendation.soil.pH}</p>
            </div>
        </div>
    `;
    
    resultContainer.style.display = 'block';
}

// Get weather information
async function getWeatherInfo() {
    const location = document.getElementById('weather-location').value;
    const apiKey = document.getElementById('weather-key').value;
    
    if (!location || !apiKey) {
        alert('Please enter both location and Weather API key');
        return;
    }
    
    showLoading();
    
    try {
        const weatherData = await getWeatherData(location, apiKey);
        displayWeatherInfo(weatherData);
    } catch (error) {
        console.error('Error getting weather info:', error);
        alert('Error getting weather information. Please try again.');
    } finally {
        hideLoading();
    }
}

// Display weather information
function displayWeatherInfo(weatherData) {
    const resultContainer = document.getElementById('weather-result');
    
    resultContainer.innerHTML = `
        <div class="weather-card">
            <h3>🌤️ Weather for ${weatherData.location}</h3>
            <div class="weather-details">
                <p><strong>Temperature:</strong> ${weatherData.temperature.toFixed(1)}°C</p>
                <p><strong>Humidity:</strong> ${weatherData.humidity.toFixed(1)}%</p>
                <p><strong>Condition:</strong> ${weatherData.condition}</p>
            </div>
        </div>
    `;
    
    resultContainer.style.display = 'block';
}

// Analyze soil
async function analyzeSoil() {
    const nitrogen = parseFloat(document.getElementById('soil-nitrogen').value) || 80;
    const phosphorus = parseFloat(document.getElementById('soil-phosphorus').value) || 40;
    const potassium = parseFloat(document.getElementById('soil-potassium').value) || 60;
    const ph = parseFloat(document.getElementById('soil-ph').value) || 6.5;
    
    showLoading();
    
    try {
        const response = await fetch('/api/soil-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                N: nitrogen,
                P: phosphorus,
                K: potassium,
                pH: ph
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displaySoilAnalysis(result.data);
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Soil analysis error:', error);
        alert('Error analyzing soil. Please try again.');
    } finally {
        hideLoading();
    }
}

// Get soil recommendations
function getSoilRecommendations(n, p, k, ph) {
    const recommendations = [];
    
    if (n < 60) recommendations.push('Nitrogen levels are low. Consider adding nitrogen-rich fertilizers.');
    if (p < 30) recommendations.push('Phosphorus levels are low. Add phosphorus fertilizers.');
    if (k < 50) recommendations.push('Potassium levels are low. Use potassium-rich fertilizers.');
    if (ph < 6.0) recommendations.push('Soil is acidic. Consider adding lime to increase pH.');
    if (ph > 8.0) recommendations.push('Soil is alkaline. Consider adding sulfur to decrease pH.');
    
    if (recommendations.length === 0) {
        recommendations.push('Soil conditions are optimal for most crops.');
    }
    
    return recommendations;
}

// Display soil analysis
function displaySoilAnalysis(analysis) {
    const resultContainer = document.getElementById('soil-result');
    
    resultContainer.innerHTML = `
        <div class="soil-analysis-card">
            <h3>🌱 Soil Analysis Results</h3>
            <div class="soil-values">
                <p><strong>Nitrogen (N):</strong> ${analysis.values.N}</p>
                <p><strong>Phosphorus (P):</strong> ${analysis.values.P}</p>
                <p><strong>Potassium (K):</strong> ${analysis.values.K}</p>
                <p><strong>pH Level:</strong> ${analysis.values.pH}</p>
            </div>
            <div class="soil-recommendations">
                <h4>📋 Recommendations:</h4>
                ${analysis.recommendations.map(rec => `<p>• ${rec}</p>`).join('')}
            </div>
        </div>
    `;
    
    resultContainer.style.display = 'block';
}

// Load market prices
async function loadMarketPrices() {
    try {
        const response = await fetch('/api/market-prices');
        const result = await response.json();
        
        if (result.success) {
            const marketGrid = document.getElementById('market-grid');
            
            marketGrid.innerHTML = result.data.map(item => `
                <div class="market-price-card">
                    <h3>${item.crop}</h3>
                    <p class="price">₹${item.price.toFixed(2)}/kg</p>
                    <p class="trend ${item.trend}">
                        ${item.trend === 'up' ? '↗' : item.trend === 'down' ? '↘' : '→'} 
                        ${item.change > 0 ? '+' : ''}${item.change.toFixed(1)}%
                    </p>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading market prices:', error);
    }
}

// Get pest control information
async function getPestControl() {
    const cropType = document.getElementById('crop-type').value;
    
    if (!cropType) {
        alert('Please select a crop type');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/pest-control', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ crop_type: cropType })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayPestControlInfo(cropType, result.data);
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Pest control error:', error);
        alert('Error getting pest control information.');
    } finally {
        hideLoading();
    }
}

// Display pest control information
function displayPestControlInfo(cropType, pestInfo) {
    const resultContainer = document.getElementById('pest-result');
    
    resultContainer.innerHTML = `
        <div class="pest-control-card">
            <h3>🐛 Pest Control for ${cropType.charAt(0).toUpperCase() + cropType.slice(1)}</h3>
            
            <div class="pest-section">
                <h4>Common Pests:</h4>
                <ul>
                    ${pestInfo.common_pests.map(pest => `<li>${pest}</li>`).join('')}
                </ul>
            </div>
            
            <div class="pest-section">
                <h4>Prevention:</h4>
                <p>${pestInfo.prevention}</p>
            </div>
            
            <div class="pest-section">
                <h4>Treatment:</h4>
                <p>${pestInfo.treatment}</p>
            </div>
        </div>
    `;
    
    resultContainer.style.display = 'block';
}

// Show add listing form
function showAddListing() {
    document.getElementById('add-listing-form').style.display = 'block';
}

// Cancel listing
function cancelListing() {
    document.getElementById('add-listing-form').style.display = 'none';
    clearListingForm();
}

// Clear listing form
function clearListingForm() {
    document.getElementById('listing-crop').value = '';
    document.getElementById('listing-quantity').value = '';
    document.getElementById('listing-price').value = '';
    document.getElementById('listing-contact').value = '';
    document.getElementById('listing-location').value = '';
}

// Add new listing
async function addListing() {
    const crop = document.getElementById('listing-crop').value;
    const quantity = document.getElementById('listing-quantity').value;
    const price = document.getElementById('listing-price').value;
    const contact = document.getElementById('listing-contact').value;
    const location = document.getElementById('listing-location').value;
    
    if (!crop || !quantity || !price || !contact || !location) {
        alert('Please fill in all fields');
        return;
    }
    
    try {
        const response = await fetch('/api/marketplace', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                crop_name: crop,
                quantity: parseInt(quantity),
                price: parseFloat(price),
                contact_info: contact,
                location_detail: location
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Listing added successfully!');
            loadMarketplaceListing();
            cancelListing();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Error adding listing:', error);
        alert('Error adding listing. Please try again.');
    }
}

// Load marketplace listings
async function loadMarketplaceListing() {
    try {
        const response = await fetch('/api/marketplace');
        const result = await response.json();
        
        if (result.success) {
            const marketplaceListings = document.getElementById('marketplace-listings');
            
            marketplaceListings.innerHTML = result.data.map(listing => `
                <div class="marketplace-card">
                    <h3>${listing.crop_name.charAt(0).toUpperCase() + listing.crop_name.slice(1)}</h3>
                    <p><strong>Quantity:</strong> ${listing.quantity} kg</p>
                    <p><strong>Price:</strong> ₹${listing.price.toFixed(2)}/kg</p>
                    <p><strong>Contact:</strong> ${listing.contact_info}</p>
                    <p><strong>Location:</strong> ${listing.location_detail}</p>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading marketplace listings:', error);
    }
}

// Refresh marketplace
function refreshMarketplace() {
    loadMarketplaceListing();
    alert('Marketplace refreshed successfully!');
}
