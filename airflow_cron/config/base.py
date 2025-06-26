from airflow_pydantic import Dag
from pydantic import BaseModel

__all__ = ("CronConfiguration", "CronDAG")

# _log = getLogger(__name__)


class CronConfiguration(BaseModel): ...


class CronDAG(Dag): ...
