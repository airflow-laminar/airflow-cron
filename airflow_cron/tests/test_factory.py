from datetime import timedelta

import pytest

from airflow_cron import CronAirflowConfiguration, CronConfiguration, create_dags


def test_create_dags() -> None:
    configuration = CronAirflowConfiguration.model_validate(
        {
            "environment": {"PATH": "/opt/bin"},
            "job": {
                "backup": {"schedule": "0 2 * * *", "command": "backup"},
                "disabled": {"schedule": "@daily", "command": "disabled", "enabled": False},
            },
        }
    )

    dags = create_dags(configuration)

    assert list(dags) == ["backup"]
    dag = dags["backup"]
    assert dag.schedule == "0 2 * * *"
    assert dag.catchup is False
    assert dag.tasks is not None
    assert list(dag.tasks) == ["run"]
    task = dag.tasks["run"]
    assert task.bash_command == "backup"
    assert task.env == {"PATH": "/opt/bin"}
    assert task.append_env is True


def test_create_dags_applies_airflow_defaults() -> None:
    configuration = CronAirflowConfiguration.model_validate(
        {
            "job": {"report": {"schedule": "@weekly", "command": "report"}},
            "dag_args": {"catchup": True, "max_active_runs": 1, "tags": ["imported"]},
            "task_args": {
                "env": {"REPORT_FORMAT": "json"},
                "append_env": False,
                "execution_timeout": timedelta(hours=2),
            },
        }
    )

    dag = create_dags(configuration)["report"]
    assert dag.tasks is not None
    task = dag.tasks["run"]

    assert dag.catchup is True
    assert dag.max_active_runs == 1
    assert dag.tags == ["imported"]
    assert task.env == {"REPORT_FORMAT": "json"}
    assert task.append_env is False
    assert task.execution_timeout == timedelta(hours=2)


def test_create_dags_accepts_dict_and_base_configuration() -> None:
    data = {"job": {"first": {"schedule": "@hourly", "command": "first"}}}

    assert create_dags(data)["first"].schedule == "@hourly"
    assert create_dags(CronConfiguration.model_validate(data))["first"].schedule == "@hourly"


@pytest.mark.parametrize(
    ("schedule", "expected"),
    [
        ("@yearly", "@yearly"),
        ("@annually", "@yearly"),
        ("@monthly", "@monthly"),
        ("@weekly", "@weekly"),
        ("@daily", "@daily"),
        ("@midnight", "@daily"),
        ("@hourly", "@hourly"),
    ],
)
def test_create_dags_maps_special_schedules(schedule: str, expected: str) -> None:
    dag = create_dags({"job": {"job": {"schedule": schedule, "command": "run"}}})["job"]

    assert dag.schedule == expected


@pytest.mark.parametrize(
    ("configuration", "message"),
    [
        ({"system": True, "job": {"job": {"schedule": "@daily", "command": "run", "user": "root"}}}, "system crontab"),
        ({"job": {"job": {"schedule": "@reboot", "command": "run"}}}, "@reboot"),
        ({"job": {"job": {"schedule": "1~5 * * * *", "command": "run"}}}, "random schedule"),
        ({"job": {"invalid name": {"schedule": "@daily", "command": "run"}}}, "valid Airflow DAG ID"),
        ({"job": {"job": {"schedule": "@daily", "command": "date +%F"}}}, "unescaped %"),
        ({"environment": {"CRON_TZ": "UTC"}, "job": {}}, "CRON_TZ"),
        ({"environment": {"RANDOM_DELAY": "5"}, "job": {}}, "RANDOM_DELAY"),
    ],
)
def test_create_dags_rejects_unsupported_cron_semantics(configuration: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        create_dags(configuration)


def test_create_dags_accepts_escaped_percent() -> None:
    dag = create_dags({"job": {"job": {"schedule": "@daily", "command": r"date +\%F"}}})["job"]

    assert dag.tasks is not None
    assert dag.tasks["run"].bash_command == r"date +\%F"
