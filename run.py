from os.path import join, expanduser

from hdx.api.configuration import Configuration
from hdx.facades.simple import facade
from hdx.utilities.dateparse import now_utc

from archive_datasets import archive


def main():
    archive(Configuration.read(), now_utc())


if __name__ == "__main__":
    facade(
        main,
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yml"),
        user_agent_lookup="hdx-dataset-archiver",
        project_config_yaml=join("config", "project_configuration.yml"),
    )
