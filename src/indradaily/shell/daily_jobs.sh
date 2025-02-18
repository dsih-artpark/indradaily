#!/bin/bash
set -e  # Exit immediately if a command fails

# Define environment variables
PROJ_ROOT="${HOME}/code/indradaily"
CONDA_ROOT="${HOME}/miniconda3"  # Change this if using Anaconda instead
CONDA_ENV="indradaily_prod"
CONDA_PYTHON="${CONDA_ROOT}/envs/${CONDA_ENV}/bin/python"

# Change to project directory
cd "${PROJ_ROOT}" || exit 1

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
# To add new dependencies:
#   poetry add package_name
#
# To install only production dependencies:
#   poetry install --no-dev
# =====================================================

# Run CDS daily job
"${CONDA_PYTHON}" src/indradaily/jobs/cds_daily.py -y ~/.dsih-config/weather-data-jobs.yaml

# Run ECPDS daily job
"${CONDA_PYTHON}" src/indradaily/jobs/ecpds_daily.py -y ~/.dsih-config/weather-data-jobs.yaml

# Return to home directory
cd "${HOME}"

# Set timezone to UTC
# sudo timedatectl set-timezone UTC

# Run the script every day at 09:00, this command is for crontab
# * 9 * * * ${HOME}/code/indradaily/src/indradaily/shell/daily_jobs.sh >> daily_jobs.log 2>&1