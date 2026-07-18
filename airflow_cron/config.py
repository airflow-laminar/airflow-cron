from airflow_pydantic import BashTaskArgs, Dag, DagArgs
from cron_pydantic import CronConfiguration
from pydantic import Field

__all__ = ("CronAirflowConfiguration", "load_airflow_config")


class CronAirflowConfiguration(CronConfiguration):
    """Cron configuration plus defaults for generated Airflow DAGs and tasks."""

    dag_args: DagArgs = Field(default_factory=DagArgs)
    task_args: BashTaskArgs = Field(default_factory=BashTaskArgs)

    def create_dags(self) -> dict[str, Dag]:
        """Create one airflow-pydantic DAG model for each enabled cron job."""
        from .factory import create_dags

        return create_dags(self)


load_airflow_config = CronAirflowConfiguration.load
