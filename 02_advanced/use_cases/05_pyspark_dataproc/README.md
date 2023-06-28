# Access GCP DataProc service using Python and Run PySpark code

This module has code for following using Python:
- Building `Egg` for existing PySpark Code and Uploading same to GCS
- Creating Cluster on GCP Dataproc
- Deleting a Cluster from GCP Dataproc
- Running a PySpark job on GCP Dataproc

## Commands to run

```shell
# Build Egg distributable file for Python code
python process/build_egg_and_upload_to_gcs.py \
       --profile dataProcess.ini \
       --build_config bdist_egg \
       --gcs_base gs://temp_bucket \
       --upload_lst '/dist/*.egg' \
       --local_base <pyspark_local_dir> \
       --staging_base <staging_dir> \
       --output_file run_sears_harlem125_blobs.json

# Create the Spark Cluster on GCP DataProc
python process/create_dataproc_spark_cluster.py \
       --profile dataProcess.ini

# Run PySpark job on the Spark Cluster
python process/run_job_on_spark_cluster.py \
       --profile dataProcess.ini \
       --run_datetime_json_file run_sears_datetime.json \
       --harlem125_uploaded_blobs_json_file run_sears_harlem125_blobs.json \
       --sears_online_rule_uploaded_blobs_json_file run_sears_online_rule_blobs.json

# Delete the Spark Cluster from GCP DataProc
python process/delete_dataproc_spark_cluster.py \
       --profile dataProcess.ini
```