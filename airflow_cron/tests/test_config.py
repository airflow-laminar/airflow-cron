from airflow_config import load_config


class TestConfig:
    def test_load_config(self):
        config = load_config("config", "config")
        assert config is not None
        # assert "cron" in config.extensions
