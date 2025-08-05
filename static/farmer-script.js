// Farmer Dashboard JavaScript
// Global variables
let currentLanguage = 'en';
let crops = [];
let weatherData = {};
let soilAnalysis = {};
let marketPrices = {};
let pestControlInfo = {};
let diseasePredictionData = {};


// Weekend Farming video upload
let uploadedVideosCount = 0;

function uploadFarmingVideo() {
    const fileInput = document.getElementById('video-upload');
    const titleInput = document.getElementById('video-title');
    const descriptionInput = document.getElementById('video-description');
    
    const files = fileInput.files;
    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();
    
    if (files.length === 0) {
        alert('Please select at least one video file to upload.');
        return;
    }
    
    if (!title) {
        alert('Please enter a video title.');
        return;
    }
    
    // Show progress bar
    const progressContainer = document.getElementById('upload-progress');
    const progressFill = document.getElementById('progress-fill');
    progressContainer.style.display = 'block';
    
    // Simulate upload process for demo
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 10;
        progressFill.style.width = progress + '%';
        
        if (progress >= 100) {
            clearInterval(progressInterval);
            
            // Simulate successful upload
            setTimeout(() => {
                uploadedVideosCount += files.length;
                alert(`Video(s) uploaded successfully! Total videos uploaded: ${uploadedVideosCount}`);
                
                // Check for prizes
                checkPrizeEligibility();
                
                // Clear form
                fileInput.value = '';
                titleInput.value = '';
                descriptionInput.value = '';
                progressContainer.style.display = 'none';
                progressFill.style.width = '0%';
                
            }, 500);
        }
    }, 200);
}

function checkPrizeEligibility() {
    let prizeMessage = '';
    
    if (uploadedVideosCount >= 3) {
        prizeMessage = '🎉 Congratulations! You\'ve unlocked the Gold Level prize: Premium Tool Kit + Cash Prize!';
    } else if (uploadedVideosCount >= 2) {
        prizeMessage = '🥈 Great! You\'ve unlocked the Silver Level prize: Fertilizer Vouchers!';
    } else if (uploadedVideosCount >= 1) {
        prizeMessage = '🥉 Awesome! You\'ve unlocked the Bronze Level prize: Free Seeds Package!';
    }
    
    if (prizeMessage) {
        setTimeout(() => {
            alert(prizeMessage);
        }, 1000);
    }
}

// Fetch latest agricultural news
function fetchLatestNews() {
    const newsFeed = document.getElementById('news-feed');
    const category = document.getElementById('news-category').value;
    
    // Show loading state
    newsFeed.innerHTML = `
        <div class="news-loading">
            <i class="fas fa-spinner fa-spin"></i>
            <h3>Fetching latest agricultural news...</h3>
            <p>Please wait while we load the most recent articles</p>
        </div>
    `;
    
    // Make actual API call to backend
    fetch('/api/agriculture-news', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.articles) {
            displayNewsArticles(data.articles, category);
        } else {
            // Fallback to sample news if API fails
            displaySampleNews(category);
        }
    })
    .catch(error => {
        console.error('Error fetching news:', error);
        // Fallback to sample news on error
        displaySampleNews(category);
    });
}

