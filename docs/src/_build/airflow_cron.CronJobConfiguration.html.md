# airflow_cron.CronJobConfiguration

### *pydantic model* airflow_cron.CronJobConfiguration[[source]](../../../_modules/cron_pydantic/models.html.md#CronJobConfiguration)

Bases: `BaseModel`

Command and schedule for one crontab entry.

#### *field* schedule *: [CronSchedule](airflow_cron.CronSchedule.html.md#airflow_cron.CronSchedule) | SpecialSchedule* *[Required]*

#### *field* command *: Command* *[Required]*

#### *field* user *: str | None* *= None*

#### *field* enabled *: bool* *= True*

#### to_cron(system: bool = False) → str[[source]](../../../_modules/cron_pydantic/models.html.md#CronJobConfiguration.to_cron)
