#!/bin/bash
set -e  # Exit immediately if a command fails

# Define environment variables
PROJ_ROOT="${HOME}/jobs/indradaily"
CONDA_ROOT="${HOME}/miniconda3"  # Change this if using Anaconda instead
CONDA_ENV="indradaily_prod"
CONDA_PYTHON="${CONDA_ROOT}/envs/${CONDA_ENV}/bin/python"

# Change to project directory
cd "${PROJ_ROOT}/src/indradaily" || exit 1

# =====================================================
# Environment Setup Instructions
# =====================================================
# Prerequisites:
#   1. Install Poetry: curl -sSL https://install.python-poetry.org | python3 -
#   2. Install Conda (if not already installed)
#
# Initial Setup:
#   conda create -n ${CONDA_ENV} python=3.9  # Adjust Python version as needed
#   conda activate ${CONDA_ENV}
#   poetry env use $(which python)  # Use conda's Python
#   poetry install  # Installs dependencies from pyproject.toml
#
# To update dependencies:
#   conda activate ${CONDA_ENV}
#   poetry update  # Updates to latest versions within constraints
#
# To add new dependencies:
#   poetry add package_name
#
# To install only production dependencies:
#   poetry install --no-dev
# =====================================================

# Run CDS daily job
"${CONDA_PYTHON}" jobs/cds_daily.py -y config/cds_daily_params.yaml

# Run ECPDS daily job
"${CONDA_PYTHON}" jobs/ecpds_daily.py -y config/ecpds_daily_params.yaml

# Return to home directory
cd "${HOME}"