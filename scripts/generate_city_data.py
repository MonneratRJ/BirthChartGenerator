import json
from geonamescache import GeonamesCache
from timezonefinder import TimezoneFinder

# Load countries.json
with open('../static/countries.json', encoding='utf-8') as f:
    countries = json.load(f)
country_codes = set(c['code'] for c in countries)

# Get cities from geonamescache
gc = GeonamesCache()
cities = gc.get_cities()

# Prepare country_code -> [city, lat, lon] mapping
country_cities = {}
for city_id, city_data in cities.items():
    cc = city_data['countrycode']
    if cc not in country_codes:
        continue
    entry = {
        'name': city_data['name'],
        'lat': float(city_data['latitude']),
        'lon': float(city_data['longitude'])
    }
    country_cities.setdefault(cc, []).append(entry)

# Save cities.json
with open('../static/cities.json', 'w', encoding='utf-8') as f:
    json.dump(country_cities, f, ensure_ascii=False, indent=2)

# Prepare city+country -> timezone mapping
finder = TimezoneFinder()
city_timezones = {}
for cc, city_list in country_cities.items():
    for city in city_list:
        tz = finder.timezone_at(lng=city['lon'], lat=city['lat'])
        key = f"{cc}:{city['name']}"
        city_timezones[key] = tz

# Save city_timezones.json
with open('../static/city_timezones.json', 'w', encoding='utf-8') as f:
    json.dump(city_timezones, f, ensure_ascii=False, indent=2)

print('Done! cities.json and city_timezones.json generated.')
