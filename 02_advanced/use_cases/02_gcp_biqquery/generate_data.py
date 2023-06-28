import configparser
import logging.config
import os
import sys

from google.cloud import storage, bigquery
from google.oauth2 import service_account


def delete_blobs(credentials, project, gcs_bucket, gcs_path):
    storage_client = storage.Client(credentials=credentials, project=project)
    blobs = storage_client.list_blobs(gcs_bucket, prefix=gcs_path)

    logger.info("Blobs to Delete:")
    for blob in blobs:
        logger.info(blob.name)
        blob.delete()


def export_qry_to_sto(credentials, query, project, gcs_bucket, gcs_path):
    client = bigquery.Client(credentials=credentials, project=project)
    bq_export_to_gs = f'''
EXPORT DATA OPTIONS(
  uri='gs://{gcs_bucket}/{gcs_path}/*',
  format='CSV',
  overwrite=true,
  header=false,
  field_delimiter='|') AS
{query}
    '''
    query_job = client.query(bq_export_to_gs)
    results = query_job.result()
    for row in results:
        logger.info(row)


def copy_sto_to_local(credentials, project, gcs_bucket, gcs_path, lcl_file_path): 
    # Truncate file
    f = open(lcl_file_path, "w+")
    f.close()

    storage_client = storage.Client(credentials=credentials, project=project)
    blobs = storage_client.list_blobs(gcs_bucket, prefix=gcs_path)

    logger.info("Blobs:")
    for blob in blobs:
        logger.info(blob.name)
        rule_data = blob.download_as_string()
        f = open(lcl_file_path, "a", encoding='utf-8')
        f.write(rule_data.decode('utf-8'))
        f.close

 
