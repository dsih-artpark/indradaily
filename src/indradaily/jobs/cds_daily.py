import argparse
from pathlib import Path

import indrafetch
from dotenv import load_dotenv
from indradaily import get_params, set_custom_loggers
from indradaily.emails import draft_and_send_email


def main(*, yaml_path: str, current_month: bool=True, direct_upload: bool=False, log_level: str='DEBUG'):
    loggers_config = set_custom_loggers(level=log_level)
    indrafetch.setup_logging(loggers_config=loggers_config, default_level=log_level)

    params = get_params(yaml_path=yaml_path)

    latest_timestamp, _ = indrafetch.last_date_of_cds_data()

    if current_month:
        start_date = latest_timestamp.strftime("%Y-%m-01")
        end_date = latest_timestamp.strftime("%Y-%m-%d")
        params["start_date"] = start_date
        params["end_date"] = end_date

    region_specific_output_dir = Path(params['output_dir']) / Path(params['region'].upper())
    region_specific_output_dir.mkdir(parents=True, exist_ok=True)
    if not direct_upload:
        indrafetch.retrieve_data_from_cds(bounds_nwse=params['bounds_nwse'][params['region']], variables=list(params['variables'].keys()),
                                          output_dir=region_specific_output_dir,
                                          start_date=params["start_date"], end_date=params["end_date"],
                                          variable_code_dict = params['variables'], region=params['region'],
                                          check_credentials=False
                                         )

    no_files = len(list(region_specific_output_dir.glob(f'*.{params["extension"]}')))
    load_dotenv()
    upload_success = indrafetch.upload_data_to_s3(upload_dir=region_specific_output_dir, Bucket=params['s3_bucket'],
                                                  Prefix=f"{params['s3_prefix']}/{params['region'].upper()}", extension=params['extension'])

    return upload_success, no_files, latest_timestamp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process CDS ERA5 daily data')
    parser.add_argument('-y', '--yaml_path', required=True, help='Path to YAML configuration file')
    parser.add_argument('-l', '--log_level', required=False, help='Log level', default='DEBUG')
    parser.add_argument('-d', '--direct_upload', action="store_true", help='Boolean to directly upload to s3, useful for testing')
    parser.add_argument('-c', '--current_month', action="store_false", help='Boolean to use current month as date range for data retrieval')
    args = parser.parse_args()

    upload_success, no_files, latest_timestamp = main(yaml_path=args.yaml_path,
                                                      log_level=args.log_level, direct_upload=args.direct_upload,
                                                      current_month=args.current_month)
    draft_and_send_email(upload_success=upload_success, yaml_path=args.yaml_path,
                         no_files=no_files, latest_timestamp=latest_timestamp)
