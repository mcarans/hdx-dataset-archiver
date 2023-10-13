import logging

from dateutil.relativedelta import relativedelta
from hdx.data.dataset import Dataset
from hdx.utilities.dateparse import parse_date

logger = logging.getLogger(__name__)


def archive(configuration, today, DatasetCls=Dataset):
    all_datasets = []
    for org_name, fields_to_match in configuration["orgs"].items():
        logger.info(f"Organisation: {org_name}\n")
        for name in fields_to_match:
            if name == "before":
                for field_name, match_value in fields_to_match["before"].items():
                    date = today - relativedelta(**match_value)
                    fields_to_match["before"][field_name] = date

        datasets = DatasetCls.search_in_hdx(fq=f"organization:{org_name}")
        count = 0
        for dataset in datasets:
            match = True
            for field_name, match_value in fields_to_match.items():
                if field_name == "before":
                    for field_name, match_value in fields_to_match["before"].items():
                        field_value = parse_date(dataset[field_name])
                        if field_value >= match_value:
                            match = False
                            break
                    continue
                field_value = dataset[field_name]
                if field_value != match_value:
                    match = False
                    break
            if match:
                name = dataset["name"]
                title = dataset["title"]
                count += 1
                logger.info(
                    f"Archiving dataset: {name} with title: {title} and url: {dataset.get_hdx_url()}"
                )
                dataset["archived"] = True
                dataset.update_in_hdx(
                    operation="patch",
                    batch_mode="KEEP_OLD",
                    skip_validation=True,
                    ignore_check=True,
                )
        logger.info(f"{org_name}: {count} dataset archived!\n")
        all_datasets.extend(datasets)
    return all_datasets
