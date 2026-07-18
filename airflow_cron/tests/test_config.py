from pathlib import Path

from airflow_pydantic import BashTaskArgs, DagArgs

from airflow_cron import CronAirflowConfiguration, load_airflow_config


def test_configuration_defaults() -> None:
    configuration = CronAirflowConfiguration(job={})

    assert configuration.dag_args == DagArgs()
    assert configuration.task_args == BashTaskArgs()


def test_configuration_loads_yaml(tmp_path: Path) -> None:
    source = tmp_path / "cron.yaml"
    source.write_text("job:\n  backup:\n    schedule: '@daily'\n    command: backup\n")

    configuration = load_airflow_config(source)

    assert isinstance(configuration, CronAirflowConfiguration)
    assert configuration.job["backup"].command == "backup"


def test_configuration_creates_dags() -> None:
    configuration = CronAirflowConfiguration(job={"backup": {"schedule": "@daily", "command": "backup"}})

    assert list(configuration.create_dags()) == ["backup"]
