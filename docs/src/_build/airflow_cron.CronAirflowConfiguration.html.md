# airflow_cron.CronAirflowConfiguration

### *pydantic model* airflow_cron.CronAirflowConfiguration

Bases: [`CronConfiguration`](airflow_cron.CronConfiguration.md#airflow_cron.CronConfiguration)

Cron configuration plus defaults for generated Airflow DAGs and tasks.

#### *field* dag_args *: DagArgs* *[Optional]*

#### *field* task_args *: BashTaskArgs* *[Optional]*

#### create_dags() → dict[str, Dag]

Create one airflow-pydantic DAG model for each enabled cron job.
