from os.path import join

import pytest
from hdx.api.configuration import Configuration
from hdx.utilities.dateparse import parse_date
from hdx.utilities.useragent import UserAgent

from archive_datasets import archive


class TestDataset:
    @staticmethod
    def search_in_hdx(fq):
        if "unosat" in fq:
            return [{"name": "unosat-test-recent", "title": "unosat test recent", "last_modified": "2023-10-10T00:00:00", "data_update_frequency": "-1", "archived": False}, {"name": "unosat-test-should_archive", "title": "unosat test old", "last_modified": "2023-04-12T00:00:00", "data_update_frequency": "-1", "archived": False}]
        else:
            return [{"name": "wfp-adam-test-recent", "title": "wfp adam test recent", "last_modified": "2023-10-10T00:00:00", "data_update_frequency": "-1", "archived": False}, {"name": "wfp-adam-test-should_archive", "title": "wfp adam test old", "last_modified": "2022-03-02T00:00:00", "data_update_frequency": "-1", "archived": False}]


class TestDatasetArchiver:
    @pytest.fixture(scope="function")
    def configuration(self):
        Configuration._create(
            hdx_read_only=True,
            user_agent="test",
            project_config_yaml=join("config", "project_configuration.yml"),
        )
        UserAgent.set_global("test")
        return Configuration.read()

    def test_archive(self, configuration):
        today = parse_date("2023-10-12")
        datasets = archive(configuration, today, DatasetCls=TestDataset)
        for dataset in datasets:
            name = dataset["name"]
            if dataset["archived"]:
                assert "should_archive" in name
            else:
                assert "recent" in name