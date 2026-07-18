# How-to guides

These guides cover common cron-to-Airflow conversion tasks.

## How to apply common DAG and task settings

Set `dag_args` and `task_args` beside the cron jobs:

```yaml
job:
  report:
    schedule: "30 6 * * mon-fri"
    command: /opt/jobs/report
dag_args:
  catchup: false
  max_active_runs: 1
  tags: [imported-cron]
task_args:
  pool: batch
  execution_timeout: 02:00:00
  env:
    REPORT_FORMAT: json
```

Job schedule and command override the corresponding common fields. Task
environment values override crontab environment values with the same names.

## How to combine generated and hand-written airflow-config DAGs

Load the existing Airflow configuration and merge the generated models before
materializing it:

```python
from airflow_config import Configuration, load_config
from airflow_cron import CronAirflowConfiguration, create_dags

base = load_config("config", "production")
cron = CronAirflowConfiguration.load("cron.yaml")

config = Configuration.model_validate(
    {
        **base.model_dump(),
        "dags": {**(base.dags or {}), **create_dags(cron)},
    }
)
config.generate_in_mem()
```

Use unique cron job names because each name becomes an Airflow DAG ID.

## How to disable a generated DAG

Disable the source job:

```yaml
job:
  retired-report:
    schedule: "@weekly"
    command: /opt/jobs/report
    enabled: false
```

Disabled jobs are omitted from `create_dags()` rather than emitted as paused
DAGs.

## How to handle unsupported cron features

Replace unsupported scheduler semantics before conversion:

- Replace `@annually` with the equivalent generated `@yearly` schedule, or let
  the built-in mapping do it.
- Replace `@midnight` with `@daily`, or let the built-in mapping do it.
- Move `CRON_TZ` behavior into Airflow's DAG timezone configuration.
- Replace Cronie `~` randomization with Airflow-native delay logic.
- Keep `@reboot`, system-user entries, and cron `%` stdin handling in a real
  cron or systemd deployment.

Conversion raises `ValueError` when it would otherwise change these semantics
silently.
