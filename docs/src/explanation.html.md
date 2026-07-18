# Why cron jobs become DAG models

`airflow-cron` is a translation layer, not a cron installer. A cron job already
contains the essential shape of a simple Airflow workflow: a schedule, a command,
an enabled state, and an environment. The package maps that shape to an
`airflow-pydantic` DAG with one Bash task.

The model boundary keeps Airflow imports out of configuration parsing. Generated
models can be inspected, combined with `airflow-config`, rendered as code, or
instantiated only when an Airflow process loads the DAG file.

## Semantic limits

Cron and Airflow are different schedulers. Cron can select a Unix user in a
system crontab, start work during boot, randomize fields, and split a command at
an unescaped `%`. Airflow delegates users to its executor, has no reboot event,
and sends a Bash command as one command string.

Rejecting those features is deliberate. A conversion tool should not produce a
DAG that looks valid while running at a different time or under a different
security identity.

## Relationship to process supervisors

[airflow-supervisor](https://github.com/airflow-laminar/airflow-supervisor) and
[airflow-systemd](https://github.com/airflow-laminar/airflow-systemd) orchestrate
external process lifecycles and monitor their state. `airflow-cron` instead moves
schedule ownership into Airflow and runs the command as an ordinary task.

Use a supervisor integration when the external service manager must retain
ownership of the process. Use cron conversion when a cron entry is fundamentally
a scheduled batch command that Airflow can own directly.