function displaySampleNews(category) {
    const newsFeed = document.getElementById('news-feed');
    
    // Sample news data (in real implementation, this would come from the API)
    const sampleNews = [
        {
            title: "New Government Subsidy Scheme for Organic Farming Launched",
            description: "The government has announced a new subsidy scheme to promote organic farming practices among farmers across the country.",
            source: "The Hindu",
            publishedAt: "2025-01-31T10:30:00Z",
            url: "https://example.com/news1",
            imageUrl: "https://via.placeholder.com/300x200?text=Organic+Farming"
        },
        {
            title: "Wheat Prices Rise by 15% in Major Agricultural Markets",
            description: "Wheat prices have shown a significant increase across major agricultural markets due to favorable weather conditions and increased demand.",
            source: "Indian Express",
            publishedAt: "2025-01-31T08:15:00Z",
            url: "https://example.com/news2",
            imageUrl: "https://via.placeholder.com/300x200?text=Wheat+Market"
        },
        {
            title: "Advanced Drone Technology for Crop Monitoring Introduced",
            description: "New drone technology has been introduced to help farmers monitor their crops more effectively and detect diseases early.",
            source: "Times of India",
            publishedAt: "2025-01-30T16:45:00Z",
            url: "https://example.com/news3",
            imageUrl: "https://via.placeholder.com/300x200?text=Drone+Technology"
        },
        {
            title: "Monsoon Forecast Predicts Normal Rainfall This Season",
            description: "The meteorological department has predicted normal rainfall this monsoon season, bringing relief to farmers across the country.",
            source: "Hindustan Times",
            publishedAt: "2025-01-30T12:20:00Z",
            url: "https://example.com/news4",
            imageUrl: "https://via.placeholder.com/300x200?text=Monsoon+Forecast"
        }
    ];
    
    // Filter news based on category (simplified)
    let filteredNews = sampleNews;
    if (category !== 'all') {
        filteredNews = sampleNews.filter(news => 
            news.title.toLowerCase().includes(category.toLowerCase()) ||
            news.description.toLowerCase().includes(category.toLowerCase())
        );
    }
    
    if (filteredNews.length === 0) {
        newsFeed.innerHTML = `
            <div class="news-empty">
                <i class="fas fa-exclamation-circle"></i>
                <h3>No news found for "${category}" category</h3>
                <p>Try selecting a different category or fetch all news</p>
            </div>
        `;
        return;
    }
    
    // Display news articles
    let newsHTML = `<div class="news-articles">`;
    
    filteredNews.forEach(article => {
        const publishedDate = new Date(article.publishedAt).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        newsHTML += `
            <div class="news-article">
                <div class="news-image">
                    <img src="${article.imageUrl}" alt="News Image" onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
                </div>
                <div class="news-content">
                    <h3>${article.title}</h3>
                    <p class="news-description">${article.description}</p>
                    <div class="news-meta">
                        <span class="news-source"><i class="fas fa-globe"></i> ${article.source}</span>
                        <span class="news-date"><i class="fas fa-calendar"></i> ${publishedDate}</span>
                    </div>
                    <a href="${article.url}" target="_blank" class="news-link">
                        <i class="fas fa-external-link-alt"></i> Read Full Article
                    </a>
                </div>
            </div>
        `;
    });
    
    newsHTML += `</div>`;
    newsFeed.innerHTML = newsHTML;
}
document.addEventListener('DOMContentLoaded', function() {
    initializeFarmerDashboard();
});

function initializeFarmerDashboard() {
    // Load farmer info
    loadFarmerInfo();
    
    // Load crops
    loadCrops();
    
    // Load weather data
    loadWeatherData();
    
    // Load soil analysis
    loadSoilAnalysis();
    
    // Load market prices
    loadMarketPrices();
    
    // Load pest control info
    loadPestControlInfo();
    
    // Initialize disease prediction
    initializeDiseasePrediction();
    
    // Set default language
    changeLanguage();
}

// Load farmer information
async function loadFarmerInfo() {
    try {
        const response = await fetch('/api/user-info');
        const result = await response.json();
        
        if (result.success) {
            const farmerName = document.getElementById('farmer-name');
            if (farmerName) {
                farmerName.textContent = `Welcome, ${result.data.name}!`;
            }
        }
    } catch (error) {
        console.error('Error loading farmer info:', error);
    }
}

// Load crops
async function loadCrops() {
    try {
        const response = await fetch('/api/crops');
        const result = await response.json();
        
        if (result.success) {
            crops = result.data;
            displayCrops(crops);
        }
    } catch (error) {
        console.error('Error loading crops:', error);
        // Display sample crops
        crops = [
            { id: 1, name: 'Wheat', type: 'cereal', status: 'growing', planted_date: '2024-01-15', harvest_date: '2024-06-15' },
            { id: 2, name: 'Corn', type: 'cereal', status: 'planted', planted_date: '2024-02-01', harvest_date: '2024-07-01' },
            { id: 3, name: 'Tomatoes', type: 'vegetable', status: 'harvested', planted_date: '2024-01-01', harvest_date: '2024-04-01' }
        ];
        displayCrops(crops);
    }
}

