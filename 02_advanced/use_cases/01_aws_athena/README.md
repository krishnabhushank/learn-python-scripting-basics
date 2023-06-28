# Access AWS Athena using boto3

This code sample shows 
- How to run an Athena Version of HiveQL file on AWS Athena using Python.

`Assumptions` : 
- You will run this python script on AWS EC2.
- The EC2 will have a IAM role. 
  - IAM role has the all the permission to access AWS Athena

## Commands to run

```shell
source athena.venv/bin/activate
# Create S3 based tables on Athena (External)
python process_data_in_athena.py \
      --profile dataProcess.ini \
      --params format=srs,om_db=entpric-om-work,lc_current_time=2023-06-26_07:08:25,lc_current_date=2023-06-26,lc_part_dt=2023-06-25,lc_batch_date=2023-06-25,lc_criticalDate=2023-06-29,lc_releaseDate=2023-07-13 \
      -f hive_create_work_tables/work__hdmkt_ps_pro_082_00_concat_history.sql
# Create S3 based tables on Athena (Apache Iceberg)
python process_data_in_athena.py \
      --profile dataProcess.ini \
      --params format=srs,om_db=entpric-om-work,lc_current_time=2023-06-26_07:08:25,lc_current_date=2023-06-26,lc_part_dt=2023-06-25,lc_batch_date=2023-06-25,lc_criticalDate=2023-06-29,lc_releaseDate=2023-07-13 \
      -f hive_create_work_tables/work__hdmkt_ps_pro_082_01_concat_history_active.sql
# Process Data
python process_data_in_athena.py \
      --profile dataProcess.ini \
      --params format=srs,om_db=entpric-om-work,lc_current_time=2023-06-26_07:08:25,lc_current_date=2023-06-26,lc_part_dt=2023-06-25,lc_batch_date=2023-06-25,lc_criticalDate=2023-06-29,lc_releaseDate=2023-07-13 \
      -f hive_load_work_tables/OM_PS_PRO_082_01_Cleanup_Inputs.sql
deactivate
```