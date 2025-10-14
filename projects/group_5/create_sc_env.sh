#!/bin/bash

# Define the name of your Conda environment
ENV_NAME="sc_analysis_env"

# List of packages to install from conda-forge and defaults
PACKAGES=(
    "python=3.10" # Specify a Python version
    "anndata"
    "pandas"
    "numpy"
    "scipy"
    "matplotlib"
    "seaborn"   # For enhanced statistical plots
    "scanpy"    # The main single-cell analysis library built on AnnData
    "hdf5plugin" # Recommended for performance with h5ad files
    "ipykernel" # To use this env in Jupyter notebooks
)

echo "Creating Conda environment: $ENV_NAME"
echo "This might take a few minutes..."

# Create the Conda environment, explicitly adding conda-forge channel
# We also include 'defaults' to ensure standard packages are still found
conda create -n "$ENV_NAME" -c conda-forge -c defaults "${PACKAGES[@]}" -y

# Check if the environment creation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "Conda environment '$ENV_NAME' created successfully!"
    echo "Installing gseapy from bioconda channel..."
    
    # Activate the environment and install gseapy from bioconda
    conda install -n "$ENV_NAME" -c bioconda gseapy -y
    
    if [ $? -eq 0 ]; then
        echo "gseapy installed successfully!"
    else
        echo "Warning: Failed to install gseapy. You can install it manually later with:"
        echo "conda activate $ENV_NAME && conda install -c bioconda gseapy"
    fi
    
    echo ""
    echo "To activate this environment, run:"
    echo "conda activate $ENV_NAME"
    echo ""
    echo "Once activated, if you want to use this environment in Jupyter notebooks,"
    echo "run the following commands (within the activated environment):"
    echo "conda install -y ipykernel" # ipykernel is usually in defaults or conda-forge, but explicit install is good
    echo "python -m ipykernel install --user --name=$ENV_NAME --display-name \"Python ($ENV_NAME)\""
else
    echo ""
    echo "Error: Conda environment creation failed."
    echo "Please check the error messages above."
    echo "Tip: Ensure you have an active internet connection and try again."
fi