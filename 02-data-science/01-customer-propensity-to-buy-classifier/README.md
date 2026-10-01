# Customer Propensity-to-Buy Classifier

A machine learning app that estimates the probability a bank customer will subscribe to a term deposit, based on customer profile, campaign history and economic indicators. Built with scikit-learn and deployed as an interactive Streamlit app.

**Live demo:** _add Streamlit Cloud link here_

---

## Business Problem

Marketing teams cannot call every customer. A propensity model scores each customer by how likely they are to buy, so the team can focus calls on the highest-probability leads, cut wasted outreach and improve conversion.

## Dataset

- **Source:** [Bank Marketing Dataset (UCI)](https://archive.ics.uci.edu/dataset/222/bank+marketing), `bank-additional-full.csv`
- **Size:** 41,188 rows, 21 columns
- **Target:** `y` (did the customer subscribe? yes = 1, no = 0)
- **Class balance:** about 11% "yes" (4,640) vs 89% "no" (36,548)
- **Features:** age, job, marital status, education, loan flags, contact type, month, day of week, campaign history, and macroeconomic indicators (employment variation rate, consumer price and confidence index, Euribor 3-month rate, number employed)

> The file is semicolon-separated, so it is loaded with `sep=";"`.

## Approach

1. **Load** the data and check the class balance.
2. **Drop `duration`.** Call duration is only known after the call ends, so keeping it would leak the answer and make the model unusable for real prediction.
3. **Preprocess:** fill missing values (median for numeric columns, mode for categorical), then one-hot encode categoricals with `pd.get_dummies`.
4. **Split** 80/20 with stratification to preserve the class ratio.
5. **Train** a `RandomForestClassifier` (200 trees, `max_depth=12`, `class_weight="balanced"`).
6. **Save** the model and the exact training feature list with `joblib`.
7. **Serve** predictions through a Streamlit form that rebuilds a one-row DataFrame, reindexes it to the saved feature list, and calls `predict_proba`.

## Results

Evaluated on the 20% hold-out set (8,238 rows):

| Metric | Value |
|---|---|
| Accuracy | 0.86 |
| Precision (buyers) | 0.43 |
| Recall (buyers) | 0.63 |
| F1 (buyers) | 0.51 |

Accuracy alone is misleading here because most customers say "no". Recall on the buyer class is the metric that matters: the model finds about 63% of customers who actually subscribe.

## Key Design Decisions

- **Column alignment:** the most common deployment bug is a mismatch between training and prediction columns. The app loads `feature_columns.joblib` and reindexes every input row to that exact list and order.
- **`class_weight="balanced"`:** improves recall on the minority class, but it inflates probabilities. Treat the output as a ranking score for prioritizing leads, not a calibrated real-world probability.
- **Single-row encoding:** the app calls `get_dummies` without `drop_first`, because dropping the first category on a one-row frame would remove every categorical column. Reindexing then discards the extras so the result matches training.

## Project Structure

```
05_customer-propensity-to-buy-classifier/
├── app.py                    # Streamlit app
├── train_model.py            # Training script
├── bank.csv                  # Dataset (bank-additional-full.csv, renamed)
├── bank-additional-names.txt  # Column descriptions
├── model.joblib              # Trained model
├── feature_columns.joblib    # Exact feature list and order
├── requirements.txt
└── README.md
```

## Run Locally

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model (prints accuracy and classification report)
python train_model.py

# 4. Launch the app
python -m streamlit run app.py
```

## Tech Stack

Python, pandas, scikit-learn, joblib, Streamlit

## Deployment

Deployed on Streamlit Community Cloud. Point it at `05_customer-propensity-to-buy-classifier/app.py`. Package versions are pinned in `requirements.txt` so the deployed environment matches the one used to train the model.


## Data Citation

Moro, S., Rita, P., and Cortez, P. (2014). Bank Marketing. UCI Machine Learning Repository.
