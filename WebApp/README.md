# Garbage Classification for Smart Cities — SmartWaste

Streamlit app: **login page first** → **dashboard** with full navigation, waste image classification (Biodegradable vs Non-Biodegradable), live camera, and city weather.

## Run the website

```powershell
cd "C:\Users\chanchal\Videos\Automatic Waste Detection Using Deep Learning\Source Code\WebApp"
pip install -r requirements.txt
streamlit run app.py
```

## Login

- Opens on **Welcome to SmartWaste** (no Home/About/Contact nav).
- After login you go to the dashboard with **WELCOME BACK, [YOUR NAME]**.
- **Demo:** `admin` / `admin123`
- **Your accounts** in `smartwaste_users.json` (e.g. `arshi@gov.city.in`) — password `12345678` if you used that when registering.

## Dataset & model

**Dataset** (Organic **O** / Recyclable **R**):

```
Automatic Waste Detection Using Deep Learning/
  Dataset/DATASET/TRAIN/O/
  Dataset/DATASET/TRAIN/R/
  Dataset/DATASET/TEST/O/
  Dataset/DATASET/TEST/R/
```

**Trained model** should be in `saved_models/waste_classification_model.h5` (already copied if you trained earlier).

Retrain on your local dataset:

```powershell
python train_model.py --quick
```

Then restart Streamlit.

## Features

| Tab | Works |
|-----|--------|
| Dashboard | Stats, upload classify, map, quick actions |
| Live Detection | Webcam capture |
| Image Classification | Upload images |
| Waste Locations | Map, filter, add locations |
| Collection Routes | Route table |
| Analytics & Reports | Charts + CSV export |
| History | All detections |
| Alerts | City alerts |
| Bin Status | Bin fill levels |
| User Management | Registered users |
| Settings | Model path + reload |

**Location** (top right) changes city and shows **live temperature** (Open-Meteo API).

Plastic / recyclable images → **Non-Biodegradable**. Organic (O) → **Biodegradable**.
