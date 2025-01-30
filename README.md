# Indradaily
Indradaily is a Python package designed to fetch and process ERA5 reanalysis data for specific regions and upload the processed data to an S3 bucket.

## Installation

First, create a conda environment and install the dependencies:

```sh
conda create --name indradaily python=3.10 -y
conda activate indradaily
```

Then, use Poetry to install the package:

```sh
poetry install
```

## Usage

### Configuration

The configuration for the data retrieval is specified in a YAML file. Below is an example configuration (`era5_daily_params.yaml`):

```yaml
region: "ka"
bounds_nwse:
    ka: [19,74,11,79]
variables:
    "2m_temperature": "2t"
    "2m_dewpoint_temperature": "2d"
    "total_precipitation": "tp"
    "10m_u_component_of_wind": "10u"
    "10m_v_component_of_wind": "10v"
output_dir: ".dsih-data/era5"
start_date: "2025-01-01"
end_date: "2025-01-01"
s3_bucket: "dsih-artpark-03-standardised-data"
s3_prefix: "MW0016DS0046-ERA5_Reanalysis_Single_Level/all_india_netcdf"
```

### Running the Script

To run the script, execute the following command:

```sh
python era5_daily.py
```

This will fetch the data for the specified region and time period, and upload it to the specified S3 bucket.

## Project Structure

- `era5_daily.py`: Main script to fetch and upload ERA5 data.
- `era5_daily_params.yaml`: Configuration file for specifying parameters.
- `pyproject.toml`: Project metadata and dependencies.

## TO DO
1. Main should recieve command line arguments as appropriate, esp for YAML file.

## License

This project is licensed under the GPL-3.0-or-later License.

## Authors

- Sneha S <sneha@artpark.in>
- Aishwarya R <aishwarya@artpark.in>
