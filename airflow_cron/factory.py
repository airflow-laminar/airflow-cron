import re
from typing import Any

from airflow_pydantic import BashTask, Dag
from cron_pydantic import CronConfiguration, CronJobConfiguration, CronSchedule, SpecialSchedule

from .config import CronAirflowConfiguration

__all__ = ("create_dags",)

_SPECIAL_SCHEDULES: dict[SpecialSchedule, str] = {
    "@yearly": "@yearly",
    "@annually": "@yearly",
    "@monthly": "@monthly",
    "@weekly": "@weekly",
    "@daily": "@daily",
    "@midnight": "@daily",
    "@hourly": "@hourly",
}
_DAG_ID = re.compile(r"^[A-Za-z0-9_.-]+$")
_UNESCAPED_PERCENT = re.compile(r"(?<!\\)(?:\\\\)*%")


def _airflow_schedule(schedule: CronSchedule | SpecialSchedule) -> str:
    if isinstance(schedule, CronSchedule):
        value = schedule.to_cron()
        if "~" in value:
            raise ValueError("Airflow does not support Cronie random schedule ranges")
        return value
    if schedule == "@reboot":
        raise ValueError("Airflow cannot represent the @reboot schedule")
    return _SPECIAL_SCHEDULES[schedule]


def _create_dag(name: str, job: CronJobConfiguration, cfg: CronAirflowConfiguration) -> Dag:
    if not _DAG_ID.fullmatch(name):
        raise ValueError(f"cron job name is not a valid Airflow DAG ID: {name!r}")
    if _UNESCAPED_PERCENT.search(job.command):
        raise ValueError(f"cron job {name!r} uses unescaped %, whose stdin behavior Airflow cannot represent")

    dag_args: dict[str, Any] = cfg.dag_args.model_dump(exclude_none=True, exclude_unset=True, exclude={"schedule"})
    dag_args.setdefault("catchup", False)

    task_args: dict[str, Any] = cfg.task_args.model_dump(
        exclude_none=True,
        exclude_unset=True,
        exclude={"append_env", "bash_command", "env"},
    )
    environment = {**cfg.environment, **(cfg.task_args.env or {})} or None
    append_environment = cfg.task_args.append_env
    if append_environment is None and environment:
        append_environment = True

    task = BashTask(
        task_id="run",
        bash_command=job.command,
        env=environment,
        append_env=append_environment,
        **task_args,
    )
    return Dag(
        dag_id=name,
        schedule=_airflow_schedule(job.schedule),
        tasks={"run": task},
        **dag_args,
    )


def create_dags(config: CronAirflowConfiguration | CronConfiguration | dict[str, Any]) -> dict[str, Dag]:
    """Convert enabled user-crontab jobs into airflow-pydantic DAG models."""
    if not isinstance(config, CronAirflowConfiguration):
        data = config.model_dump() if isinstance(config, CronConfiguration) else config
        config = CronAirflowConfiguration.model_validate(data)
    if config.system:
        raise ValueError("system crontab users cannot be represented by Airflow tasks")
    unsupported_environment = {"CRON_TZ", "RANDOM_DELAY"}.intersection(config.environment)
    if unsupported_environment:
        names = ", ".join(sorted(unsupported_environment))
        raise ValueError(f"cron scheduler environment is not supported by Airflow: {names}")
    return {name: _create_dag(name, job, config) for name, job in config.job.items() if job.enabled}
