# airflow_cron.CronConfiguration

### *pydantic model* airflow_cron.CronConfiguration

Bases: `BaseModel`

Environment and named jobs rendered as one crontab file.

#### *field* job *: dict[str, [CronJobConfiguration](airflow_cron.CronJobConfiguration.md#airflow_cron.CronJobConfiguration)]* *[Required]*

#### *field* environment *: dict[str, str]* *[Optional]*

#### *field* system *: bool* *= False*

#### *field* path *: Path | None* *= None*

#### to_cron() → str

#### write(path: Path | str | None = None) → Path

#### *classmethod* from_cron(contents: str, , system: bool = False, path: Path | None = None) → Self

#### *classmethod* load(path: Path | str) → Self
