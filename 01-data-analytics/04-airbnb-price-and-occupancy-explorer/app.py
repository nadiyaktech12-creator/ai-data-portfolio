import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Airbnb Price & Occupancy Explorer",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Airbnb Price & Occupancy Explorer")
st.markdown("Explore Airbnb listings by neighborhood, room type, and price range.")

# Load data
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "listings.csv"
    df = pd.read_csv(data_path)
    
    # Clean price
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.strip()
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Neighborhood (using cleansed version)
neighborhoods = sorted(df["neighbourhood_cleansed"].dropna().unique())
selected_neighborhoods = st.sidebar.multiselect(
    "Neighborhood",
    options=neighborhoods,
    default=neighborhoods[:10] if len(neighborhoods) > 10 else neighborhoods
)

# Room type
room_types = sorted(df["room_type"].dropna().unique())
selected_room_types = st.sidebar.multiselect(
    "Room Type",
    options=room_types,
    default=room_types
)

# Price range
min_price = int(df["price"].min())
max_price = int(df["price"].quantile(0.95))
price_range = st.sidebar.slider(
    "Price Range ($)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, min(max_price, 400))
)

# Apply filters
filtered_df = df[
    (df["neighbourhood_cleansed"].isin(selected_neighborhoods)) &
    (df["room_type"].isin(selected_room_types)) &
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]

# KPI row
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Price", f"${filtered_df['price'].mean():.0f}")

with col2:
    st.metric("Median Price", f"${filtered_df['price'].median():.0f}")

with col3:
    st.metric("Number of Listings", f"{len(filtered_df):,}")

# Charts
st.subheader("Visualizations")

# 1. Price Distribution
fig_hist = px.histogram(
    filtered_df,
    x="price",
    nbins=40,
    title="Price Distribution",
    labels={"price": "Price ($)"}
)
st.plotly_chart(fig_hist, use_container_width=True)

# 2. Average Price by Neighborhood (Top 10)
avg_price = (
    filtered_df.groupby("neighbourhood_cleansed")["price"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_bar = px.bar(
    avg_price,
    x="neighbourhood_cleansed",
    y="price",
    title="Top 10 Neighborhoods by Average Price",
    labels={"price": "Average Price ($)", "neighbourhood_cleansed": "Neighborhood"}
)
st.plotly_chart(fig_bar, use_container_width=True)

# 3. Price vs Number of Reviews
if "number_of_reviews" in filtered_df.columns:
    fig_scatter = px.scatter(
        filtered_df,
        x="number_of_reviews",
        y="price",
        color="room_type",
        hover_name="name",
        title="Price vs Number of Reviews",
        labels={"number_of_reviews": "Number of Reviews", "price": "Price ($)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# 4. Map
if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:
    st.subheader("Map of Listings")
    map_df = filtered_df[["latitude", "longitude"]].dropna()
    st.map(map_df)