from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='TP2FinalPadre',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
    tags=['ingest', 'transform'],
    params={"example_key": "example_value"},
) as dag:

    comienza_proceso = DummyOperator(
        task_id='comienza_proceso',
    )

    finaliza_proceso = DummyOperator(
        task_id='finaliza_proceso',
    )

    ingest = BashOperator(
        task_id='ingest',
        bash_command='/usr/bin/sh /home/hadoop/scripts/ingestFinalTP2.sh ',
    )

    transform = TriggerDagRunOperator(
        task_id='trigger_target',
        trigger_dag_id='TP2FinalHijo', 
        execution_date='{{ ds }}',
        reset_dag_run=True,
        wait_for_completion=True,
        poke_interval=30
    )

    comienza_proceso >> ingest >> transform >> finaliza_proceso

if __name__ == "__main__":
    dag.cli()
