import streamlit as st
import numpy as np
from scipy.stats import chi2_contingency
import plotly.graph_objects as go

st.set_page_config(page_title="A/B Test Statistical Evaluator", layout="wide")

st.title("A/B Test Statistical Evaluator")
st.markdown("""
Evaluate whether the difference between Control and Treatment is statistically significant.  
Enter the conversion numbers below.
""")

# Input form
with st.form("ab_test_form"):
    st.subheader("Test Results")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Control Group**")
        control_conversions = st.number_input("Control Conversions", min_value=0, value=120)
        control_total = st.number_input("Control Total Visitors", min_value=1, value=1000)

    with col2:
        st.markdown("**Treatment Group**")
        treatment_conversions = st.number_input("Treatment Conversions", min_value=0, value=150)
        treatment_total = st.number_input("Treatment Total Visitors", min_value=1, value=1000)

    submitted = st.form_submit_button("Evaluate Results", type="primary")

if submitted:
    # Conversion rates
    control_rate = control_conversions / control_total
    treatment_rate = treatment_conversions / treatment_total
    lift = ((treatment_rate - control_rate) / control_rate) * 100 if control_rate > 0 else 0

    # Chi-square test
    contingency_table = [
        [control_conversions, control_total - control_conversions],
        [treatment_conversions, treatment_total - treatment_conversions]
    ]
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    # Significance
    is_significant = p_value < 0.05
    significance_text = "Statistically Significant" if is_significant else "Not Statistically Significant"
    significance_color = "green" if is_significant else "red"

    # Results
    st.divider()
    st.subheader("Results")

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Control Conversion Rate", f"{control_rate:.2%}")
    with metric_col2:
        st.metric("Treatment Conversion Rate", f"{treatment_rate:.2%}")
    with metric_col3:
        st.metric("Lift", f"{lift:+.1f}%")

    # Significance
    if is_significant:
        st.success(f"**{significance_text}** (p-value = {p_value:.4f})")
    else:
        st.error(f"**{significance_text}** (p-value = {p_value:.4f})")

    st.caption("Significance threshold: p-value < 0.05")

    # Visual comparison
    fig = go.Figure(data=[
        go.Bar(name="Control", x=["Conversion Rate"], y=[control_rate * 100], marker_color="#4C78A8"),
        go.Bar(name="Treatment", x=["Conversion Rate"], y=[treatment_rate * 100], marker_color="#F58518")
    ])
    fig.update_layout(
        title="Conversion Rate Comparison",
        yaxis_title="Conversion Rate (%)",
        barmode="group",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Recommendation
    st.subheader("Recommendation")
    if is_significant and lift > 0:
        st.write("The Treatment performed better and the difference is statistically significant. Consider implementing the Treatment.")
    elif is_significant and lift < 0:
        st.write("The Treatment performed worse and the difference is statistically significant. Do not implement the Treatment.")
    else:
        st.write("The difference is not statistically significant. Continue testing or gather more data before making a decision.")