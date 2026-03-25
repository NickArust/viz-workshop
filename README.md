# We will keep the accounts active for a week (until 3/31/26 at 4pm). After that time, the virtual machine will be closed and all accounts will be deactivated. Please use this time to experiment with the code and get it set up and running on your own local machine if you wish


# Beginner Data Visualization Workshop (Citi Bike)

This workshop is a beginner-friendly journey from Matplotlib basics to an interactive Dash dashboard. We use one dataset and a single narrative throughout:

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
├── README.md
├── data
│   ├── processed
│   │   └── 202510-citibike-tripdata_1.csv
│   └── raw
├── notebooks
│   ├── data
│   ├── outputs
│   ├── presenters
│   │   ├── 00_introduction.ipynb
│   │   ├── 01_matplotlib_basics.ipynb
│   │   ├── 02_matplotlib_styling.ipynb
│   │   ├── 03_seaborn_plotly.ipynb
│   │   └── 04_dash_showcase.ipynb
│   └── students
│       ├── 00_introduction.ipynb
│       ├── 01_matplotlib_basics.ipynb
│       ├── 02_matplotlib_styling.ipynb
│       ├── 03_seaborn_plotly.ipynb
│       └── 04_dash_showcase.ipynb
├── requirements.txt
└── src
    ├── __pycache__
    │   ├── data_prep.cpython-312.pyc
    │   └── viz_helpers.cpython-312.pyc
    ├── data_prep.py
    └── viz_helpers.py
```

## Running the Notebooks

You can run the notebooks in this workshop in **three different ways** depending on your setup and experience level.

---

## Option 1 — Run Locally with Jupyter (Recommended)

This option gives you the most control and works well if you plan to continue using Python for data analysis.

### Step 1 — Install Python

Download and install Python (version **3.9 or newer**):

https://www.python.org/downloads/

During installation, make sure to check:` Add Python to PATH`


---

### Step 2 — Download the Repository

You can either:

#### Option A — Download ZIP

1. Go to the GitHub repository page
2. Click: `Code` -> `Download ZIP`
3. Extract the folder to your computer

#### Option B — Clone with Git
git clone https://github.com/YOUR_USERNAME/viz-workshop.git

cd viz-workshop

---

### Step 3 — Create a Virtual Environment

Open a terminal inside the project folder and run:
```
python -m venv venv 
```

Activate it:

**Mac / Linux**

` source venv/bin/activate `


**Windows**
`venv\Scripts\activate`



---

### Step 4 — Install Dependencies



pip install -r requirements.txt


---

### Step 5 — Launch Jupyter


`jupyter notebook`


or
`jupyter lab`



---

## Option 2 — Run in Google Colab (No Installation Required)

This is the easiest option for beginners or workshop settings.

### Step 1 — Open Google Colab

Go to:

https://colab.research.google.com

---

### Step 2 — Upload the Workshop Folder

You can:

- Upload the ZIP file, or  
- Upload the folder to Google Drive  

---

### Step 3 — Open a Notebook

In Colab:


File → Open notebook → Upload


or open from Google Drive.

---

### Step 4 — Run the Notebook

Click:
`Runtime → Run all`


Each notebook includes a setup cell that installs required packages automatically.

---

## Option 3 — Run in VS Code

If you already use VS Code, this is often the smoothest workflow.

### Install Extensions

- Python  
- Jupyter  

Then:

1. Open the project folder in VS Code  
2. Select the Python interpreter  
3. Open any notebook  
4. Click:


`Run All`



## Dataset Citation
Data source: Citi Bike System Data / Trip Histories.
- Official system data page: https://citibikenyc.com/system-data
- Files are hosted on the official trip data bucket: https://tripdata.s3.amazonaws.com/

This workshop downloads one recent month of data, then samples to a smaller size for speed.

## Troubleshooting
- Install issues: restart the runtime and re-run the install cell.
- Plotly rendering: make sure `plotly` is installed and run the import cell first.

## Notes on File Size and Sampling
The raw monthly file can be large. The notebooks automatically cache a sampled and cleaned dataset in `data/processed/` for faster reruns.
