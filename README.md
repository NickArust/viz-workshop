# Beginner Data Visualization Workshop (Citi Bike)

This workshop is a 4-part beginner-friendly journey from Matplotlib basics to an interactive Dash dashboard. We use one dataset and a single narrative throughout:

"What drives Citi Bike usage patterns in NYC?"

By the end, you will build a small dashboard that explores usage over time, rider types, trip durations, and station hotspots.

## Learning Outcomes
- Load, clean, and reuse a real-world dataset
- Build clear Matplotlib charts and style them for readability
- Use Seaborn for statistical plots and Plotly for interactive charts
- Create a simple Dash app with filters and linked charts

## Repository Structure
```
viz-workshop/
  README.md
  requirements.txt
  data/
    raw/
    processed/
  notebooks/
    00_introduction.ipynb
    01_matplotlib_basics.ipynb
    02_matplotlib_styling.ipynb
    03_seaborn_plotly.ipynb
    04_dash_showcase.ipynb
  src/
    data_prep.py
    viz_helpers.py
```

## How to Run Locally
1. Create a virtual environment.
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Open the notebooks in VS Code or Jupyter and run in order.

## How to Run in Colab
- Upload the `viz-workshop` folder to Colab or your Drive.
- Open the notebooks in order and run top-to-bottom.
- Each notebook includes a "Run this first" cell that installs dependencies and sets paths.

## Dataset Citation
Data source: Citi Bike System Data / Trip Histories.
- Official system data page: https://citibikenyc.com/system-data
- Files are hosted on the official trip data bucket: https://tripdata.s3.amazonaws.com/

This workshop downloads one recent month of data, then samples to a smaller size for speed.

## Troubleshooting
- Install issues: restart the runtime and re-run the install cell.
- Plotly rendering: make sure `plotly` is installed and run the import cell first.
- Dash in Colab: use the provided JupyterDash cell and follow the "open link" instruction if inline render fails.

## Notes on File Size and Sampling
The raw monthly file can be large. The notebooks automatically cache a sampled and cleaned dataset in `data/processed/` for faster reruns.