// Display crops
function displayCrops(cropList) {
    const cropsContainer = document.getElementById('crops-list');
    if (!cropsContainer) return;
    
    cropsContainer.innerHTML = cropList.map(crop => `
        <div class="crop-card">
            <div class="crop-info">
                <h4>${crop.name}</h4>
                <p>Type: ${crop.type}</p>
                <p>Status: <span class="status ${crop.status}">${crop.status}</span></p>
                <p>Planted: ${crop.planted_date}</p>
                <p>Harvest: ${crop.harvest_date}</p>
            </div>
            <div class="crop-actions">
                <button onclick="editCrop(${crop.id})" class="btn btn-secondary">Edit</button>
                <button onclick="deleteCrop(${crop.id})" class="btn btn-danger">Delete</button>
                <button onclick="viewCropDetails(${crop.id})" class="btn btn-primary">Details</button>
            </div>
        </div>
    `).join('');
}

// Add new crop
async function addCrop() {
    const name = document.getElementById('crop-name').value;
    const type = document.getElementById('crop-type').value;
    const plantedDate = document.getElementById('planted-date').value;
    const harvestDate = document.getElementById('harvest-date').value;
    
    if (!name || !type || !plantedDate || !harvestDate) {
        alert('Please fill in all fields');
        return;
    }
    
    const cropData = {
        name,
        type,
        planted_date: plantedDate,
        harvest_date: harvestDate,
        status: 'planted'
    };
    
    try {
        const response = await fetch('/api/crops', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cropData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Crop added successfully!');
            loadCrops();
            clearCropForm();
        } else {
            alert('Error adding crop: ' + result.message);
        }
    } catch (error) {
        console.error('Error adding crop:', error);
        alert('Error adding crop. Please try again.');
    }
}

// Clear crop form
function clearCropForm() {
    document.getElementById('crop-name').value = '';
    document.getElementById('crop-type').value = '';
    document.getElementById('planted-date').value = '';
    document.getElementById('harvest-date').value = '';
}

// Edit crop
function editCrop(cropId) {
    const crop = crops.find(c => c.id === cropId);
    if (!crop) return;
    
    const name = prompt('Edit crop name:', crop.name);
    const type = prompt('Edit crop type:', crop.type);
    const status = prompt('Edit crop status (planted/growing/harvested):', crop.status);
    
    if (name && type && status) {
        updateCrop(cropId, { name, type, status });
    }
}

