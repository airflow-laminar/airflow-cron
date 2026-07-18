# airflow-cron

Generate declarative Airflow DAG models from cron configuration.

[![Build Status](https://github.com/airflow-laminar/airflow-cron/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/airflow-laminar/airflow-cron/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/airflow-laminar/airflow-cron/branch/main/graph/badge.svg)](https://codecov.io/gh/airflow-laminar/airflow-cron)
[![License](https://img.shields.io/github/license/airflow-laminar/airflow-cron)](https://github.com/airflow-laminar/airflow-cron)
[![PyPI](https://img.shields.io/pypi/v/airflow-cron.svg)](https://pypi.python.org/pypi/airflow-cron)

```python
from airflow_cron import CronAirflowConfiguration, create_dags

config = CronAirflowConfiguration.model_validate(
    {
        "job": {
            "backup": {
                "schedule": "0 2 * * *",
                "command": "/opt/jobs/backup",
            }
        }
    }
)

dag_models = create_dags(config)
```

Each enabled user-crontab job becomes one `airflow-pydantic` DAG containing one
Bash task. The result can be instantiated directly or added to an
`airflow-config` configuration.

## Documentation

- [Tutorial: generate an Airflow DAG](docs/src/tutorial.md)
- [How-to guides](docs/src/how-to.md)
- [Why cron jobs become DAG models](docs/src/explanation.md)
- [API reference](docs/src/api.md)

Published documentation is available at
[airflow-laminar.github.io/airflow-cron](https://airflow-laminar.github.io/airflow-cron/).

## Ecosystem

- [cron-pydantic](https://github.com/airflow-laminar/cron-pydantic) provides the source crontab models.
- [supervisor-pydantic](https://github.com/airflow-laminar/supervisor-pydantic) and [systemd-pydantic](https://github.com/airflow-laminar/systemd-pydantic) model process managers.
- [airflow-supervisor](https://github.com/airflow-laminar/airflow-supervisor) and [airflow-systemd](https://github.com/airflow-laminar/airflow-systemd) manage long-running jobs.
- [airflow-pydantic](https://github.com/airflow-laminar/airflow-pydantic) supplies generated DAG and task models.
- [airflow-config](https://github.com/airflow-laminar/airflow-config) applies shared YAML configuration and materializes DAGs.

#### NOTE
This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
