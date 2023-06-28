import argparse
import json
import os
import sys
import glob
import subprocess as sp
import uuid
import logging.config
import configparser
import shutil
from urllib.parse import urlparse

from google.cloud import storage
from google.oauth2 import service_account


def build_egg_and_upload_to_gcs(build_config='bdist_egg',
                                gcs_base=None,
                                local_base=None,
                                staging_base=None,
                                upload_lst=['/dist/*.egg'],
                                output_file=None):
    job_status = 'SUCCESS'
    try:
        shutil.copytree(local_base, staging_base)
        # bucket, blobpath = _parse_gcs_url(gcs_base)

        ''' Given  _parse_gcs_url a Google Cloud Storage URL (gs://<bucket>/<blob>), returns a
        tuple containing the corresponding bucket and blob.'''
        gcs_base = gcs_base + '/{}'.format(uuid.uuid4())
        parsed_url = urlparse(gcs_base)
        bucket = parsed_url.netloc
        blob_path = parsed_url.path.lstrip('/')

        repo_folder = str(uuid.uuid4())[-8:]
        '''base = GoogleCloudBaseHook(google_cloud_storage_conn_id)
        cred = base._get_credentials()'''
        service_acc_file_path = config['google_credentials']['SERVICE_ACCOUNT_FILE_PATH']
        credentials = service_account.Credentials.from_service_account_file(service_acc_file_path)
        sto_client = storage.Client(project=config['build_egg_and_upload_to_gcs']['TARGET_PROJECT'],
                                    credentials=credentials)

        if build_config is not None:
            sp.check_call("{} {}/setup.py {}".format(
                sys.executable,
                staging_base,
                build_config
            ),
                shell=True, cwd=staging_base)
        # egg_path = glob.glob(os.path.join('/tmp', repo_folder, 'dist', '*.egg'))[0]
        total_file_lst = []
        for each_path in upload_lst:
            # total_file_lst += glob.glob(os.path.join('/tmp', repo_folder, each_path.lstrip('/')))
            each_path = each_path.replace("'","")
            file_path = os.path.join(staging_base, each_path.lstrip('/'))
            logger.info(f"Appending : {file_path}")
            total_file_lst += glob.glob(file_path)

        bk = sto_client.get_bucket(bucket)
        return_blob_lst = []
        for each_blob in total_file_lst:
            # gcs_blob_path = each_blob.replace('/tmp/{}/'.format(repo_folder), '')
            gcs_blob_path = each_blob.replace(staging_base + '/', '')
            blob = bk.blob('{}/{}'.format(blob_path, gcs_blob_path))
            return_blob_lst.append('{}/{}'.format(gcs_base, gcs_blob_path))
            logger.info(f"Uploading : {each_blob}")
            blob.upload_from_filename(filename=each_blob)
        # return return_blob_lst

        ret_dict = {'blob_lst': return_blob_lst}
        logger.info(ret_dict)
        with open(output_file, "w") as outfile:
            json.dump(ret_dict, outfile, indent=4)

    except BaseException as e:
        job_status = 'FAIL'
        logger.exception(e)

    logger.info(f"status : {job_status}")
    li_rc = 0
    if job_status == 'FAIL':
        li_rc = 1
    return li_rc


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='GitHubHarlem125Operator, Build EGG and Upload File List to GCS')
    parser.add_argument('-P', '--profile',
                        help='Path to INI/Configuration File',
                        required=True)
    parser.add_argument('--build_config',
                        choices=['bdist_egg'],
                        help='Build Configuration',
                        required=True)
    parser.add_argument('--gcs_base',
                        help='Base GCS Location',
                        required=True)
    parser.add_argument('--upload_lst',
                        nargs='+',
                        help='Upload List',
                        required=True)
    parser.add_argument('--local_base',
                        help='Local Base Dir of the code to build',
                        required=True)
    parser.add_argument('--staging_base',
                        help='Staging for code',
                        required=True)
    parser.add_argument('--output_file',
                        help='Output JSON File with Blob List',
                        required=True)

    results = parser.parse_args(args)
    return results


if __name__ == '__main__':
    res = check_arg(sys.argv[1:])
    lc_configFile = res.profile

    logging.config.fileConfig(lc_configFile)

    # Create logger
    logger = logging.getLogger('dpRun')

    logger.info("Using Config from " + str(lc_configFile))

    global config
    config = configparser.ConfigParser()
    config.read(lc_configFile)

    # gcs_base = config['variable']['GCS_Temp_URL'],
    # upload_lst = ['/dist/*.egg']
    # cred = config['google_credentials']['SERVICE_ACCOUNT_FILE_PATH']
    rc = build_egg_and_upload_to_gcs(build_config=res.build_config,
                                     gcs_base=res.gcs_base,
                                     upload_lst=res.upload_lst,
                                     local_base=res.local_base,
                                     staging_base=res.staging_base,
                                     output_file=res.output_file)
    # process('20220724')
    logger.info("Script completed... : " + str(rc))
    sys.exit(rc)