// Update crop
async function updateCrop(cropId, cropData) {
    try {
        const response = await fetch(`/api/crops/${cropId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cropData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Crop updated successfully!');
            loadCrops();
        } else {
            alert('Error updating crop: ' + result.message);
        }
    } catch (error) {
        console.error('Error updating crop:', error);
        alert('Error updating crop. Please try again.');
    }
}

// Delete crop
async function deleteCrop(cropId) {
    if (!confirm('Are you sure you want to delete this crop?')) return;
    
    try {
        const response = await fetch(`/api/crops/${cropId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Crop deleted successfully!');
            loadCrops();
        } else {
            alert('Error deleting crop: ' + result.message);
        }
    } catch (error) {
        console.error('Error deleting crop:', error);
        alert('Error deleting crop. Please try again.');
    }
}

// View crop details
function viewCropDetails(cropId) {
    const crop = crops.find(c => c.id === cropId);
    if (!crop) return;
    
    alert(`Crop Details:\n\nName: ${crop.name}\nType: ${crop.type}\nStatus: ${crop.status}\nPlanted: ${crop.planted_date}\nHarvest: ${crop.harvest_date}`);
}

// Load weather data
async function loadWeatherData() {
    try {
        const response = await fetch('/api/weather');
        const result = await response.json();
        
        if (result.success) {
            weatherData = result.data;
            displayWeatherData(weatherData);
        }
    } catch (error) {
        console.error('Error loading weather data:', error);
        // Display sample weather data
        weatherData = {
            temperature: 25,
            humidity: 65,
            rainfall: 12.5,
            wind_speed: 8.2,
            forecast: 'Partly cloudy with chance of rain'
        };
        displayWeatherData(weatherData);
    }
}

// Display weather data
function displayWeatherData(weather) {
    const weatherContainer = document.getElementById('weather-info');
    if (!weatherContainer) return;
    
    weatherContainer.innerHTML = `
        <div class="weather-card">
            <h3>🌡️ Current Weather</h3>
            <div class="weather-details">
                <p><strong>Temperature:</strong> ${weather.temperature}°C</p>
                <p><strong>Humidity:</strong> ${weather.humidity}%</p>
                <p><strong>Rainfall:</strong> ${weather.rainfall}mm</p>
                <p><strong>Wind Speed:</strong> ${weather.wind_speed} km/h</p>
                <p><strong>Forecast:</strong> ${weather.forecast}</p>
            </div>
        </div>
    `;
}

// Load soil analysis
async function loadSoilAnalysis() {
    try {
        const response = await fetch('/api/soil-analysis');
        const result = await response.json();
        
        if (result.success) {
            soilAnalysis = result.data;
            displaySoilAnalysis(soilAnalysis);
        }
    } catch (error) {
        console.error('Error loading soil analysis:', error);
        // Display sample soil analysis
        soilAnalysis = {
            ph_level: 6.8,
            nitrogen: 45,
            phosphorus: 32,
            potassium: 38,
            organic_matter: 4.2,
            recommendations: 'Soil pH is optimal for most crops. Consider adding phosphorus fertilizer.'
        };
        displaySoilAnalysis(soilAnalysis);
    }
}

// Display soil analysis
function displaySoilAnalysis(soil) {
    const soilContainer = document.getElementById('soil-analysis');
    if (!soilContainer) return;
    
    soilContainer.innerHTML = `
        <div class="soil-card">
            <h3>🌱 Soil Analysis</h3>
            <div class="soil-details">
                <p><strong>pH Level:</strong> ${soil.ph_level}</p>
                <p><strong>Nitrogen:</strong> ${soil.nitrogen}%</p>
                <p><strong>Phosphorus:</strong> ${soil.phosphorus}%</p>
                <p><strong>Potassium:</strong> ${soil.potassium}%</p>
                <p><strong>Organic Matter:</strong> ${soil.organic_matter}%</p>
                <div class="soil-recommendations">
                    <strong>Recommendations:</strong>
                    <p>${soil.recommendations}</p>
                </div>
            </div>
        </div>
    `;
}

// Load market prices
async function loadMarketPrices() {
    try {
        const response = await fetch('/api/market-prices');
        const result = await response.json();
        
        if (result.success) {
            marketPrices = result.data;
            displayMarketPrices(marketPrices);
        }
    } catch (error) {
        console.error('Error loading market prices:', error);
        // Display sample market prices
        marketPrices = [
            { crop: 'Wheat', price: 250, unit: 'per quintal', trend: 'up' },
            { crop: 'Corn', price: 180, unit: 'per quintal', trend: 'stable' },
            { crop: 'Tomatoes', price: 45, unit: 'per kg', trend: 'down' },
            { crop: 'Rice', price: 320, unit: 'per quintal', trend: 'up' }
        ];
        displayMarketPrices(marketPrices);
    }
}

// Display market prices
function displayMarketPrices(prices) {
    const pricesContainer = document.getElementById('market-prices');
    if (!pricesContainer) return;
    
    pricesContainer.innerHTML = `
        <div class="prices-card">
            <h3>💰 Market Prices</h3>
            <div class="prices-list">
                ${prices.map(price => `
                    <div class="price-item">
                        <span class="crop-name">${price.crop}</span>
                        <span class="price-value">₹${price.price} ${price.unit}</span>
                        <span class="price-trend ${price.trend}">${price.trend === 'up' ? '📈' : price.trend === 'down' ? '📉' : '➡️'}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Load pest control info
async function loadPestControlInfo() {
    try {
        const response = await fetch('/api/pest-control');
        const result = await response.json();
        
        if (result.success) {
            pestControlInfo = result.data;
            displayPestControlInfo(pestControlInfo);
        }
    } catch (error) {
        console.error('Error loading pest control info:', error);
        // Display sample pest control info
        pestControlInfo = [
            { pest: 'Aphids', crop: 'Wheat', treatment: 'Neem oil spray', severity: 'low' },
            { pest: 'Corn Borer', crop: 'Corn', treatment: 'Bt spray', severity: 'medium' },
            { pest: 'Whitefly', crop: 'Tomatoes', treatment: 'Yellow sticky traps', severity: 'high' }
        ];
        displayPestControlInfo(pestControlInfo);
    }
}

// Display pest control info
function displayPestControlInfo(pestInfo) {
    const pestContainer = document.getElementById('pest-control');
    if (!pestContainer) return;
    
    pestContainer.innerHTML = `
        <div class="pest-card">
            <h3>🐛 Pest Control</h3>
            <div class="pest-list">
                ${pestInfo.map(pest => `
                    <div class="pest-item">
                        <div class="pest-info">
                            <h4>${pest.pest}</h4>
                            <p><strong>Crop:</strong> ${pest.crop}</p>
                            <p><strong>Treatment:</strong> ${pest.treatment}</p>
                            <p><strong>Severity:</strong> <span class="severity ${pest.severity}">${pest.severity}</span></p>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Get crop recommendations
async function getCropRecommendations() {
    const location = document.getElementById('location').value;
    const season = document.getElementById('season').value;
    
    if (!location || !season) {
        alert('Please enter location and select season');
        return;
    }
    
    try {
        const response = await fetch('/api/crop-recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ location, season })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayCropRecommendations(result.data);
        } else {
            alert('Error getting recommendations: ' + result.message);
        }
    } catch (error) {
        console.error('Error getting crop recommendations:', error);
        // Display sample recommendations
        displayCropRecommendations([
            { crop: 'Wheat', suitability: 'High', expected_yield: '45 quintals/hectare' },
            { crop: 'Barley', suitability: 'Medium', expected_yield: '35 quintals/hectare' },
            { crop: 'Mustard', suitability: 'High', expected_yield: '20 quintals/hectare' }
        ]);
    }
}

// Display crop recommendations
function displayCropRecommendations(recommendations) {
    const recommendationsContainer = document.getElementById('crop-recommendations');
    if (!recommendationsContainer) return;
    
    recommendationsContainer.innerHTML = `
        <div class="recommendations-card">
            <h3>🌾 Crop Recommendations</h3>
            <div class="recommendations-list">
                ${recommendations.map(rec => `
                    <div class="recommendation-item">
                        <h4>${rec.crop}</h4>
                        <p><strong>Suitability:</strong> <span class="suitability ${rec.suitability.toLowerCase()}">${rec.suitability}</span></p>
                        <p><strong>Expected Yield:</strong> ${rec.expected_yield}</p>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
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
    if (!languageSelect) return;
    
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

// Initialize disease prediction
function initializeDiseasePrediction() {
    // Set up auto-fill from recommendation results
    const recommendationForm = document.getElementById('recommendation-result');
    if (recommendationForm) {
        // Monitor for changes to automatically fill disease prediction form
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    autofillDiseaseForm();
                }
            });
        });
        observer.observe(recommendationForm, { childList: true, subtree: true });
    }
}

