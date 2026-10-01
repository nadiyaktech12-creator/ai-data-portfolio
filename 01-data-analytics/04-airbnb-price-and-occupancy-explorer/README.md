# 🏠 Airbnb Price & Occupancy Explorer

An interactive Streamlit dashboard to explore Airbnb listings by neighborhood, room type, and price range.

**Live Demo:** [Add your Streamlit Cloud link here]

---

## 📊 Features

- **Sidebar Filters**
  - Neighborhood
  - Room Type
  - Price Range slider

- **Key Metrics (KPIs)**
  - Average Price
  - Median Price
  - Number of Listings

- **Visualizations**
  - Price Distribution (Histogram)
  - Top 10 Neighborhoods by Average Price (Bar Chart)
  - Price vs Number of Reviews (Scatter Plot)
  - Interactive Map of Listings

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – Web app framework
- **Pandas** – Data processing
- **Plotly Express** – Interactive charts

---

## 📁 Project Structure

04_airbnb-price-and-occupancy-explorer/ ├── app.py ├── listings.csv ├── requirements.txt └── README.md
---

##  How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/nadiyaktech12-creator/ai-data-portfolio.git
cd ai-data-portfolio/01-data-analytics/04-airbnb-price-and-occupancy-explorer
	2	Create a virtual environment (optional but recommended)       
	3	Install dependencies
pip install -r requirements.txt
	4	Run the app
streamlit run app.py

📦 Requirements
streamlit
pandas
plotly

📌 Dataset
	•	Source: Inside Airbnb
	•	City used: Albany, New York
	•	File: listings.csv

Created by: Nadiya Kauser 
