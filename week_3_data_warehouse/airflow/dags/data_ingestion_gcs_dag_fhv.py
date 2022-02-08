""" Now create another DAG - for uploading the FHV data.

We will need three steps:

Donwload the data
Parquetize it
Upload to GCS
If you don't have a GCP account, for local ingestion you'll need two steps:

Download the data
Ingest to Postgres
Use the same frequency and the start date as for the yellow taxi dataset

Question: how many DAG runs are green for data in 2019 after finishing everything?

Note: when processing the data for 2020-01 you probably will get an error. 
It's up to you to decide what to do with it - for Week 3 homework we won't need 2020 data. """

import os
import logging

from airflow import DAG

# Our airflow operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Helps us to interact with GCP Storage
from google.cloud import storage

from datetime import datetime

from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

# Helps to convert our data to parquet format
import pyarrow.csv as pv
import pyarrow.parquet as pq

# Take environmental variables into local variables. These were set in the docker-compose setup.
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "trips_data_all")

current_month_year = "{{ execution_date.strftime(\'%Y-%m\') }}"
if "2020" in current_month_year:
    dataset_file = "fhvhv_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv"
else:
    dataset_file = "fhv_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv"

dataset_url_prefix = "https://nyc-tlc.s3.amazonaws.com/trip+data"
dataset_url = dataset_url_prefix + "/" + dataset_file
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
parquet_file = dataset_file.replace('.csv', '.parquet')
output_file_template = path_to_local_home + "/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv"

# BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "trips_data_all")

def format_to_parquet(src_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))

def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


############################################ DAG ################################################

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="data_ingestion_gcs_dag_fhv",
    schedule_interval="@monthly",
    default_args=default_args,
    start_date=datetime(2019, 1, 1),
    catchup=True,
    max_active_runs=3,
    tags=['Homework DAG FHV Week 3'],
) as dag:

    """download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sS {dataset_url} > {path_to_local_home}/{dataset_file}"
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{dataset_file}",
        },
    )"""

    """# TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}",
        },
    )"""

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table_fhv",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{parquet_file}"],
            },
        },
    )

    download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task
