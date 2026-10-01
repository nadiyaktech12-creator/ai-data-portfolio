from pathlib import Path
import joblib
import pandas as pd
import streamlit as st
from pandas.api.types import is_numeric_dtype

BASE_DIR = Path(__file__).parent


@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "german_credit.csv").drop(columns=["class"])


@st.cache_resource
def load_artifacts():
    return (
        joblib.load(BASE_DIR / "model.joblib"),
        joblib.load(BASE_DIR / "feature_columns.joblib"),
    )


def grouped_importance(model, cols, raw_cols):
    imp = pd.Series(model.feature_importances_, index=cols)

    def parent(col):  # map dummy column back to its original feature
        m = [r for r in raw_cols if col == r or col.startswith(r + "_")]
        return max(m, key=len) if m else col

    return imp.groupby(parent).sum().sort_values(ascending=False)


st.title("Credit Risk Scorecard")
st.caption("Educational only. Not a real credit decision engine.")

raw = load_data()
model, cols = load_artifacts()

inputs = {}
for c in raw.columns:
    if is_numeric_dtype(raw[c]):
        inputs[c] = st.number_input(c, value=float(raw[c].median()))
    else:
        inputs[c] = st.selectbox(c, sorted(raw[c].dropna().unique()))

if st.button("Predict"):
    row = pd.get_dummies(pd.DataFrame([inputs]))
    row = row.reindex(columns=cols, fill_value=0).astype(float)
    p = model.predict_proba(row)[0][1]
    level = "Low" if p < 0.33 else "Medium" if p < 0.60 else "High"
    st.metric("Probability of default", f"{p:.0%}")
    st.progress(float(p))
    st.subheader(f"{level} risk")

st.divider()
with st.expander("What drives the model? (feature importance)"):
    top = grouped_importance(model, cols, list(raw.columns)).head(10)
    st.bar_chart(top, horizontal=True)
    st.caption("Shows what the model relies on most, not what causes default.")