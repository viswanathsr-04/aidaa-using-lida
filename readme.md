# AIDAA - AI Data Analysis Application

## Overview

This is a Streamlit application that uses Microsoft's LIDA and Google's PaLM API to generate visualizations from uploaded data. It allows users to upload data files in CSV, Excel, or JSON format and then generate charts based on the uploaded data and user-specified queries.

## Features

- Upload data files in CSV, Excel, or JSON format
- Generate charts using various visualization libraries (seaborn, plotly, matplotlib, altair, ggplot)
- Visualize data based on user-specified queries

## Getting Started

1. Clone this repository using `git clone https://github.com/your-username/your-repo-name.git`
2. Create a virtual environment in python using `python -m venv <venv_name>`
3. Activate the virtual environment using `<venv_name>\Scripts\activate`
4. Install the required libraries using `pip install -r requirements.txt`
5. It is important to include your PaLM API service account key from Vertex AI in your local environment as environment variables.
6. Run the application in the terminal using `streamlit run app.py`

## Usage

1. Upload your data file in the sidebar
2. Enter your desired visualization query in the text area
3. Click the "Generate Charts" button to generate the visualization
