from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

pytest.importorskip("airflow")

from airflow.exceptions import AirflowException, AirflowSkipException

from airflow_cron import CronAirflowConfiguration


def alert(context):
    return context


@pytest.mark.parametrize(("code", "error"), [(0, None), (7, AirflowException), (99, AirflowSkipException)])
def test_generated_task_forwards_output_and_exit_status(code, error):
    cfg = CronAirflowConfiguration.model_validate(
        {
            "job": {"probe": {"schedule": "@daily", "command": f"printf 'cron stdout\\n'; printf 'cron stderr\\n' >&2; exit {code}"}},
            "dag_args": {"start_date": datetime(2025, 1, 1, tzinfo=UTC)},
            "task_args": {"on_failure_callback": alert},
        }
    )
    dag = cfg.create_dags()["probe"].instantiate()
    task = dag.get_task("run")
    log = Mock()
    task.subprocess_hook._log = log
    if error is None:
        assert task.execute({"dag": dag, "task": task}) == "cron stderr"
    else:
        with pytest.raises(error):
            task.execute({"dag": dag, "task": task})
    assert "cron stdout" in str(log.info.call_args_list)
    assert "cron stderr" in str(log.info.call_args_list)
    assert task.on_failure_callback in (alert, [alert])


def test_explicit_none_disables_skip_exit_code():
    cfg = CronAirflowConfiguration.model_validate(
        {
            "job": {"probe": {"schedule": "@daily", "command": "exit 99"}},
            "dag_args": {"start_date": datetime(2025, 1, 1, tzinfo=UTC)},
            "task_args": {"skip_on_exit_code": None},
        }
    )
    dag = cfg.create_dags()["probe"].instantiate()
    task = dag.get_task("run")
    with pytest.raises(AirflowException, match="99"):
        task.execute({"dag": dag, "task": task})
