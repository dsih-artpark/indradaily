import argparse
from pathlib import Path

import indrafetch
from dotenv import load_dotenv
from indradaily import get_params, set_custom_loggers
from indradaily.emails import data_upload_email


def main(*, cds_params: dict, shared_params: dict, current_month: bool=True, direct_upload: bool=False, log_level: str='DEBUG'):
    loggers_config = set_custom_loggers(level=log_level)
    indrafetch.setup_logging(loggers_config=loggers_config, default_level=log_level)

    latest_timestamp, _ = indrafetch.last_date_of_cds_data()

    if current_month:
        start_date = latest_timestamp.strftime("%Y-%m-01")
        end_date = latest_timestamp.strftime("%Y-%m-%d")
        cds_params["start_date"] = start_date
        cds_params["end_date"] = end_date
    
    upload_successes = []
    total_no_files = 0

    for i, region in enumerate(cds_params['bounds_nwse'].keys()):
        s3_prefix = f"{cds_params['ds_id']}-{cds_params['ds_name']}/{cds_params['folder_name']}/{region.upper()}"
        local_region_dir = Path(shared_params['local_data_dir']).expanduser() / Path(shared_params['s3_bucket']) / Path(s3_prefix)
        local_region_dir.mkdir(parents=True, exist_ok=True)
        if not direct_upload:
            indrafetch.retrieve_data_from_cds(bounds_nwse=cds_params['bounds_nwse'][region], variables=list(cds_params['variables'].keys()),
                                              output_dir=local_region_dir,
                                              start_date=cds_params["start_date"], end_date=cds_params["end_date"],
                                              variable_code_dict = cds_params['variables'], region=region,
                                              check_credentials=False
                                              )

        no_files = len(list(local_region_dir.glob(f'*.{cds_params["extension"]}')))
        load_dotenv()
        upload_success = indrafetch.upload_data_to_s3(upload_dir=local_region_dir, Bucket=shared_params['s3_bucket'],
                                                      Prefix=s3_prefix, extension=cds_params['extension'])

        upload_successes.append(upload_success)
        total_no_files += no_files

    if all(upload_successes):
        return True, total_no_files, latest_timestamp
    else:
        return False, total_no_files, latest_timestamp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process CDS ERA5 daily data')
    parser.add_argument('-y', '--yaml_path', required=True, help='Path to YAML configuration file')
    parser.add_argument('-l', '--log_level', required=False, help='Log level', default='DEBUG')
    parser.add_argument('-d', '--direct_upload', action="store_true", help='Boolean to directly upload to s3, useful for testing')
    parser.add_argument('-c', '--current_month', action="store_false", help='Boolean to use current month as date range for data retrieval')
    args = parser.parse_args()

    params = get_params(yaml_path=args.yaml_path)
    cds_params = params['cds']
    shared_params = params['shared_params']

    upload_success, no_files, latest_timestamp = main(cds_params=cds_params, shared_params=shared_params,
                                                      log_level=args.log_level, direct_upload=args.direct_upload,
                                                      current_month=args.current_month)
    data_upload_email(upload_success=upload_success, recipients=shared_params['email_recipients'],
                      dataset_name=cds_params['ds_name'].replace('_', ' '), dataset_source=cds_params['ds_source'],
                      no_files=no_files, latest_timestamp=latest_timestamp)
