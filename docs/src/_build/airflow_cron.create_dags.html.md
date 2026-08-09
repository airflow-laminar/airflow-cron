# airflow_cron.create_dags

### airflow_cron.create_dags(config: [CronAirflowConfiguration](airflow_cron.CronAirflowConfiguration.html.md#airflow_cron.CronAirflowConfiguration) | [CronConfiguration](airflow_cron.CronConfiguration.html.md#airflow_cron.CronConfiguration) | dict[str, Any]) → dict[str, Dag][[source]](../../../_modules/airflow_cron/factory.html.md#create_dags)

Convert enabled user-crontab jobs into airflow-pydantic DAG models.
