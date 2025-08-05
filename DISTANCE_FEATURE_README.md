# Distance Calculation Feature Documentation

## Overview
The SmartFarm application now includes a comprehensive distance calculation feature that shows the distance between buyers and products in the marketplace. This feature uses the Google Maps Distance Matrix API to provide accurate distance and travel time information.

## Features Implemented

### 1. Distance Calculation Function
- **Function**: `calculate_distance(origin, destination, api_key)`
- **API**: Google Maps Distance Matrix API
- **API Key**: `AIzaSyDKlljm7I5R6_knlq8nFUKEFl_e_tRNq2U`
- **Returns**: Distance text, distance value (meters), duration text, duration value (seconds)

### 2. Enhanced Buyer Dashboard
- **New Tab**: "📍 Profile" tab added to buyer dashboard
- **Location Management**: Buyers can update their complete address
- **Profile Update**: New `show_buyer_profile_update()` function
- **Database Integration**: `update_user_profile()` method in DatabaseManager

### 3. Marketplace Enhancements
- **Distance Display**: Shows distance and travel time for each product listing
- **Color Coding**: 
  - 🟢 Green: Less than 50 km
  - 🟡 Orange: 50-100 km
  - 🔴 Red: More than 100 km
- **Expander Titles**: Product listings show distance in the title

### 4. Filtering and Sorting
- **Distance Filter**: Maximum distance slider (10-500 km)
- **Distance Sorting**: "Distance (Nearest)" and "Distance (Farthest)" options
- **Location-based Filtering**: Automatically filters products within the specified distance range

### 5. User Experience Features
- **Loading Indicators**: Shows progress when calculating distances for multiple listings
- **Error Handling**: Graceful handling of API errors and network issues
- **User Location Display**: Shows buyer's current location in the marketplace
- **Setup Prompts**: Guides users to set up their location if not configured

## Database Schema Updates

### User Profile Enhancement
The `users` table already contains the necessary fields:
- `address`: Stores the complete address for distance calculations
- `phone`: Contact information for notifications

### New Database Method
```python
def update_user_profile(self, user_id: int, phone: str, address: str) -> bool:
    """Update user profile information"""
```

## API Configuration

### Google Maps Distance Matrix API
- **Endpoint**: `https://maps.googleapis.com/maps/api/distancematrix/json`
- **Parameters**:
  - `origins`: Buyer's address
  - `destinations`: Product location
  - `units`: metric (for kilometers)
  - `key`: API key
- **Response**: JSON with distance and duration information

## Usage Instructions

### For Buyers:
1. **Set Your Location**:
   - Go to the "📍 Profile" tab in your buyer dashboard
   - Enter your complete address (city, state, country)
   - Click "💾 Update Profile"

2. **Browse Products with Distance**:
   - Go to "🌾 Browse Crops" tab
   - Distance and travel time will be displayed for each product
   - Use the "🚗 Max Distance" filter to find nearby products
   - Sort by "Distance (Nearest)" to see closest products first

3. **Filter by Distance**:
   - Use the distance slider to set maximum distance (10-500 km)
   - Products beyond this distance will be automatically filtered out

### For Farmers:
- Enter detailed location information when listing products
- More specific addresses lead to better distance calculations

## Technical Implementation

### Key Functions:
1. `calculate_distance()`: Core distance calculation using Google Maps API
2. `get_user_location()`: Retrieves buyer's address from database
3. `show_buyer_profile_update()`: Profile management interface
4. `show_crop_listings_for_buyers()`: Enhanced marketplace with distance features

### Error Handling:
- Network timeouts
- Invalid API responses
- Missing location data
- API quota limitations

### Performance Optimization:
- Loading indicators for multiple calculations
- Progress updates for large lists
- Efficient distance filtering
- Cached user location retrieval

## Testing

The feature has been tested with:
- **Test Script**: `test_distance_calculation.py`
- **Sample Route**: Mumbai to Pune (155 km, 3 hours)
- **API Response**: Confirmed working with provided API key

## Future Enhancements

### Potential Improvements:
1. **Map Integration**: Visual map display of product locations
2. **Batch Processing**: Optimize API calls for multiple locations
3. **Route Planning**: Multi-stop route optimization
4. **Location Autocomplete**: Google Places API integration
5. **Offline Fallback**: Cached distance data for common routes

## Security Considerations

- API key should be moved to environment variables in production
- Rate limiting for API calls
- Input validation for location data
- Error message sanitization

## Benefits

### For Buyers:
- **Better Decision Making**: Know exact distances before making offers
- **Time Savings**: Find nearby products quickly
- **Cost Estimation**: Understand transportation costs
- **Convenience**: Sort and filter by proximity

### For Farmers:
- **Targeted Selling**: Attract nearby buyers
- **Competitive Advantage**: Proximity-based marketing
- **Reduced Transportation**: Connect with local buyers

### For the Platform:
- **Enhanced User Experience**: More informed marketplace interactions
- **Increased Engagement**: Better search and filtering capabilities
- **Competitive Advantage**: Unique location-based features

## Conclusion

The distance calculation feature significantly enhances the SmartFarm marketplace by providing location-based intelligence. Buyers can now make more informed decisions based on product proximity, while farmers can better target their local markets. The feature is fully integrated with the existing user interface and provides a seamless experience for all users.
