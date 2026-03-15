# 🌸 Vancouver Cherry Blossom Tracker

An interactive Streamlit application to explore and visualize over 40,000 cherry blossom trees across Vancouver.

## Features
- **Interactive Map**: View tree density and specific varieties using PyDeck (Heatmap, Scatter, and 3D Hexagon layers).
- **Bloom Tracking**: Estimated bloom status based on tree diameter and maturity.
- **Advanced Filtering**: Search by address, variety, height, trunk diameter, and planting year.
- **Analytics Dashboard**: Visualize variety distribution, planting timelines, and street-level data with Plotly.
- **Data Export**: Filter the dataset and download it as a CSV.

## Data Source
- [City of Vancouver Open Data Portal](https://opendata.vancouver.ca)

## Hosting
This app is designed to be hosted on [Streamlit Cloud](https://streamlit.io/cloud).

## Installation
To run locally:
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```
