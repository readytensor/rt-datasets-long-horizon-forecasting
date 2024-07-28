import os

from process_datasets import get_main_dataset_df, save_dataset
from generate_schemas import generate_schema
from create_train_test_key_files import create_train_test_testkey_files_for_dataset
from utils import load_metadata, load_features_config, strip_quotes
import paths
from config.config import FORECAST_LENS


def run_all():
    dataset_metadata = load_metadata(paths.dataset_cfg_path)
    features_config = load_features_config(paths.features_cfg_path).apply(strip_quotes)

    for _, dataset_row in dataset_metadata.iterrows():
        if dataset_row["use_dataset"] == 0:
            continue
        dataset_name = dataset_row["name"]
        print("Processing dataset:", dataset_name)

        main_dataset_df = get_main_dataset_df(dataset_name=dataset_name)

        for forecast_len in FORECAST_LENS:
            dataset_name_with_forecast_len = (
                dataset_name + f"_forecast_len_{forecast_len}"
            )
            save_dir = os.path.join(
                paths.processed_datasets_path, dataset_name_with_forecast_len
            )
            save_dataset(
                dataset_name=dataset_name_with_forecast_len,
                main_dataset_df=main_dataset_df,
                save_dir=save_dir,
            )

            schema = generate_schema(
                dataset=main_dataset_df,
                dataset_cfg=dataset_row,
                features_config=features_config,
                forecast_len=forecast_len,
                save_dir=save_dir,
            )

            create_train_test_testkey_files_for_dataset(
                dataset=main_dataset_df,
                dataset_name=dataset_name,
                schema=schema,
                dataset_cfg=dataset_row,
                save_dir=save_dir,
            )


if __name__ == "__main__":
    run_all()
