# Smart Farming Assistant - Portable Deployment Guide

## 🚀 Quick Start (Making it Portable)

### Step 1: Run the Portable Setup Script
```bash
python portable_setup.py
```

This script will:
- ✅ Fix hardcoded paths
- ✅ Create proper directory structure
- ✅ Find and copy data files
- ✅ Install dependencies
- ✅ Train models if needed
- ✅ Create run scripts for different platforms

### Step 2: Copy Project Anywhere
After running the setup script, you can copy the entire project folder to:
- ✅ Any location on the same computer
- ✅ Different computers (Windows, Linux, Mac)
- ✅ USB drives, cloud storage, etc.

### Step 3: Run the Application
**Windows:**
```cmd
run_windows.bat
```

**Linux/Mac:**
```bash
./run_unix.sh
```

**Manual (any platform):**
```bash
streamlit run app.py
```

---

## 📁 Required Files for Portability

Make sure these files/folders are included when copying:

### Core Application Files
- `app.py` - Main application
- `database.py` - Database management
- `requirements.txt` - Python dependencies
- `config.py` - Configuration settings (created by setup)

### Data Files
- `data/` folder with:
  - `train.csv` - Soil training data
  - `test.csv` - Test data
  - `sample_submission.csv` - Sample submission format
  - `soil_data.csv` - Soil reference data
  - `market_prices.csv` - Market price data
  - `pesticides.csv` - Pesticide data

### Model Files
- `crop_recommendation_model.pkl` - Trained ML model
- `enhanced_crop_model.pkl` - Enhanced model
- `water_resource_encoder.pkl` - Water resource encoder

### Optional Files
- `smart_farming.db` - Database (created automatically)
- `run_windows.bat` - Windows run script
- `run_unix.sh` - Linux/Mac run script

---

## 🔧 Manual Setup (Without Script)

If you prefer to set up manually:

### 1. Fix the Hardcoded Path
The main issue is in `app.py` line 1103. The hardcoded path:
```python
soil_df = pd.read_csv(r"C:\Users\navya\Downloads\playground-series-s5e6\train.csv")
```

Should be replaced with (already fixed in the current version):
```python
# Try multiple possible paths
possible_paths = [
    "playground-series-s5e6/train.csv",
    "../playground-series-s5e6/train.csv", 
    "data/train.csv",
    "train.csv"
]

for path in possible_paths:
    if os.path.exists(path):
        soil_df = pd.read_csv(path)
        break
```

### 2. Create Directory Structure
```
smart-farming-assistant/
├── app.py
├── database.py
├── requirements.txt
├── data/
│   ├── train.csv
│   ├── test.csv
│   ├── sample_submission.csv
│   ├── soil_data.csv
│   ├── market_prices.csv
│   └── pesticides.csv
├── models/ (optional)
└── logs/ (optional)
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train Models (if needed)
```bash
python train_model.py
```

---

## 🌍 Cross-Platform Compatibility

### Windows
- ✅ Works with Python 3.8+
- ✅ Uses `run_windows.bat` script
- ✅ Handles Windows path separators

### Linux/Mac
- ✅ Works with Python 3.8+
- ✅ Uses `run_unix.sh` script
- ✅ Handles Unix path separators

### Cloud/Docker
- ✅ Can be containerized
- ✅ Environment variables supported
- ✅ Relative paths work in containers

---

## 📊 Data File Locations

The app will automatically search for `train.csv` in these locations:
1. `playground-series-s5e6/train.csv`
2. `../playground-series-s5e6/train.csv`
3. `data/train.csv`
4. `train.csv` (current directory)

**Recommendation:** Copy `train.csv` to the `data/` folder for best portability.

---

## 🔑 API Key Setup

1. Get your API key from [WeatherAPI](https://www.weatherapi.com/)
2. When you run the app, enter the API key in the sidebar
3. The app will store it for the session

---

## 🐛 Troubleshooting

### "File not found" errors
- Ensure all data files are in the correct locations
- Run `python portable_setup.py` to auto-fix paths

### "Module not found" errors
- Run `pip install -r requirements.txt`
- Ensure Python 3.8+ is installed

### API/Weather errors
- Check your WeatherAPI key
- Ensure internet connection is available

### Database errors
- The app will create `smart_farming.db` automatically
- Ensure write permissions in the project folder

---

## ✅ Portability Checklist

Before copying to a new location:

- [ ] Run `portable_setup.py` script
- [ ] All data files in `data/` folder
- [ ] Model files (.pkl) present
- [ ] Dependencies installed
- [ ] Database file included (or will be created)
- [ ] Configuration file created
- [ ] Run scripts created

After copying:

- [ ] Test with `streamlit run app.py`
- [ ] Verify all features work
- [ ] Check API key functionality
- [ ] Confirm database operations

---

## 🎯 Best Practices

1. **Always use the portable setup script** before distributing
2. **Keep the complete project folder** - don't copy individual files
3. **Test on the target system** before assuming it will work
4. **Include the WeatherAPI key** in documentation for end users
5. **Use relative paths** for any new file references

---

## 📞 Support

If you encounter issues with portability:
1. Check the troubleshooting section
2. Verify all files are included
3. Test the portable setup script
4. Ensure proper Python version (3.8+)

The project is now designed to be **fully portable** across different systems and locations! 🎉
