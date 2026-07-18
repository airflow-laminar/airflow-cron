# airflow_cron.create_dags

### airflow_cron.create_dags(config: [CronAirflowConfiguration](airflow_cron.CronAirflowConfiguration.md#airflow_cron.CronAirflowConfiguration) | [CronConfiguration](airflow_cron.CronConfiguration.md#airflow_cron.CronConfiguration) | dict[str, Any]) → dict[str, Dag]

Convert enabled user-crontab jobs into airflow-pydantic DAG models.