// Auto-fill disease prediction form from crop recommendation results
function autofillDiseaseForm() {
    // Get recommendation data if available
    const recResult = document.getElementById('recommendation-result');
    if (recResult && recResult.style.display !== 'none') {
        // Extract data from recommendation result
        const tempElement = recResult.querySelector('.temp-value');
        const humidityElement = recResult.querySelector('.humidity-value');
        const rainfallElement = recResult.querySelector('.rainfall-value');
        const cropElement = recResult.querySelector('.recommended-crop');
        
        if (tempElement) {
            document.getElementById('disease-temp').value = tempElement.textContent.replace('°C', '').trim();
        }
        if (humidityElement) {
            document.getElementById('disease-humidity').value = humidityElement.textContent.replace('%', '').trim();
        }
        if (rainfallElement) {
            document.getElementById('disease-rainfall').value = rainfallElement.textContent.replace('mm', '').trim();
        }
        if (cropElement) {
            const cropName = cropElement.textContent.toLowerCase().trim();
            const cropSelect = document.getElementById('disease-crop-type');
            if (cropSelect) {
                cropSelect.value = cropName;
            }
        }
    }
}

// Predict disease for selected crop
async function predictDisease() {
    const cropType = document.getElementById('disease-crop-type').value;
    const temperature = parseFloat(document.getElementById('disease-temp').value);
    const humidity = parseFloat(document.getElementById('disease-humidity').value);
    const rainfall = parseFloat(document.getElementById('disease-rainfall').value);
    const windSpeed = parseFloat(document.getElementById('disease-wind').value);
    const ph = parseFloat(document.getElementById('disease-ph').value);
    
    if (!cropType) {
        alert('Please select a crop type');
        return;
    }
    
    if (isNaN(temperature) || isNaN(humidity) || isNaN(rainfall) || isNaN(windSpeed) || isNaN(ph)) {
        alert('Please fill in all environmental parameters with valid numbers');
        return;
    }
    
    const diseaseData = {
        crop_name: cropType,
        temperature: temperature,
        humidity: humidity,
        rainfall: rainfall,
        wind_speed: windSpeed,
        specific_humidity: 0.01, // Default value
        ph: ph
    };
    
    try {
        showLoadingSpinner();
        
        const response = await fetch('/api/predict-disease', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(diseaseData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayDiseaseResult(result.data);
        } else {
            alert('Error predicting disease: ' + result.message);
        }
    } catch (error) {
        console.error('Disease prediction error:', error);
        // Use client-side prediction as fallback
        const clientResult = predictDiseaseClientSide(diseaseData);
        displayDiseaseResult(clientResult);
    } finally {
        hideLoadingSpinner();
    }
}

// Client-side disease prediction as fallback
function predictDiseaseClientSide(data) {
    const { crop_name, temperature, humidity, rainfall, wind_speed, ph } = data;
    
    // Simple rule-based prediction system
    const diseaseRules = {
        'rice': {
            'blast': {
                conditions: temperature >= 20 && temperature <= 30 && humidity >= 85 && rainfall >= 100,
                prevention: ['Use resistant varieties', 'Proper field drainage', 'Balanced nitrogen application']
            },
            'bacterial_blight': {
                conditions: temperature >= 25 && temperature <= 35 && humidity >= 80 && wind_speed <= 10,
                prevention: ['Use disease-free seeds', 'Avoid excessive nitrogen', 'Maintain proper plant spacing']
            }
        },
        'wheat': {
            'rust': {
                conditions: temperature >= 15 && temperature <= 25 && humidity >= 70 && rainfall >= 50 && rainfall <= 200,
                prevention: ['Use resistant varieties', 'Crop rotation', 'Fungicide spray if needed']
            }
        },
        'tomato': {
            'late_blight': {
                conditions: temperature >= 10 && temperature <= 25 && humidity >= 75 && rainfall >= 50,
                prevention: ['Use certified seeds', 'Proper ventilation', 'Copper-based fungicides']
            }
        },
        'maize': {
            'rust': {
                conditions: temperature >= 20 && temperature <= 30 && humidity >= 60 && wind_speed >= 5,
                prevention: ['Resistant hybrids', 'Timely planting', 'Field sanitation']
            }
        },
        'cotton': {
            'wilt': {
                conditions: temperature >= 25 && temperature <= 35 && humidity >= 40 && humidity <= 70 && ph >= 6 && ph <= 8,
                prevention: ['Use resistant varieties', 'Soil treatment', 'Proper irrigation']
            }
        }
    };
    
    const cropDiseases = diseaseRules[crop_name.toLowerCase()];
    if (cropDiseases) {
        for (const [disease, rule] of Object.entries(cropDiseases)) {
            if (rule.conditions) {
                return {
                    disease: disease,
                    risk_level: 'High',
                    risk_factors: ['temperature', 'humidity', 'rainfall'],
                    prevention: rule.prevention
                };
            }
        }
    }
    
    // Default healthy response
    return {
        disease: 'healthy',
        risk_level: 'Low',
        risk_factors: [],
        prevention: [
            'Monitor plants regularly',
            'Maintain proper field hygiene',
            'Use quality seeds',
            'Follow proper irrigation practices'
        ]
    };
}

// Display disease prediction results
function displayDiseaseResult(diseaseData) {
    const resultContainer = document.getElementById('disease-result');
    if (!resultContainer) return;
    
    // Initialize variables
    let diseaseInfo, riskLevel, pesticides, preventionTips, forecast;
    
    // Handle both old and new data structures
    if (diseaseData.diseases && diseaseData.diseases.length > 0) {
        // New comprehensive structure
        const primaryDisease = diseaseData.diseases[0];
        diseaseInfo = primaryDisease.disease;
        riskLevel = primaryDisease.risk_level;
        pesticides = primaryDisease.prevention.pesticides || ['Consult agricultural expert'];
        preventionTips = primaryDisease.prevention.management || primaryDisease.prevention.critical_stage || ['Monitor regularly'];
        forecast = diseaseData.forecast_7days;
    } else {
        // Old simple structure
        diseaseInfo = diseaseData.disease || 'Unknown';
        riskLevel = diseaseData.risk_level || 'Low';
        pesticides = diseaseData.pesticides || ['Consult agricultural expert'];
        preventionTips = diseaseData.prevention || ['Monitor regularly'];
        forecast = null;
    }
    
    const riskColor = {
        'High': '#dc3545',
        'Medium': '#ffc107',
        'Low': '#28a745',
        'Unknown': '#6c757d'
    };
    
    const diseaseIcon = diseaseInfo === 'healthy' ? '✓' : '⚠';
    const riskBadgeColor = riskColor[riskLevel] || '#6c757d';
    
    let forecastHtml = '';
    if (forecast && forecast.forecast_available) {
        forecastHtml = `
            <div class="forecast-section">
                <h4>CALENDAR 7-Day Disease Risk Forecast</h4>
                <div class="forecast-summary">
                    <p><strong>Summary:</strong></p>
                    <ul>
                        <li>High Risk Days: ${forecast.summary.high_risk_days}</li>
                        <li>Medium Risk Days: ${forecast.summary.medium_risk_days}</li>
                        <li>Low Risk Days: ${forecast.summary.low_risk_days}</li>
                    </ul>
                </div>
                <div class="forecast-days">
                    ${forecast.forecast_days.map(day => `
                        <div class="forecast-day risk-${day.risk_level.toLowerCase()}">
                            <strong>Day ${day.day}</strong><br>
                            Temp: ${day.temperature}C<br>
                            Humidity: ${day.humidity}%<br>
                            Risk: ${day.risk_level}
                        </div>
                    `).join('')}
                </div>
                <div class="forecast-recommendations">
                    <h5>Recommendations:</h5>
                    <ul>
                        ${forecast.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }
    
    resultContainer.innerHTML = `
        <div class="disease-prediction-card">
            <div class="disease-header">
                <h3>${diseaseIcon} Disease Prediction Results</h3>
                <div class="risk-badge" style="background-color: ${riskBadgeColor}">
                    Risk Level: ${riskLevel}
                </div>
            </div>
            
            <div class="disease-content">
                <div class="disease-info">
                    <h4>MICROBE Predicted Condition</h4>
                    <p class="disease-name">${diseaseInfo.replace('_', ' ').toUpperCase()}</p>
                </div>
                
                <div class="pesticide-recommendations">
                    <h4>BOTTLE Recommended Pesticides/Fungicides</h4>
                    <div class="pesticide-list">
                        ${pesticides.map(pesticide => `<span class="pesticide-tag">${pesticide}</span>`).join('')}
                    </div>
                </div>
                
                <div class="prevention-tips">
                    <h4>SHIELD Prevention & Management Tips</h4>
                    <ul class="prevention-list">
                        ${preventionTips.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
                
                ${forecastHtml}
                
                <!-- After 7 days Conditions Section -->
                \u003cdiv style="border: 2px solid #28a745; padding: 15px; margin: 20px 0; border-radius: 8px; background: #f0f8f0;"\u003e
                    \u003ch3 style="text-align: center; color: #28a745; margin-bottom: 15px;"\u003e🔮 After 7 Days Conditions\u003c/h3\u003e
                    \u003cdiv style="background: #ffffff; padding: 15px; border-radius: 5px; border-left: 4px solid #28a745;"\u003e
                        \u003ch4 style="color: #28a745;"\u003e📈 Expected Disease Progression:\u003c/h4\u003e
                        ${diseaseInfo !== 'healthy' ? `
                            \u003cdiv style="margin: 10px 0;"\u003e
                                \u003cp\u003e\u003cstrong\u003e🔍 Disease Development:\u003c/strong\u003e Based on current conditions, \u003cem\u003e${diseaseInfo.replace('_', ' ')}\u003c/em\u003e may progress from ${riskLevel.toLowerCase()} to potentially higher risk levels if environmental conditions remain favorable.\u003c/p\u003e
                                \u003cp\u003e\u003cstrong\u003e🌡️ Weather Impact:\u003c/strong\u003e Temperature and humidity patterns over the next 7 days will be critical factors in disease development.\u003c/p\u003e
                                \u003cp\u003e\u003cstrong\u003e⚠️ Critical Days:\u003c/strong\u003e Days 3-5 are typically most critical for disease establishment and spread.\u003c/p\u003e
                            \u003c/div\u003e
                            \u003cdiv style="background: #fff3cd; padding: 10px; border-radius: 5px; border-left: 3px solid #ffc107;"\u003e
                                \u003ch5 style="color: #856404;"\u003e🎯 What to Expect:\u003c/h5\u003e
                                \u003cul style="margin: 5px 0; padding-left: 20px;"\u003e
                                    \u003cli\u003eSymptom visibility may increase if conditions remain favorable\u003c/li\u003e
                                    \u003cli\u003eDisease spread rate will depend on humidity and temperature patterns\u003c/li\u003e
                                    \u003cli\u003eEarly intervention in next 2-3 days can significantly reduce impact\u003c/li\u003e
                                    \u003cli\u003eMonitor plants daily for early symptom detection\u003c/li\u003e
                                \u003c/ul\u003e
                            \u003c/div\u003e
                            \u003cdiv style="background: #d1ecf1; padding: 10px; border-radius: 5px; border-left: 3px solid #17a2b8; margin-top: 10px;"\u003e
                                \u003ch5 style="color: #0c5460;"\u003e💊 Preventive Action Timeline:\u003c/h5\u003e
                                \u003cul style="margin: 5px 0; padding-left: 20px;"\u003e
                                    \u003cli\u003e\u003cstrong\u003eDay 1-2:\u003c/strong\u003e Apply recommended pesticides: ${pesticides.slice(0, 2).join(', ')}\u003c/li\u003e
                                    \u003cli\u003e\u003cstrong\u003eDay 3-4:\u003c/strong\u003e Monitor for early symptoms and adjust irrigation\u003c/li\u003e
                                    \u003cli\u003e\u003cstrong\u003eDay 5-7:\u003c/strong\u003e Evaluate effectiveness and repeat treatment if necessary\u003c/li\u003e
                                \u003c/ul\u003e
                            \u003c/div\u003e
                        ` : `
                            \u003cdiv style="margin: 10px 0;"\u003e
                                \u003cp\u003e\u003cstrong\u003e✅ Healthy Outlook:\u003c/strong\u003e Current conditions suggest your crop will likely remain healthy over the next 7 days.\u003c/p\u003e
                                \u003cp\u003e\u003cstrong\u003e🌱 Maintenance:\u003c/strong\u003e Continue with regular monitoring and preventive care practices.\u003c/p\u003e
                                \u003cp\u003e\u003cstrong\u003e📊 Risk Assessment:\u003c/strong\u003e Low probability of disease development based on current environmental conditions.\u003c/p\u003e
                            \u003c/div\u003e
                            \u003cdiv style="background: #d4edda; padding: 10px; border-radius: 5px; border-left: 3px solid #28a745;"\u003e
                                \u003ch5 style="color: #155724;"\u003e🌟 Recommended Actions:\u003c/h5\u003e
                                \u003cul style="margin: 5px 0; padding-left: 20px;"\u003e
                                    \u003cli\u003eMaintain current irrigation and fertilization schedule\u003c/li\u003e
                                    \u003cli\u003eContinue regular field inspections\u003c/li\u003e
                                    \u003cli\u003eKeep preventive treatments ready in case conditions change\u003c/li\u003e
                                    \u003cli\u003eMonitor weather forecasts for any sudden changes\u003c/li\u003e
                                \u003c/ul\u003e
                            \u003c/div\u003e
                        `}
                    \u003c/div\u003e
                \u003c/div\u003e
                
                ${diseaseInfo !== 'healthy' ? `
                    <div class="treatment-advice">
                        <h4>HOSPITAL Treatment Recommendations</h4>
                        <div class="alert alert-warning">
                            <strong>Important:</strong> Consult with local agricultural experts or extension officers for specific treatment plans. This prediction is based on environmental conditions and should be used as a preliminary assessment.
                        </div>
                    </div>
                ` : `
                    <div class="healthy-status">
                        <div class="alert alert-success">
                            <strong>Good News!</strong> Current conditions suggest low disease risk. Continue with regular monitoring and preventive practices.
                        </div>
                    </div>
                `}
            </div>
        </div>
    `;
    
    resultContainer.style.display = 'block';
}

// Show loading spinner
function showLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.style.display = 'flex';
    }
}

// Hide loading spinner
function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.style.display = 'none';
    }
}

// Refresh dashboard
function refreshDashboard() {
    loadCrops();
    loadWeatherData();
    loadSoilAnalysis();
    loadMarketPrices();
    loadPestControlInfo();
    alert('Dashboard refreshed successfully!');
}
