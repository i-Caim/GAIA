# GAIA
GAIA is a data-driven urban greening intelligence platform that uses satellite imagery to identify and prioritize areas in Riyadh most in need of vegetation.

**start date :** may 7  
**postpone reason :** got demotivated by not getting accepted into the hackathon

---

## OG Idea

A data-driven smart platform to support urban greening in Riyadh. The system analyzes satellite imagery to identify areas most in need of planting, and recommends the most suitable vegetation type based on the area's conditions. The goal is to shift greening decisions from manual guesswork to intelligent, data-driven prioritization — in support of Saudi Arabia's Green Initiative.

---

## Thoughts

this idea was inspired from the effort of trying to enhance the city's livability and environmental quality, by addressing one of Riyadh's most visible challenges, the lack of green cover in urban areas

as my views as a citizen i see the efforts being made although slow but effective, i thought; "as they try to carry through with the project maybe i can find a way to help, even with a prototype" so i tried to develop **GAIA**.

---

## The Tools Used

### Google Earth Engine
to extract NDVI satellite data for Riyadh

**Google Earth Engine** is free to use as long as the Token does not exceed limits

#### code for Riyadh region
```javascript
// تحديد منطقة الرياض
var riyadh = ee.Geometry.Rectangle([46.5, 24.5, 47.0, 25.0]);

// جلب صور Sentinel-2
var image = ee.ImageCollection('COPERNICUS/S2_SR')
  .filterBounds(riyadh)
  .filterDate('2024-01-01', '2024-12-31')
  .median();

// حساب NDVI
var ndvi = image.normalizedDifference(['B8', 'B4']);

// عرض الخريطة
Map.centerObject(riyadh, 11);
Map.addLayer(ndvi, {min: -0.2, max: 0.8,
  palette: ['red', 'yellow', 'green']}, 'NDVI Riyadh');
```

#### Extracting the info into Excel sheet
```javascript
// تحديد منطقة الرياض
var riyadh = ee.Geometry.Rectangle([46.5, 24.5, 47.0, 25.0]);

// جلب صور Sentinel-2
var image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(riyadh)
  .filterDate('2024-01-01', '2024-12-31')
  .median();

// حساب NDVI
var ndvi = image.normalizedDifference(['B8', 'B4']);

// تقسيم الرياض لنقاط
var points = ee.FeatureCollection.randomPoints(riyadh, 50);

// استخراج NDVI مع الإحداثيات
var ndviPoints = ndvi.sampleRegions({
  collection: points,
  scale: 100,
  geometries: true
});

// إضافة أعمدة lat/lng
var withCoords = ndviPoints.map(function(f) {
  return f.set({
    longitude: f.geometry().coordinates().get(0),
    latitude: f.geometry().coordinates().get(1)
  });
});

// تصدير
Export.table.toDrive({
  collection: withCoords,
  description: 'Riyadh_NDVI_Coords',
  fileFormat: 'CSV'
});
```

---

### VS Code
main development environment

---

### Python coding language
**IDE:** VS Code

#### ndvi_priority.py
This script reads the raw CSV exported from Google Earth Engine, classifies each point into a priority level (High / Medium / Low) based on its NDVI value, and saves the result as a new CSV file — `Riyadh_NDVI_Priority.csv` — with the priority column added.

#### convert_data.py
This script takes the processed CSV and converts it into a JavaScript file (`data.js`). This conversion is what makes the data readable by the browser and Mapbox.

#### data.js — the bridge
After Python finishes processing, the data lives in a CSV file. But Mapbox runs in the browser and can't read CSV directly. `data.js` is the solution — it's the same data reformatted as a JavaScript array, loaded directly into `the_map.html`. This is what connects the Python processing pipeline to the Mapbox interactive map.

---

### JavaScript coding language
**IDE:** within Google Earth Engine

---

### HTML / CSS / JavaScript coding languages
**IDE:** VS Code

---

### Libraries

- **pandas**: opened the CSV file from Earth Engine, added the priority column (High/Medium/Low) based on NDVI values, and saved the final processed file
- **openpyxl**: exported the data as a colored Excel file (.xlsx) where each row was colored red/yellow/green based on priority
- **jinja2**: required by pandas to apply the color styling to the Excel file — it works in the background, we didn't write any jinja2 code directly

---

### MapBox
for the interactive map frontend JS

- **Displaying the map**: rendered the dark map of Riyadh as the base
- **Plotting the points**: placed each NDVI data point on the map as a glowing dot with its priority color
- **Pulsing ring animations**: the expanding rings around each dot
- **Popups**: the small tooltip that appears when you hover over a dot on the map
- **Fly to location**: when you click a point in the left panel, the map smoothly flies to it
- **Reverse Geocoding API**: converted the raw coordinates into readable region names (like "Ad Diriyah", "As Sulaymaniyah") that appear in the panel and detail section

> **Note:** To run this project you need your own Mapbox token. Replace `YOUR_MAPBOX_TOKEN_HERE` in `the_map.html` with your token.

---

## The Errors I Faced

**⚡ ModuleNotFoundError: No module named 'pandas'**  
fixed with `pip install pandas`

**⚡ AttributeError: The '.style' accessor requires jinja2**  
fixed with `pip install jinja2`

**⚡ AttributeError: 'Styler' object has no attribute 'applymap'**  
fixed by replacing `applymap` with `map` (pandas version change)

**⚡ ndvi is not defined in Earth Engine**  
fixed by combining all code into one script instead of separate ones

**⚡ Map markers growing detached from coordinates**  
fixed by setting wrapper div to `0x0` and using negative offsets from center

---

## Data Sources

All data was sourced from **free, publicly available platforms:**

- **Google Earth Engine + Sentinel-2 (Copernicus)** — satellite imagery used to calculate NDVI (vegetation index) for Riyadh
- **Mapbox Geocoding API** — open API used to retrieve region and neighborhood names from coordinates

### Pending response since May 2026
Outreach was made to المركز الوطني للغطاء النباتي and مبادرة السعودية الخضراء for official soil and vegetation data
