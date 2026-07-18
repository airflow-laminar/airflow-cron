# Tutorial: generate an Airflow DAG

In this tutorial, we will turn one YAML cron job into an Airflow DAG through
`airflow-config`.

## Install the packages

For Airflow 3, run:

```bash
pip install 'airflow-cron[airflow3]' airflow-config
```

Use the `airflow` extra instead when running Airflow 2.

## Describe the cron job

Create `cron.yaml`:

```yaml
environment:
  PATH: /usr/local/bin:/usr/bin
job:
  backup:
    schedule: "0 2 * * *"
    command: /opt/jobs/backup
dag_args:
  max_active_runs: 1
  tags: [cron]
```

## Register the generated DAG

Create an Airflow DAG file:

```python
from airflow_config import Configuration
from airflow_cron import CronAirflowConfiguration, create_dags

cron = CronAirflowConfiguration.load("cron.yaml")
config = Configuration(
    default_dag_args={"start_date": "2024-01-01"},
    dags=create_dags(cron),
)
config.generate_in_mem()
```

Place both files where the Airflow scheduler can read them, keeping the relative
path from the DAG file to `cron.yaml` unchanged.

## Inspect the result

Parse the DAG folder with Airflow:

```bash
airflow dags list | grep backup
```

The output contains a DAG named `backup`. In the graph view it contains one task
named `run`, scheduled with `0 2 * * *`.

You have now converted cron data into an Airflow-owned schedule without
installing a host crontab.
