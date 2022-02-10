import os

from airflow import DAG
from airflow.utils.dates import days_ago

# To allow us to interact with BigQuery
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator

from datetime import datetime

# Take environmental variables into local variables. These were set in the docker-compose setup.
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "trips_data_all")

default_args = {
    "owner": "airflow",
    "start_date" : days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="live_coded_gcs_to_bq_dag",
    schedule_interval="@monthly",
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=['Homework DAG Week 3'],
) as dag:
    
    gcs_2_gcs_task = GCSToGCSOperator(
        task_id="gcs_2_gcs_task",
        source_bucket=BUCKET,
        source_object='raw/green_tripdata*.parquet',
        destination_bucket=BUCKET,
        destination_object="green/",
        move_object=False
    )
    
    gcs_2_bq_ext_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_green_tripdata_week3",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/green/*"]
            },
        },
    )
    
    CREATE_PART_TBL_QUERY = f"CREATE OR REPLACE TABLE silent-oasis-338916.trips_data_all.external_green_tripdata_partitoned_week3 \
                                PARTITION BY \
                                DATE(lpep_pickup_datetime) AS \
                                SELECT * EXCEPT (ehail_fee) FROM {BIGQUERY_DATASET}.external_green_tripdata_week3;"

    bq_ext_2_part_task = BigQueryInsertJobOperator(
        task_id="bq_ext_2_part_task",
        configuration={
            "query" : {
                "query" : CREATE_PART_TBL_QUERY,
                "useLegacySql" : False,
            }
        }
    )
    
    gcs_2_gcs_task >> gcs_2_bq_ext_task >> bq_ext_2_part_task