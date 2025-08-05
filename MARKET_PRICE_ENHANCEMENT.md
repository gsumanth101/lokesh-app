# 🌾 Enhanced Market Price Management System

## Overview

The Smart Farming Assistant now includes a comprehensive market price management system that allows agents to update market prices with detailed logging, automatic farmer notifications, and comprehensive analytics.

## 🆕 New Features

### 1. **Enhanced Agent Market Management Dashboard**
- **Multi-tab Interface**: Current Prices, Update Prices, Price History, Notifications
- **Real-time Price Updates**: Agents can update market prices instantly
- **Smart Notifications**: Automatic SMS notifications to farmers
- **Comprehensive Logging**: All price changes are logged with detailed information

### 2. **Market Price Logging System**
- **Detailed Logs**: Every price update is tracked with:
  - Old and new prices
  - Price change percentage
  - Trend changes
  - Agent information (who made the update)
  - Timestamp
  - Reason for update
- **Price History**: View historical price changes over time
- **Recent Changes Summary**: Quick overview of recent market movements

### 3. **Intelligent Notification System**
- **Automatic SMS Alerts**: Farmers receive instant notifications when prices change
- **Smart Filtering**: Only send notifications for significant price changes (configurable threshold)
- **Custom Messages**: Agents can send custom market alerts to farmers
- **Targeted Notifications**: Send notifications to farmers growing specific crops

### 4. **Enhanced Database Schema**
- **New Table**: `market_price_logs` for comprehensive price tracking
- **Foreign Key Relationships**: Proper data integrity
- **Optimized Queries**: Fast retrieval of price history and analytics

## 🔧 Technical Implementation

### Database Schema
```sql
CREATE TABLE market_price_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_name TEXT NOT NULL,
    old_price REAL,
    new_price REAL NOT NULL,
    old_trend TEXT,
    new_trend TEXT NOT NULL,
    updated_by_user_id INTEGER NOT NULL,
    updated_by_name TEXT NOT NULL,
    updated_by_role TEXT NOT NULL,
    update_reason TEXT,
    update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price_change_percent REAL,
    FOREIGN KEY (updated_by_user_id) REFERENCES users (id)
);
```

### Key Functions

#### Agent Market Management
- `show_agent_market_management()`: Main dashboard for agents
- `send_market_update_to_farmers()`: Send SMS notifications to farmers
- `get_farmers_for_notification()`: Get list of farmers to notify

#### Database Operations
- `update_market_price()`: Update prices with enhanced logging
- `log_market_price_update()`: Log price changes to database
- `get_market_price_logs()`: Retrieve price update history
- `get_recent_price_changes()`: Get recent price movements

## 🚀 How to Use

### For Agents

1. **Login as Agent**
   - Use: `agent@smartfarm.com` / `agent123`

2. **Navigate to Market Management**
   - Go to "Manage Market" tab in Agent Dashboard

3. **Update Market Prices**
   - Select crop from dropdown
   - Enter new price (₹/quintal)
   - Choose price trend (Stable, Increasing, Decreasing, Volatile)
   - Add reason for update (optional)
   - Configure notification settings
   - Click "Update Market Price"

4. **View Price History**
   - Check "Price History" tab for detailed logs
   - Filter by crop or view all changes
   - See recent changes summary

5. **Send Custom Notifications**
   - Use "Notifications" tab
   - Compose custom message
   - Target specific crop farmers or all farmers
   - Mark as urgent if needed

### For Farmers

1. **Receive Automatic Notifications**
   - Get instant SMS when prices change
   - Receive notifications for crops you're growing
   - View updated prices in "Market Prices" tab

2. **View Market Dashboard**
   - Check current market prices
   - See price trends and last updated information
   - Make informed selling decisions

## 📊 Dashboard Features

### Current Prices Tab
- Enhanced price display with trend indicators
- Price trend summary (Increasing, Decreasing, Volatile, Stable)
- Visual indicators for price movements

### Update Prices Tab
- Real-time price reference
- Price change calculation
- Notification settings
- Update reason tracking

### Price History Tab
- Comprehensive price logs
- Filterable by crop and date range
- Recent changes summary (last 7 days)
- Price change analytics

### Notifications Tab
- Notification settings management
- Custom message composer
- Targeted farmer notifications
- Urgent message flagging

## 🔔 Notification System

### Automatic Notifications
When an agent updates market prices:
1. **Price Change Calculation**: System calculates percentage change
2. **Threshold Check**: Only sends notifications for significant changes (default: 5%)
3. **Message Composition**: Creates informative message with:
   - Crop name
   - New price
   - Price trend
   - Percentage change
   - Agent information
4. **SMS Delivery**: Sends to relevant farmers via Twilio

### Notification Message Format
```
Market Alert: Wheat price updated to ₹1200/quintal (Trend: Increasing) - increased by 20.0% by Agent John Doe.
```

## 📈 Analytics & Reporting

### Price Change Analytics
- **Percentage Changes**: Automatic calculation of price movements
- **Trend Analysis**: Track how market trends change over time
- **Agent Activity**: See which agents are most active in price updates
- **Time-based Analysis**: View changes by day, week, or month

### Recent Changes Summary
- Last 7 days price movements
- Quick overview of market activity
- Visual indicators for price directions

## 🛠️ Setup & Installation

### 1. Database Setup
```bash
cd "C:\Users\navya\Downloads\Inf\Inf"
python recreate_database.py
```

### 2. Test the System
```bash
python demo_market_price_update.py
```

### 3. Run the Application
```bash
streamlit run app.py
```

## 🔐 User Accounts

### Default Accounts Created
- **Admin**: `admin@smartfarm.com` / `admin123`
- **Agent**: `agent@smartfarm.com` / `agent123`

### Sample Farmers Created
- **Ravi Kumar**: `ravi@farmer.com` / `farmer123`
- **Sita Devi**: `sita@farmer.com` / `farmer123`

## 📱 SMS Configuration

The system uses Twilio for SMS notifications. Make sure to:
1. Verify phone numbers in Twilio console
2. Add credits to your Twilio account
3. Use proper phone number format: `+919876543210`

## 🔄 Data Flow

1. **Agent Updates Price** → 2. **System Logs Change** → 3. **Calculate Percentage** → 4. **Check Notification Settings** → 5. **Send SMS to Farmers** → 6. **Update CSV File** → 7. **Refresh Dashboard**

## 🎯 Benefits

### For Agents
- **Comprehensive Control**: Full control over market price management
- **Detailed Tracking**: Every change is logged and trackable
- **Efficient Communication**: Instant notifications to relevant farmers
- **Analytics Insights**: Understanding of market trends and changes

### For Farmers
- **Real-time Updates**: Instant notifications when prices change
- **Market Transparency**: Access to current and historical price data
- **Informed Decisions**: Better timing for crop sales
- **Direct Communication**: Receive important market alerts

### For System Administrators
- **Full Audit Trail**: Complete history of all price changes
- **User Activity Tracking**: Monitor agent activities
- **System Analytics**: Comprehensive reporting and insights
- **Data Integrity**: Proper database relationships and logging

## 🚀 Future Enhancements

- **Price Prediction**: AI-powered price forecasting
- **Market Trends**: Advanced analytics and trend predictions
- **Mobile App**: Dedicated mobile application for farmers
- **API Integration**: Connect with external market data sources
- **Automated Pricing**: Rule-based automatic price updates

---

*This enhanced market price management system provides a complete solution for agricultural market price tracking, agent management, and farmer communication in the Smart Farming Assistant platform.*
