from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

# DAG Padre
dag = DAG(
    dag_id='TP2Final',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
    tags=['ingest'],
    params={"example_key": "example_value"},
) as dag:

    comienza_proceso = DummyOperator(
        task_id='comienza_proceso',
        dag=dag,
    )

    finaliza_proceso = DummyOperator(
        task_id='finaliza_proceso',
        dag=dag,
    )

    ingest = BashOperator(
        task_id='ingest',
        bash_command='/usr/bin/sh /home/hadoop/scripts/ingestFinalTP2.sh ',
        dag=dag,
    )

    transform_dag = DAG(
        dag_id='transform',
        default_args=args,
        schedule_interval=None,  
        start_date=days_ago(365),
        dagrun_timeout=timedelta(minutes=60),
        tags=['transform'],
        params={"example_key": "example_value"},
    ) as dag:

        transform = BashOperator(
            task_id='transform',
            bash_command='ssh hadoop@172.17.0.2 /home/hadoop/spark/bin/spark-submit --files /home/hadoop/hive/conf/hive-site.xml /home/hadoop/scripts/sparkFinalTP2.py',
            dag=transform_dag,
        )


comienza_proceso >> ingest >> finaliza_proceso

if __name__ == "__main__":
    dag.cli()
