# 🏙 Nagpur Property Intelligence Dashboard

A high-end **Real Estate Analytics & Investment Intelligence Platform** built using Streamlit.

This project analyzes land/plot price trends in Nagpur and transforms raw growth data into:

- Investment signals
- Risk scoring
- Predictive growth modeling
- Segment-based insights
- Interactive visual intelligence dashboards

---

# 🚀 Project Overview

Nagpur Property Intelligence is a fully interactive analytics dashboard that:

- Compares 1-Year and 3-Year growth trends
- Identifies top-performing and underperforming localities
- Segments properties into Affordable / Mid-Range / Premium
- Predicts next-year price growth using Linear Regression
- Generates investment recommendations using a multi-tier logic engine
- Evaluates volatility-based risk
- Provides a professional futuristic UI experience

---

# 📊 Core Analytics Features

### 1️⃣ Locality-Wise Growth Comparison
- Horizontal gradient growth visualization
- Sorted by selected growth window (1Y or 3Y)

### 2️⃣ Top 5 Fastest Growing vs Lowest Performing
- Dual-panel comparative analysis
- Integrated recommendation signals

### 3️⃣ 1Y vs 3Y Growth Comparison
- Grouped bar visualization
- Heatmap for quick comparative analysis

### 4️⃣ Price Segment Analysis
- Auto-segmentation:
  - Affordable
  - Mid-Range
  - Premium
- Average growth per segment
- Donut distribution chart
- Predicted returns per segment

---

# 🔮 Prediction Model

### Model Type:
Linear Regression

### Features Used:
- 1-Year Growth
- 3-Year Growth

### Output:
- Predicted Next-Year Growth %
- R² model performance score
- Model coefficients displayed in dashboard

---

# 💡 Investment Recommendation Logic

Multi-tier classification system based on:

- Predicted growth
- Volatility (risk)

| Signal | Criteria |
|--------|----------|
| 🚀 Strong Buy | Predicted > 15% AND Low volatility |
| 📈 High Growth / High Risk | Predicted > 15% AND High volatility |
| 📊 Moderate Buy | Predicted 5–15% |
| ⏸ Hold | Predicted 0–5% |
| ⚠ Avoid | Negative predicted growth |

---

# ⚠ Risk Evaluation

Volatility is computed as:

Standard Deviation of (growth_1y, growth_3y)

High volatility areas are:

- Highlighted in dashboard
- Visualized using radar charts
- Included in risk leaderboard

---

# 🧠 Advanced Features

### 🔄 Scheduled Auto-Refresh
- Automatically refreshes every 60 minutes
- Clears cache before rerun

### ⚡ Caching Strategy
- Uses `@st.cache_data(ttl=3600)`
- Optimized performance with controlled TTL

### 📊 Risk vs Reward Scatter
- Bubble size based on investment score
- Quadrant lines divide risk-reward zones

### 🏅 Investment Leaderboard
- Ranked by weighted investment score
- Progress bar visualization
- Includes volatility and predicted returns

### 🎨 Custom Futuristic UI
- Dark cyber-style theme
- Custom CSS styling
- Custom KPI cards
- Advanced layout styling
- Sidebar intelligence panel

---

# 📁 Project Structure

Nagpur_Dashboard/
│
├── app.py                      # Complete analytics dashboard
├── nagpur_cleaned_dataset.csv  # Input dataset
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation

---

# 🛠 Technology Stack

- Python
- Streamlit
- Pandas
- Plotly (Graph Objects + Express)
- NumPy
- Scikit-learn

---

# 📦 Requirements

requirements.txt:

streamlit  
pandas  
plotly  
numpy  
scikit-learn  

---

# 🚀 Run Locally

## 1. Clone Repository

git clone https://github.com/A08rpita0/Nagpur_Dashboard.git  
cd Nagpur_Dashboard  

## 2. Install Dependencies

pip install -r requirements.txt  

## 3. Run Dashboard

streamlit run app.py  

Open in browser:

http://localhost:8501  

---

# 🌐 Deployment

Deploy easily on Streamlit Cloud:

1. Push repository to GitHub
2. Go to https://share.streamlit.io
3. Select repository
4. Set main file as app.py
5. Click Deploy

---

# 📈 Model Transparency

The dashboard displays:

- R² score
- Regression coefficients
- Intercept value
- Real vs predicted scatter

This ensures transparency and interpretability of the prediction model.

---

# 🎯 Key Highlights

✔ End-to-end analytics pipeline  
✔ Financial growth computation  
✔ Predictive modeling  
✔ Investment signal engine  
✔ Volatility-based risk scoring  
✔ Interactive multi-layer visualizations  
✔ Automated refresh & caching  
✔ Cloud deployment ready  

---



# ⭐ Conclusion

This project demonstrates:

- Advanced data analysis
- Predictive modeling
- Risk-based financial evaluation
- Full-stack dashboard engineering
- Production-ready deployment

It transforms raw property growth data into actionable real estate intelligence.

---


## 🌐 Live Demo

You can access the deployed dashboard here:

🔗 https://nagpurdashboard.streamlit.app/
