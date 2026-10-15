# A/B Test Results Analyzer

Evaluate A/B test results and determine whether the difference between Control and Treatment is statistically significant.

## Problem
Marketers and product teams run A/B tests but often struggle to correctly interpret whether the observed difference is real or simply due to chance.

## Solution
A clean Streamlit application that takes conversion numbers from Control and Treatment groups and returns:

- Conversion rates for both groups
- Lift percentage
- Statistical significance (Chi-square test)
- Clear recommendation
- Visual comparison chart

## Features
- Chi-square test for statistical significance
- Lift calculation
- Visual bar chart comparison
- Business-friendly recommendation
- Clean and minimal interface

## Tech Stack
- Python
- Streamlit
- SciPy
- Plotly
- NumPy

Live Demo
[https://ab-test-results-analyzer.streamlit.app/]

Notes
	•	Uses a significance threshold of p-value < 0.05
	•	Designed for conversion-based A/B tests
	•	No dataset or model training required
