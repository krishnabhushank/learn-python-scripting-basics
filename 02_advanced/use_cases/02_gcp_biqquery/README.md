# Access GCP BigQuery and Unload data into a Local file

This code sample shows
- How to Connect GCP BQ table and get the data into a flat file

`Assumptions` : 
- You have a Service Account created on GCP. 
  - Service Account has the permissions for Accessing GCP BigQuery service
  - Also, the account should have permissions for GCP Cloud Storage Service (GCS)
- You hve the Key for this Service account 

## Commands to run

```shell
source my_bq.venv/bin/activate
PROFILE_PATH=dataProcess.ini python generate_data.py extract.dat
deactivate
```