import os
from datetime import datetime
from pathlib import Path

import indrafetch
import yaml
from dotenv import load_dotenv
from indradaily import emails

YAML_PATH = "src/indradaily/config/cds_daily_params.yaml"

def set_custom_loggers(debug=True, info=True):

    current_month = datetime.now().strftime("%Y-%m")

    base_logger_path = Path("logs")
    debug_logger_path = base_logger_path / Path(f"indrafetch-{current_month}-debug.log")

    os.makedirs(base_logger_path, exist_ok=True)

    loggers_config = dict()
    loggers_config['indrafetch'] = {
        'level': 'DEBUG',
        'filename': debug_logger_path,
    }

    return loggers_config

def get_params(yaml_path):
    with open(yaml_path, 'r') as file:
        params = yaml.safe_load(file)
    return params

def draft_and_send_email(upload_success: bool, yaml_path: str, no_files: int,
                         latest_timestamp: datetime, attachment: bool = False):
    params = get_params(yaml_path=yaml_path)
    recipients = params['email_recipients']
    load_dotenv()
    config = {
        'SMTP_SERVER': os.getenv('SMTP_SERVER'),
        'PORT': os.getenv('PORT'),
        'EMAIL': os.getenv('EMAIL'),
        'PASSWORD': os.getenv('PASSWORD')
    }

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_month = datetime.now().strftime("%Y-%m")
    log_file = f"logs/indrafetch-{current_month}-debug.log"

    latest_timestamp = latest_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    attachment_path = log_file

    if upload_success:
        status = "SUCCESSFUL"
        body = f"""Hello,
This is a system generated email. {no_files} files obtained from CDS ERA5 have been successfully uploaded to S3 on {current_date}.
The last timestamp of data availability CDS ERA5 is {latest_timestamp}, when checked at {current_timestamp}.
Detailed health of the run can be found in the debug log file for the current month on the server: {log_file}.
"""
    else:
        status = "FAILED"
        subject = "ERA5 Daily data upload to S3 failed"
        body = f"""Hello,
This is a system generated email. CDS ERA5 Daily data has FAILED to uploaded to S3 on {current_date}.
The last timestamp of data availability on CDS ERA5 is {latest_timestamp}, when checked at {current_timestamp}.
Detailed health of the run can be found in the debug log file, attached.
The log file is attached.
        """
        attachment=True

    subject = f"ERA5 Daily Data Run {status} on {current_date}"
    emails.send_email(recipients=recipients, subject=subject, body=body, config=config,
                      attachment=attachment, attachment_path=attachment_path)

    return True

def main(yaml_path: str, current_month: bool=True, direct_upload: bool=False):
    loggers_config = set_custom_loggers()
    indrafetch.setup_logging(loggers_config=loggers_config, default_level='DEBUG')

    params = get_params(yaml_path=yaml_path)

    latest_timestamp, _ = indrafetch.last_date_of_cds_data()

    if current_month:
        start_date = latest_timestamp.strftime("%Y-%m-01")
        end_date = latest_timestamp.strftime("%Y-%m-%d")
        params["start_date"] = start_date
        params["end_date"] = end_date

    region_specific_output_dir = Path(params['output_dir']) / Path(params['region'].upper())

    if not direct_upload:
        indrafetch.retrieve_data_from_cds(bounds_nwse=params['bounds_nwse'][params['region']], variables=list(params['variables'].keys()),
                                          output_dir=region_specific_output_dir,
                                          start_date=params["start_date"], end_date=params["end_date"],
                                          variable_code_dict = params['variables'], region=params['region'],
                                          check_credentials=False
                                         )
    no_files = len(list(region_specific_output_dir.glob('*.nc')))
    upload_success = indrafetch.upload_cds_data_to_s3(upload_dir=region_specific_output_dir, region=params['region'],
                                                      Bucket=params['s3_bucket'], Prefix=params['s3_prefix'])

    return upload_success, no_files, latest_timestamp


if __name__ == "__main__":
    # upload_success, no_files, latest_timestamp = main(yaml_path=YAML_PATH)
    # draft_and_send_email(upload_success=upload_success, yaml_path=YAML_PATH, no_files=no_files, latest_timestamp=latest_timestamp)
    latest_timestamp = indrafetch.last_date_of_cds_data()[0]
    draft_and_send_email(upload_success=False, yaml_path=YAML_PATH, no_files=0, latest_timestamp=latest_timestamp)
