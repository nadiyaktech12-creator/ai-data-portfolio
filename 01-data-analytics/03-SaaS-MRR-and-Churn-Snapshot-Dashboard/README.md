# SaaS MRR and Churn Snapshot Dashboard

## 🔗 Live Demo
[Open the dashboard](httpslink.streamlit.app)

This dashboard gives a clear snapshot of Monthly Recurring Revenue (MRR), growth, and customer churn for a SaaS business.

### Business Goal
Track how subscription revenue is growing or shrinking month over month, and understand which customers are churning.

### Features
- Key metrics: Total MRR, New MRR, Churned MRR, Net New MRR, Logo Churn Rate
- Monthly Recurring Revenue trend (last 12 months)
- Revenue breakdown by plan (Basic, Pro, Enterprise)
- Clean and simple Streamlit interface

### Tech Stack
- Python
- Pandas
- Streamlit
- Plotly

### Dataset
Synthetic subscription data (`subscriptions.csv`) generated with `generate_data.py`, simulating 300 customers across 18 months with realistic churn patterns.

### How to Run Locally

1. Clone the repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. (Optional) Regenerate the dataset:
```bash
python generate_data.py
```
4. Run the app:
```bash
streamlit run app.py
```

### Project Structure
```
03-SaaS-MRR-and-Churn-Snapshot-Dashboard/
├── app.py
├── generate_data.py
├── subscriptions.csv
├── requirements.txt
└── README.md
```

### Insights
- Logo churn rate highlights what percentage of customers are leaving each month
- Net New MRR shows whether new revenue is outpacing churned revenue
- Plan mix reveals which pricing tier drives the most revenue
