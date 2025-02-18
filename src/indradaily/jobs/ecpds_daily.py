import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

import indrafetch
from dotenv import load_dotenv

from indradaily import get_params, set_custom_loggers
from indradaily.emails import data_upload_email


def main(*, get_latest_date: bool=True, custom_date: Optional[datetime]=None, shared_params: dict, ecpds_params: dict,
         direct_upload: bool=False, log_level: str='DEBUG'):
    """
    Main function to retrieve and upload ECPDS data to S3.

    :param get_latest_date: bool
        If True, retrieve the latest date of the data available in the ECPDS.
    :param custom_date: Optional[datetime]
        The date to retrieve data for, format: YYYY-MM-DD.
    :param shared_params: dict
        A dictionary of shared parameters.
    :param ecpds_params: dict
        A dictionary of ECPDS parameters.
    :param direct_upload: bool
        If True, directly upload the data to S3.
    :param log_level: str
        The log level to use for the logger.

    :return: tuple
        A tuple containing the upload success, the number of files uploaded, and the latest date of the data available in the ECPDS.

    :raises Exception:
        If the data fails to upload, an exception is raised.
    """

    loggers_config = set_custom_loggers(level=log_level)
    indrafetch.setup_logging(loggers_config=loggers_config, default_level=log_level)

    latest_date = indrafetch.last_date_of_ecpds_data()

    s3_prefix = f"{ecpds_params['ds_id']}-{ecpds_params['ds_name']}/{ecpds_params['folder_name']}/{latest_date.strftime('%Y')}"
    local_region_dir = Path(shared_params['local_data_dir']).expanduser() / Path(shared_params['s3_bucket']) / Path(s3_prefix)
    local_region_dir.mkdir(parents=True, exist_ok=True)

    if not direct_upload:
        indrafetch.retrieve_data_from_ecpds(get_latest_date=get_latest_date, custom_date=custom_date, ecpds_base_url=ecpds_params['url'],
                                            output_dir=local_region_dir, zulu_utc_timestamp=ecpds_params['zulu_utc_timestamp'],
                                            resolution=ecpds_params['resolution'],
                                            model=ecpds_params['model'], forecast_type=ecpds_params['forecast_type'],
                                            forecast_times=ecpds_params['forecast_times'],
                                            raise_error=ecpds_params['raise_error'], chunk=ecpds_params['chunk'],
                                            chunk_size=ecpds_params['chunk_size'])


    upload_success = [None] * len(ecpds_params['extensions'])
    no_files = [None] * len(ecpds_params['extensions'])

    for i, extension in enumerate(ecpds_params['extensions']):
        no_files[i] = len(list(local_region_dir.glob(f"*.{extension}")))
        load_dotenv()
        upload_success[i] = indrafetch.upload_data_to_s3(upload_dir=local_region_dir, Bucket=shared_params['s3_bucket'],
                                     Prefix=s3_prefix, extension=extension)

    upload_success = all(upload_success)
    no_files = sum(no_files)

    return upload_success, no_files, latest_date


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process ECPDS daily data')
    parser.add_argument('-g', '--get_latest_date', action="store_false", help='Boolean to get latest date of data available in ECPDS')
    parser.add_argument('-y', '--yaml_path', required=True, help='Path to YAML configuration file')
    parser.add_argument('-l', '--log_level', required=False, help='Log level', default='DEBUG')
    parser.add_argument('-d', '--direct_upload', action="store_true", help='Boolean to directly upload to s3, useful for testing')
    parser.add_argument('-c', '--custom_date', required=False, help='Custom date to retrieve data for, format: YYYY-MM-DD', default=None)
    args = parser.parse_args()

    params = get_params(yaml_path=args.yaml_path)
    ecpds_params = params['ecpds']
    shared_params = params['shared_params']

    if args.custom_date is not None:
        custom_date = datetime.strptime(args.custom_date, '%Y-%m-%d')
    else:
        custom_date = None

    upload_success, no_files, latest_date = main(get_latest_date=args.get_latest_date, custom_date=custom_date, shared_params=shared_params,
                                                 ecpds_params=ecpds_params, direct_upload=args.direct_upload)
    data_upload_email(upload_success=upload_success, recipients=shared_params['email_recipients'],
                      dataset_name=ecpds_params['ds_name'].replace('_', ' '), dataset_source=ecpds_params['ds_source'],
                      no_files=no_files, latest_timestamp=latest_date)

__all__ = ["main"]
