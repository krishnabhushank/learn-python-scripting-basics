import argparse
import configparser
import json
import datetime as dt
import logging.config
import re
import sys
import uuid

from google.oauth2 import service_account
from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage

from dp_run_sears.models.sears_static import sears_static_table
from lib.run_bigquery import runbq


def submit_job(my_data_run_datetime, my_harlem125_uploaded_blobs, my_sears_online_rule_uploaded_blobs) -> int:
    region = config['pyspark_dataproc']['REGION']

    job_status = 'SUCCESS'
    try:
        service_acc_file_path = config['google_credentials']['SERVICE_ACCOUNT_FILE_PATH']
        credentials = service_account.Credentials.from_service_account_file(service_acc_file_path)

        # Create the job client.
        job_client = dataproc.JobControllerClient(
            client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"},
            credentials=credentials
        )

        logger.info("Using Below Config")
        logger.info(json.dumps(dict(config['pyspark_dataproc']), indent = 4))
        logger.info(".. and Below Config")
        logger.info(json.dumps(dict(config['pyspark_job']), indent = 4))

        harlem125_package = list(filter(lambda x: '.egg' in x, my_harlem125_uploaded_blobs))[0]
        dp_rules_package = list(filter(lambda x: '.egg' in x, my_sears_online_rule_uploaded_blobs))[0]
        entry = list(filter(lambda x: 'main.py' in x, my_sears_online_rule_uploaded_blobs))[0]

        # Create the job config.
        job = {
            "placement": {"cluster_name": config['pyspark_dataproc']['CLUSTER_NAME']},
            "pyspark_job": {
                "main_python_file_uri": entry,
                "args": [
                    f"--prefix={config['pyspark_job']['TARGET_PREFIX']}",
                    f"--datetime={my_data_run_datetime['datetime']}",
                    f"--run_id={data_run_datetime['run_id']}",
                ],
                "python_file_uris": [
                    harlem125_package,
                    dp_rules_package
                ]
            },
        }
        
        request_id = f"run_job-{my_data_run_datetime['next_execution_date_nodash']}-{data_run_datetime['run_id']}"
        operation = job_client.submit_job_as_operation(
            request={
                "project_id": config['pyspark_dataproc']['TARGET_PROJECT'],
                "region": config['pyspark_dataproc']['REGION'],
                "job": job,
                "request_id": request_id 
            },
            timeout=40
        )
        response = operation.result()

        logger.info(f"result: {response}")
        # Dataproc job output gets saved to the Google Cloud Storage bucket
        # allocated to the job. Use a regex to obtain the bucket and blob info.
        matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)

        output = (
            storage.Client(project=config['pyspark_dataproc']['TARGET_PROJECT'],
                           credentials=credentials)
            .get_bucket(matches.group(1))
            .blob(f"{matches.group(2)}.000000000")
            .download_as_bytes().decode("utf-8")
        )

        logger.info("Output is as follows")
        print(output)

    except BaseException as e:
        job_status = 'FAIL'
        logger.exception(e)

    logger.info(f"status : {job_status}")
    li_rc = 0
    if job_status == 'FAIL':
        li_rc = 1
    return li_rc


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Build Query for Sears_Static and Execute')
    parser.add_argument('-P', '--profile',
                        help='Path to INI/Configuration File',
                        required=True)
    parser.add_argument('--run_datetime_json_file',
                        help='Run Datetime JSON file',
                        required=True)
    parser.add_argument('--harlem125_uploaded_blobs_json_file',
                        help='Harlem125 Uploaded Blobs JSON file',
                        required=True)
    parser.add_argument('--sears_online_rule_uploaded_blobs_json_file',
                        help='Sears Online_Rule Uploaded Blobs JSON file',
                        required=True)

    results = parser.parse_args(args)
    return results


if __name__ == '__main__':
    res = check_arg(sys.argv[1:])
    lc_configFile = res.profile

    logging.config.fileConfig(lc_configFile)

    # Create logger
    global logger
    logger = logging.getLogger('dpRun')

    logger.info("Using Config from " + str(lc_configFile))

    global config
    config = configparser.ConfigParser()
    config.read(lc_configFile)

    data_run_datetime = None
    try:
        with open(res.run_datetime_json_file, 'r') as handle:
            data_run_datetime = json.load(handle)
    except BaseException as e:
        logger.exception(e)
        logger.info("Script completed... : 1")
        sys.exit(1)

    harlem125_uploaded_blobs = None
    try:
        with open(res.harlem125_uploaded_blobs_json_file, 'r') as handle:
            harlem125_uploaded_blobs = json.load(handle)
    except BaseException as e:
        logger.exception(e)
        logger.info("Script completed... : 1")
        sys.exit(1)

    sears_online_rule_uploaded_blobs = None
    try:
        with open(res.sears_online_rule_uploaded_blobs_json_file, 'r') as handle:
            sears_online_rule_uploaded_blobs = json.load(handle)
    except BaseException as e:
        logger.exception(e)
        logger.info("Script completed... : 1")
        sys.exit(1)

    rc = submit_job(my_data_run_datetime=data_run_datetime,
                    my_harlem125_uploaded_blobs=harlem125_uploaded_blobs['blob_lst'],
                    my_sears_online_rule_uploaded_blobs=sears_online_rule_uploaded_blobs['blob_lst'])
    # process('20220724')
    logger.info("Script completed... : " + str(rc))
    sys.exit(rc)
