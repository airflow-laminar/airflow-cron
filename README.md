# airflow-cron

Generate Airflow DAG models from cron configuration.

[![Build Status](https://github.com/airflow-laminar/airflow-cron/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/airflow-laminar/airflow-cron/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/airflow-laminar/airflow-cron/branch/main/graph/badge.svg)](https://codecov.io/gh/airflow-laminar/airflow-cron)
[![License](https://img.shields.io/github/license/airflow-laminar/airflow-cron)](https://github.com/airflow-laminar/airflow-cron)
[![PyPI](https://img.shields.io/pypi/v/airflow-cron.svg)](https://pypi.python.org/pypi/airflow-cron)

## Overview

`airflow-cron` converts the user-crontab models from `cron-pydantic` into
`airflow-pydantic` DAG and Bash task models. Each enabled cron job becomes one
DAG containing one Bash task.

```python
from airflow_cron import CronAirflowConfiguration, create_dags

configuration = CronAirflowConfiguration.model_validate(
    {
        "environment": {"PATH": "/usr/local/bin:/usr/bin"},
        "job": {
            "backup": {
                "schedule": "0 2 * * *",
                "command": "/opt/bin/backup",
            },
            "cleanup": {
                "schedule": "@weekly",
                "command": "/opt/bin/cleanup",
                "enabled": False,
            },
        },
    }
)

dag_models = create_dags(configuration)
```

The result contains a `backup` DAG scheduled at `0 2 * * *`. Its `run` task
uses the cron command as its Bash command and appends the configured environment
to the worker environment. Disabled jobs are omitted.

To expose generated models from an Airflow DAG file:

```python
for dag_id, model in dag_models.items():
    globals()[dag_id] = model.instantiate()
```

Common Airflow settings can be supplied declaratively:

```yaml
job:
  backup:
    schedule: "0 2 * * *"
    command: /opt/bin/backup
dag_args:
  max_active_runs: 1
  tags: [cron]
task_args:
  execution_timeout: 02:00:00
```

`catchup` defaults to `false`, matching cron's behavior of not backfilling
missed runs. Job schedule and command always take precedence over defaults.

## Compatibility

Airflow cannot faithfully represent every crontab feature. Conversion rejects:

- system crontabs because Airflow executor user selection is deployment-specific
- `@reboot` schedules
- Cronie random ranges using `~`
- `CRON_TZ` and `RANDOM_DELAY` scheduler environment settings
- unescaped `%`, which cron converts into command input

`@annually` maps to `@yearly`, and `@midnight` maps to `@daily`.

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
