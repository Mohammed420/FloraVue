#!/bin/bash

echo "----------------------------------------"
echo "Launching Streamlit App..."
echo "Please wait while the server starts!"
echo "----------------------------------------"

# Change to the directory where this script is
cd "$(dirname "$0")"

# Run the Streamlit app
streamlit run app.py
