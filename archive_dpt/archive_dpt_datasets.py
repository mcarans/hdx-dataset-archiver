import logging

from hdx.data.dataset import Dataset
from hdx.data.hdxobject import HDXError
from hdx.facades.simple import facade
from hdx.utilities.dictandlist import read_list_from_csv

logger = logging.getLogger(__name__)


def main():
    datasets = read_list_from_csv(
        "datasets-to-archive.csv", headers=1, dict_form=True
    )

    for row in datasets:
        dataset_name = row["name"]
        logger.info(f"Reading dataset {dataset_name}")
        try:
            dataset = Dataset.read_from_hdx(dataset_name)
        except HDXError as e:
            logger.error(f"Could not read dataset: {e}")
            continue
        if dataset["archived"]:
            logger.info("Already archived")
            continue
        logger.info("Archiving...")
        try:
            dataset["archived"] = True
            dataset.update_in_hdx(
                update_resources=False,
                operation="patch",
                batch_mode="KEEP_OLD",
                skip_validation=True,
                ignore_check=True,
            )
            logger.info("...done\n")
        except HDXError as e:
            logger.error(f"Unable to archive {dataset_name}: {e}")


if __name__ == "__main__":
    facade(
        main,
        hdx_site="dev",
        user_agent="hdxinternal-archiver",
    )
