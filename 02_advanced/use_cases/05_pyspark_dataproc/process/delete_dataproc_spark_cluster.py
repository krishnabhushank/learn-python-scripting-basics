import argparse
import configparser
import logging.config
import sys

from google.cloud import dataproc_v1
from google.oauth2 import service_account


def delete_cluster() -> int:
    region = config['pyspark_dataproc']['REGION']

    job_status = 'SUCCESS'
    try:
        service_acc_file_path = config['google_credentials']['SERVICE_ACCOUNT_FILE_PATH']
        credentials = service_account.Credentials.from_service_account_file(service_acc_file_path)

        # Create the cluster client.
        cluster_client = dataproc_v1.ClusterControllerClient(
            client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"},
            credentials=credentials
        )
        logger.info("Using Below Config")
        logger.info(dict(config['pyspark_dataproc']))

        # Delete the cluster.
        operation = cluster_client.delete_cluster(
            request={
                "project_id": config['pyspark_dataproc']['TARGET_PROJECT'],
                "region": config['pyspark_dataproc']['REGION'],
                "cluster_name": config['pyspark_dataproc']['CLUSTER_NAME']
            }
        )
        result = operation.result()

        logger.info(result)
    except BaseException as e:
        job_status = 'FAIL'
        logger.exception(e)

    logger.info(f"status : {job_status}")
    li_rc = 0
    if job_status == 'FAIL':
        li_rc = 1
    return li_rc


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Create GCP Dataproc Cluster')
    parser.add_argument('-P', '--profile',
                        help='Path to INI/Configuration File',
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

    rc = delete_cluster()
    # process('20220724')
    logger.info("Script completed... : " + str(rc))
    sys.exit(rc)
