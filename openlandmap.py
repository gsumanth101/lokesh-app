import requests
import json
import sys
import io

# Make stdout UTF-8 capable (optional, for emojis)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

lat = 17.385044
lon = 78.486671

url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}"

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Uncomment to inspect full response:
        # print(json.dumps(data, indent=2))

        properties = data.get("properties", {}).get("layers", {})

        def get_mean_value(layer_name, depth="0-5cm"):
            layer = properties.get(layer_name, {})
            vals = layer.get("depths", [])
            for d in vals:
                if d.get("depth") == depth:
                    return d.get("values", {}).get("mean")
            return None

        ph = get_mean_value("phh2o")
        nitrogen = get_mean_value("nitrogen")
        carbon = get_mean_value("ocd")

        print(f"📊 Soil pH (H₂O): {ph if ph is not None else 'Not Available'}")
        print(f"🌿 Nitrogen: {nitrogen if nitrogen is not None else 'Not Available'} g/kg")
        print(f"🪵 Organic Carbon: {carbon if carbon is not None else 'Not Available'} g/kg")

    else:
        print(f"❌ HTTP Error: Status code {response.status_code}")

except Exception as e:
    print(f"❌ Exception occurred: {e}")
