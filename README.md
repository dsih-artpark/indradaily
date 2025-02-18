# Indradaily - Getting Started
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

The configuration for the data retrieval is specified in a YAML file. Below is an example configuration:

```yaml
shared_params:
  local_data_dir: "~/.data-folder/"
  email_recipients:
    "sample@example.com": "Sample User"
  s3_bucket: 'sample-s3-bucket'


cds:
  cds_dataset_name: "reanalysis-era5-single-levels"
  bounds_nwse:
    ka: [19,74,11,79]
  variables:
    "2m_temperature": "2t"
    "2m_dewpoint_temperature": "2d"
    "total_precipitation": "tp"
    "10m_u_component_of_wind": "10u"
    "10m_v_component_of_wind": "10v"
  start_date: None
  end_date: None
ds_id: 'dsid_cds'
  ds_name: "ERA5_Reanalysis_Single_Level"
  folder_name: "all_india_netcdf"
  ds_source: "ECMWF CDS"
  extension: "nc"

ecpds:
  url: 'https://data.ecmwf.int/forecasts'
  zulu_utc_timestamp: '00z'
  resolution: '0p25'
  model: 'ifs'
  forecast_type: 'oper'
  forecast_times: ["0h", "6h"]
  raise_error: true
  chunk: true
  chunk_size: 1048576
  ds_id: 'dsid_ecpds'
  ds_name: 'ECPDS_Operational_Forecasts'
  folder_name: '00z_ifs_0p25_oper'
  ds_source: 'ECMWF ECPDS'
  extensions: ["grib2", "index"]
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
