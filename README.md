# 🏙 Nagpur Property Intelligence Dashboard

A dark-themed, futuristic real estate analytics dashboard built with **Streamlit** — tracking land/plot price trends across Nagpur localities with ML-powered growth predictions and investment signals.

---

## 📸 Features

| Section | Description |
|---|---|
| 📊 Locality-wise Growth Comparison | Horizontal bar chart of price growth per locality |
| 🏆 Top 5 / Lowest Performing | Side-by-side winners vs laggards with data tables |
| 📈 1Y vs 3Y Comparison | Grouped bars + heatmap across growth periods |
| 🏷 Price Segment Analysis | Affordable / Mid-Range / Premium breakdown |
| 🔮 Prediction Model | Linear Regression predicting next-year growth |
| 💡 Investment Recommendation | 5-tier signal engine (Strong Buy → Avoid) |
| 🏅 Investment Leaderboard | Full ranked table with progress bar scoring |
| ⚠ Risk Zones | Radar chart of high-volatility localities |

---

## 🗂 Project Structure

```
nagpur-dashboard/
├── app.py                       # Streamlit dashboard (main app)
├── nagpur_cleaned_dataset.csv     # Final dataset used by app.py
├── nagpur_dataset.csv           # Intermediate extracted dataset
├── clean_data.py                # Data cleaning script (run locally)
├── scrap.py                     # Data extraction script (run locally)
├── nagpur_data.json             # Raw scraped JSON data
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Data Pipeline

```
nagpur_data.json
      ↓  scrap.py          → extracts JSON into CSV
nagpur_dataset.csv
      ↓  clean_data.py     → cleans, calculates growth %
nagpur_final_cleaned.csv
      ↓  app.py            → Streamlit dashboard (deployed)
```

> **Note:** Only `app.py`, `nagpur_cleaned_dataset.csv`, and `requirements.txt` are needed at runtime. The other files are for data preparation only.

---

## ⚙ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/A08rpita0/Nagpur_Dashboard
cd nagpur-dashboard
```




### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 🔄 Regenerating the Dataset (Optional)

If you want to re-run the full data pipeline from scratch:

**Step 1 — Extract raw data**

Run `scrap.py` to read `nagpur_data.json` and produce `nagpur_dataset.csv`.

```bash
python scrap.py
```

**Step 2 — Clean the data**

```bash
python clean_data.py
```

This produces `nagpur_cleaned_dataset.csv` which `app.py` reads.

---

## 📦 Requirements

```
streamlit
pandas
plotly
scikit-learn
numpy
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub (must be **public**)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** and fill in:
   - **Repository:** `YOUR_USERNAME/nagpur-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy**

Your app will be live at:
```
https://nagpurdashboard.streamlit.app/
```

---

## 🧠 How the Prediction Model Works

- **Algorithm:** Linear Regression (`scikit-learn`)
- **Features:** `growth_1y`, `growth_3y`
- **Target:** Predicted next-year growth %
- **Displayed:** R² score shown live in sidebar and KPI cards

### Investment Signal Logic

| Signal | Condition |
|---|---|
| 🚀 Strong Buy | Predicted > 15% AND volatility < 10 |
| 📈 High Growth / High Risk | Predicted > 15% AND volatility ≥ 10 |
| 📊 Moderate Buy | Predicted 5–15% |
| ⏸ Hold | Predicted 0–5% |
| ⚠ Avoid | Predicted < 0% |

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Dashboard framework |
| [Plotly](https://plotly.com) | Interactive charts |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [scikit-learn](https://scikit-learn.org) | ML prediction model |
| [NumPy](https://numpy.org) | Numerical computations |

---

## 👩‍💻 Author

**Arpita Khobragade**  
Turning raw data into real estate intelligence 🏙
