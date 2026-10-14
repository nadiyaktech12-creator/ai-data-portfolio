
# Employee Attrition Risk Intelligence System

Predict the likelihood of an employee leaving the company, understand the key drivers, and estimate the business impact of attrition.

## Problem
Employee attrition is costly. Replacing an employee can cost 50–200% of their annual salary. HR teams need early warning signals so they can intervene before resignation.

## Solution
An interactive Streamlit application that predicts attrition probability using a Random Forest model trained on the IBM HR Analytics dataset. The app provides:

- Attrition probability score
- Risk level (Low / Medium / High)
- Estimated replacement cost
- What-If analysis (impact of changing OverTime)
- Top feature drivers
- Suggested retention actions

## Key Features
- Real-time prediction based on employee attributes
- Visual risk assessment with progress bar and metrics
- Feature importance chart
- Business impact estimation
- Clean, decision-oriented interface

## Tech Stack
- Python
- Pandas
- Scikit-learn (Random Forest)
- Streamlit
- Plotly
- joblib

## Dataset
IBM HR Analytics Employee Attrition & Performance  
(Public dataset available on Kaggle)

## How to Run Locally
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
	4	Place the dataset CSV in the project folder
	5	Train the model: python train_model.py
	7	Launch the app: streamlit run app.py
   
Project Structure
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
└── .gitignore


Live Demo
[https://attrition-risk-intelligence-system.streamlit.app/]


Key Insights
	•	OverTime is one of the strongest predictors of attrition
	•	Monthly Income, Age, and Years at Company are also important drivers
	•	Lower Job Satisfaction and Environment Satisfaction increase risk

Built as part of a data science portfolio focused on practical, decision-support applications.
