Here's the full README with the live demo link added at the top — copy this entire thing to replace what's in the editor:

```markdown
# E-commerce Sales Cohort Retention Heatmap

## 🔗 Live Demo
[Open the dashboard](https://e-commerce-cohort-retention-heatmap-1.streamlit.app)

This project analyzes customer retention using cohort analysis on an e-commerce transactional dataset.

### Business Goal
Understand what percentage of customers who made their first purchase in a particular month continued to buy in the following months.

### Features
- Cohort-based customer retention analysis
- Interactive heatmap visualization
- Retention percentage over time
- Clean and simple Streamlit interface

### Tech Stack
- Python
- Pandas
- Streamlit
- Plotly

### Dataset
Online Retail dataset from UCI Machine Learning Repository
(Contains transactional data with Customer ID and Invoice Date)

### How to Run Locally

1. Clone the repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Run the app:
```bash
streamlit run app.py
```

### Project Structure
```
02-e-commerce-cohort-retention-heatmap/
├── app.py
├── online_retail.xlsx
├── requirements.txt
└── README.md
```

### Insights
- Month 0 always shows 100% (first purchase month)
- Retention typically drops in the following months
- Helps identify how well the business retains new customers over time
