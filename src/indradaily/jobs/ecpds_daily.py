import argparse
from pathlib import Path
from typing import Optional

import indrafetch
from dotenv import load_dotenv
from indradaily import get_params, set_custom_loggers
from indradaily.emails import draft_and_send_email


def main(*, yaml_path: str, latest_date: bool=True, date: Optional[str]=None, direct_upload: bool=False, log_level: str='DEBUG'):
    loggers_config = set_custom_loggers(level=log_level)
    indrafetch.setup_logging(loggers_config=loggers_config, default_level=log_level)

    params = get_params(yaml_path=yaml_path)
    output_dir = Path(params['output_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    if not direct_upload:
        indrafetch.retrieve_data_from_ecpds(latest_date=latest_date, date=date, ecpds_base_url=params['url'],
                                            output_dir=output_dir, zulu_utc_timestamp=params['zulu_utc_timestamp'],
                                            resolution=params['resolution'],
                                            model=params['model'], forecast_type=params['forecast_type'],
                                            forecast_times=params['forecast_times'],
                                            raise_error=params['raise_error'], chunk=params['chunk'], chunk_size=params['chunk_size'])

    latest_date = indrafetch.last_date_of_ecpds_data()
    upload_success = [None] * len(params['extensions'])
    no_files = [None] * len(params['extensions'])

    for i, extension in enumerate(params['extensions']):
        no_files[i] = len(list(output_dir.glob(f"*.{extension}")))
        upload_success[i] = indrafetch.upload_data_to_s3(upload_dir=output_dir, Bucket=params['s3_bucket'],
                                     Prefix=f"{params['s3_prefix']}{latest_date.strftime('%Y')}", extension=extension)

    load_dotenv()

    upload_success = all(upload_success)
    no_files = sum(no_files)

    return upload_success, no_files, latest_date


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process ECPDS daily data')
    parser.add_argument('-y', '--yaml_path', required=True, help='Path to YAML configuration file')
    parser.add_argument('-l', '--log_level', required=False, help='Log level', default='DEBUG')
    parser.add_argument('-d', '--direct_upload', action="store_true", help='Boolean to directly upload to s3, useful for testing')
    args = parser.parse_args()

    upload_success, no_files, latest_date = main(yaml_path=args.yaml_path, direct_upload=args.direct_upload)
    draft_and_send_email(upload_success=upload_success, yaml_path=args.yaml_path,
                         no_files=no_files, latest_timestamp=latest_date)
