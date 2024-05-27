from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='clase8bis',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
    tags=['ingest_clase8bis', 'transform_clase8'],
    params={"example_key": "example_value"},
) as dag:


    comienza_proceso = DummyOperator(
        task_id='comienza_proceso',
    )

    finaliza_proceso = DummyOperator(
        task_id='finaliza_proceso',
    )
    
    clean = BashOperator(
        task_id="clean", bash_command='/usr/bin/sh /home/hadoop/scripts/clase8bis/ingest_clean.sh ',
    )

    # Ingest Taskgroup
    with TaskGroup("ingest", tooltip="Tasks for ingest") as ingest:
        task_1 = BashOperator(task_id="ingest_constructor", bash_command='/usr/bin/sh /home/hadoop/scripts/clase8bis/ingest_constructor.sh ',)
        task_2 = BashOperator(task_id="ingest_driver", bash_command='/usr/bin/sh /home/hadoop/scripts/clase8bis/ingest_driver.sh ',)
        task_3 = BashOperator(task_id="ingest_races", bash_command='/usr/bin/sh /home/hadoop/scripts/clase8bis/ingest_races.sh ',)
        task_4 = BashOperator(task_id="ingest_result", bash_command='/usr/bin/sh /home/hadoop/scripts/clase8bis/ingest_result.sh ',)
        
        [task_1, task_2, task_3, task_4]
        
    # Transform Taskgroup
    with TaskGroup("transform", tooltip="Tasks for transform") as transform:
        task_1 = BashOperator(task_id="spark_driveer_results", bash_command='ssh hadoop@172.17.0.2 /home/hadoop/spark/bin/spark-submit --files /home/hadoop/hive/conf/hive-site.xml /home/hadoop/scripts/clase8bis/spark_driveer_results.py')
        task_2 = BashOperator(task_id="spark_constructor_results", bash_command='ssh hadoop@172.17.0.2 /home/hadoop/spark/bin/spark-submit --files /home/hadoop/hive/conf/hive-site.xml /home/hadoop/scripts/clase8bis/spark_constructor_results.py')

        task_1 >> task_2

    comienza_proceso >> clean >> ingest >> transform >> finaliza_proceso

if __name__ == "__main__":
    dag.cli()
