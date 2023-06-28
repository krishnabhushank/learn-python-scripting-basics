from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.email_operator import EmailOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta
import pendulum

doc_md = """
### Build SPRS Clw_Items GCP BQ table from Mainframe Feed
"""

# Instantiate Pendulum and set your timezone.
local_tz = pendulum.timezone("America/New_York")

default_args = {
    'owner': 'PR-SPRS',
    'depends_on_past': False,
    'start_date': datetime(2022, 11, 29, tzinfo=local_tz),
    'email': ["SHI_PRICING_OPS@searshc.com", "MFT_CORE_TEAM@searshc.com", "aa92ad34.searshc.onmicrosoft.com@amer.teams.ms", ],
    'email_on_failure': True,
    'email_on_success': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='DLY_PR_CTLW_ITEMS_EXPORT_TO_GCS',
    doc_md=doc_md,
    schedule_interval='0 20 * * *',
    default_args=default_args,
    tags=["PR-SPRS", "PR-SPRS.PR-SPRS-Exports"]
)

ctrlm_job_extsensor = ExternalTaskSensor(
    task_id="ctrlm_job_extsensor",
    external_dag_id="DLY_SPRS_SPR7LEVT_Handoff",
    external_task_id="ctrlm_job_sqlsensor",
    allowed_states=['success'],
    failed_states=['failed', 'skipped'],
    execution_delta=timedelta(minutes=0),
    mode='reschedule',
    dag=dag)

extract_data = SSHOperator(
    ssh_conn_id="aws_appmgt",
    task_id='extract_data',
    command="ssh -t hdprc@mdmbatch.prod.mt.oh.transformco.com 'ksh /srv/Projects/hdp_sprs/GEN_SPRS_Export_To_GCS/bin/MasterShell_SXTG.sh PRC_SXTG_00_Extract_Data_CTLW_ITEMS'",
    dag=dag)

load_data = SSHOperator(
    ssh_conn_id="aws_appmgt",
    task_id='load_data',
    command="ssh -t hdprc@mdmbatch.prod.mt.oh.transformco.com 'ksh /srv/Projects/hdp_sprs/GEN_SPRS_Export_To_GCS/bin/MasterShell_SXTG.sh PRC_SXTG_99_Load_Data_CTLW_ITEMS'",
    dag=dag)

create_checkpoint = SSHOperator(
    ssh_conn_id="aws_appmgt",
    task_id='create_checkpoint',
    command="ssh -t hdprc@mdmbatch.prod.mt.oh.transformco.com 'ksh /srv/Projects/hdp_sprs/GEN_SPRS_Create_Checkpoint/bin/MasterShell_CC.sh PRC_CC_99_Checkpoint_CTLW_ITEMS'",
    dag=dag)

email_on_dag_start = EmailOperator(
    mime_charset="utf-8",
    task_id="email_on_dag_start",
    to=["SHI_PRICING_OPS@searshc.com", "MFT_CORE_TEAM@searshc.com", ],
    subject="DAG : Started : DLY_PR_CTLW_ITEMS_EXPORT_TO_GCS",
    html_content="""
              <div style="color:Tomato;font-family: courier;"><br>
              ******************* Airflow Dag Status *******************<br>
              Hello Team,<br>
              Dag Name = DLY_PR_CTLW_ITEMS_EXPORT_TO_GCS<br>
              Dag Status = Started.<br>
              Kindly monitor!!<br>
              *******************
              </div> """,
    dag=dag)

email_on_dag_finish = EmailOperator(
    mime_charset="utf-8",
    task_id="email_on_dag_finish",
    to=["SHI_PRICING_OPS@searshc.com", "MFT_CORE_TEAM@searshc.com", ],
    subject="DAG : Finished : DLY_PR_CTLW_ITEMS_EXPORT_TO_GCS",
    html_content="""
	    <div style="color:MediumSeaGreen;font-family: courier;"><br>
        ******************* Airflow Dag Status *******************<br>
        Hello Team,<br>
        Dag Name = DLY_PR_CTLW_ITEMS_EXPORT_TO_GCS<br>
        Dag Status = Finished.<br>
        Kindly verify!!<br>
        *******************
        <br></div> """,
    dag=dag)

email_on_dag_start >> ctrlm_job_extsensor >> extract_data >> load_data >> create_checkpoint >> email_on_dag_finish