def generate_data(export_file_path) -> int:
    project = config['table_credentials']['SOURCE_PROJECT']
    service_acc_file_path = config['google_credentials']['SERVICE_ACCOUNT_FILE_PATH']
    export_gcs_bucket = config['extract']['GCS_BUCKET']
    export_gcs_path = config['extract']['GCS_PATH']
    logger.info(f"export_gcs_loc: gs://{export_gcs_bucket}/{export_gcs_path}/")
    
    credentials = service_account.Credentials.from_service_account_file(service_acc_file_path)
    job_status = 'SUCCESS'

    query_str = f'''
select lpad(cast(k.ksn_id as string),9,'0') as ksn_id,
       rpad(k.description,40,' ') as description,
       rpad(ifnull(cbs.srs_div_no,''),3,' ') as srs_div_no,
       rpad(ifnull(cbs.srs_itm_no,''),5,' ') as srs_itm_no,
       rpad(ifnull(cbs.srs_sku_no,''),5,' ') as srs_sku_no,
       rpad(ifnull(oi.Item_Type_Cd,''),4,' ') as item_type_cd,
       lpad(cast(hi.bus_nbr as string),10,'0') as bus_nbr,
       lpad(cast(hi.dvsn_nbr as string),10,'0') as dvsn_nbr,
       lpad(cast(hi.dept_nbr as string),10,'0') as dept_nbr,
       lpad(cast(hi.catg_nbr as string),10,'0') as catg_nbr,
       lpad(cast(hi.sub_catg_nbr as string),10,'0') as sub_catg_nbr,
       rpad(ifnull(sk_xref.srs_bus_nbr,''),3,' ') as srs_bus_nbr,
       rpad(ifnull(sk_xref.srs_ln_no,''),2,' ') as srs_ln_no,
       rpad(ifnull(sk_xref.srs_sbl_no,''),2,' ') as srs_sbl_no,
       rpad(ifnull(sk_xref.srs_cls_no,''),3,' ') as srs_cls_no
  from (
select ksn_id,
       Description,
       Item_Id
  from `shc-ent-data-library-prod.PreIntegration_Views.IMA_Ksn` 
 where date(Expir_Ts) >= current_date
       ) as k
  left join
       (
select ksn_id,
       srs_div_no,
       srs_itm_no,
       srs_sku_no
  from `shc-ent-data-library-prod.PreIntegration_Views.IMA_Core_Bridge_Sku`
 where date(Expir_Ts) >= current_date
       ) as cbs
    on (cbs.ksn_id = k.ksn_id)
 left join
       (
select Item_Id,
       Bus_Unit_Nbr as bus_nbr,
       rpt_Div_Nbr as dvsn_nbr,
       rpt_dept_nbr as dept_nbr,
       rpt_catg_nbr as catg_nbr,
       sub_catg_nbr
  from `shc-ent-data-library-prod.PreIntegration_Views.IMA_Hier_Item`
 where date(Hier_Item_Exp_Dt) >= current_date
       ) as hi
    on ( k.Item_Id = hi.item_id )
  left join
       (
select item_id,
       Item_Type_Cd          
  from `shc-ent-data-library-prod.PreIntegration_Views.IMA_Oi_Item`
 where date(Expir_Ts) >= current_date
       ) as oi
    on ( k.item_id = oi.item_id )
  left join 
       (
select Srs_Bus_Nbr,
       Srs_Ln_No,
       Srs_Sbl_No,
       Srs_Cls_No,
       Kmt_Dvsn_Nbr,
       Kmt_Dept_Nbr,
       Kmt_Catg_Nbr,
       Kmt_Sub_Catg_Nbr
  from `shc-ent-data-library-prod.PreIntegration_Views.IMA_Srs_Kmart_Xref`
       ) as sk_xref
    on (hi.dvsn_nbr = sk_xref.Kmt_Dvsn_Nbr and
        hi.dept_nbr = sk_xref.Kmt_Dept_Nbr and
        hi.catg_nbr = sk_xref.Kmt_Catg_Nbr and
        hi.sub_catg_nbr = sk_xref.Kmt_Sub_Catg_Nbr)
    '''
    logger.info(f"Query: {query_str}")

    try:
        logger.info('Cleaning up GCS Loc')
        try:
            delete_blobs(credentials=credentials,
                         project=project,
                         gcs_bucket=export_gcs_bucket,
                         gcs_path=export_gcs_path)
            logger.info('Cleaned up GCS Loc successfully...')
        except BaseException as e:
            raise ImportError(f"Something went wrong while Cleaning data from GCS Loc. Error: {e}")

        logger.info('Extracting data to GCS Loc')
        try:
            export_qry_to_sto(credentials=credentials,
                              query=query_str,
                              project=project,
                              gcs_bucket=export_gcs_bucket,
                              gcs_path=export_gcs_path)
            logger.info('Extracted data successfully...')
        except BaseException as e:
            raise ImportError(f"Something went wrong while fetching data from BQ table. Error: {e}")

        logger.info('Copying data from GCS Loc to Local')
        try:
            copy_sto_to_local(credentials=credentials,
                              project=project,
                              gcs_bucket=export_gcs_bucket,
                              gcs_path=export_gcs_path,
                              lcl_file_path=export_file_path)
            logger.info('Copied Data to local successfully...')
        except BaseException as e:
            raise ImportError(f"Something went wrong while Extracting data from GCS Loc. Error: {e}")

    except BaseException as e:
        job_status = 'FAIL'
        logger.exception(e)
        raise e
    finally:
        li_rc = 0
        if job_status == 'FAIL':
            li_rc = 1
        return li_rc


if __name__ == '__main__':
    arguments = sys.argv
    # PROFILE_PATH = <full_path>/GEN_IMA_Hierarchy/config.samples/dataProcess.dev.ini
    lc_configFile = os.environ.get('PROFILE_PATH')

    logging.config.fileConfig(lc_configFile)

    # Create logger
    logger = logging.getLogger('generateData')

    logger.info("Using Config from " + str(lc_configFile))

    global config
    config = configparser.ConfigParser()
    config.read(lc_configFile)

    rc = generate_data(export_file_path=arguments[1])
    # process('20220724')
    logger.info("Script completed... : " + str(rc))
    sys.exit(rc)
