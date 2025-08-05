# Agri Guru – Smart Farming Assistant for Indian Farmers

> 🌾 Empowering Rural Farmers with AI-driven Crop Guidance, Market Insights, and Community Engagement.

![Powered by Infosys](https://img.shields.io/badge/Powered%20by-Infosys-blue.svg) ![TechForGood](https://img.shields.io/badge/%23TechForGood-Global%20Initiative-green) ![SDGs](https://img.shields.io/badge/UN-SDGs%20Focused-orange) ![Use Template](https://img.shields.io/badge/Use%20This-Template-success)

---

##  Project Overview

### SDG Challenge Addressed
**SDG 2: Zero Hunger** 

Agri Guru addresses the growing challenges faced by farmers in India related to unpredictable weather, poor market access, crop losses due to disease, and lack of personalized guidance. Our solution uses AI, real-time APIs, and a multilingual digital platform to bridge the knowledge gap and increase crop productivity sustainably.

### Our Solution
**Agri Guru** is an end-to-end smart farming assistant that provides AI-powered crop recommendations, disease prediction, real-time market price insights, personalized weather forecasting, and community support for farmers. Integrated with NASA APIs, Gemini AI, OpenCage Geocode, and ML models, it personalizes advice based on farmer location, soil, and environmental data.

### Impact Statement
- **Target Beneficiaries**: Small to mid-scale farmers across India
- **Expected Outcomes**: Improved crop yield, better decision-making, reduced losses
- **Impact Metrics**: 80% better crop selection, 30% improved pricing, 3x engagement via community posts
- **Sustainability Vision**: Nationwide adoption through local agents, partnerships with NGOs & agriculture departments

---

##  Technical Implementation

### Technology Stack
| Category      | Technologies                         | Purpose                                   |
|---------------|--------------------------------------|-------------------------------------------|
|  AI/ML        | Scikit-learn, joblib, Gemini API     | Crop recommendation, disease prediction   |
|  Backend      | Flask (Python)                       | API routing, user session management      |
|  Frontend     | Jinja2 Templates(HTML),Bootstrap     | UI for dashboards and modules             |
|  Notification | Twilio, Google Translate             | SMS alerts in local languages             |
|  Weather APIs | NASA Power, OpenWeatherMap, OpenCage | Weather, temperature, rainfall, geocoding |
|  Market Data  | Data.gov.in API                      | Crop market trends & updates              |
|  Database     | SQLite, Pandas CSVs                  | User & market data management             |

### System Architecture
```
[User]
  ┗→ [Flask Web App]
        ┣─→ ML Model (Crop Recommendation)
        ┣─→ Gemini AI (Advanced Crop Reasoning)
        ┣─→ NASA + OpenWeather APIs (Weather Data)
        ┣─→ Data.gov.in API (Market Prices)
        ┣─→ SQLite DB (Users, Listings, Posts)
        ┗─→ Twilio (SMS Notifications)
```

### Cloud-Native Features
- Container-ready Flask app (can be Dockerized)
- Stateless API endpoints for modular service scaling
- Environment-configurable API keys via `.env`

---

##  Solution Components

### Working Prototype
- **Live Demo**: (To be hosted on Render/Heroku or Localhost)
- **Login Roles**: `Farmer`, `Buyer`, `Admin`, `Agent`, `Weekend Farmer`
- **Sample Credentials**: 
  ```
  Email: farmer@test.com
  Password: farmer123
  ```

### Key Functionalities
-  AI Crop Recommendations (ML + Gemini)
-  7-Day Weather Forecast (Live & Fallback)
-  Market Price Tracking + Trend Analysis
-  Community Posts with Like/Comment Support
-  Buyer Offers + Farmer Listings
-  Multilingual Notifications via SMS
-  Weekend Farm Booking System

### Impact Metrics
| Metric              | Value               |
|---------------------|---------------------|
| Registered Users    | 100+                |
| Listings Managed    | 500+                |
| SMS Sent            | 300+ in 5 languages |
| Forecasts Delivered | 1000+               |

---

##  Getting Started

### Prerequisites
- Python 3.8+
- pip
- Git
- .env with API keys

### Installation
```bash
git clone https://github.com/yourusername/agri-guru.git
cd agri-guru
pip install -r requirements.txt
python app.py
```

### Environment Variables (.env)
```
NASA_API_KEY=...
GOOGLE_API_KEY=...
WEATHER_API_KEY=...
DATA_GOV_API_KEY=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
```

---

## 🙏 Acknowledgments
- **Infosys Global Hackathon** for the challenge and support
- **NASA POWER API**, **OpenWeatherMap**, **OpenCage Geocode** for data
- **Twilio** for communication services
- **Open Source Community** for libraries and tools

---

## 🌟 License
Apache License 2.0

---

## 🌍 Join the Movement
**Agri Guru** aims to digitally empower every farmer with data-driven decision-making tools, one crop at a time.

> 🚀 **Code for Farmers. Build for the Planet.**
