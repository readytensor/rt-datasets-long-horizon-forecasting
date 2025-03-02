import os
import pandas as pd
from pandas import DataFrame
from typing import List
from sklearn.preprocessing import StandardScaler

import utils
import paths


def save_train_data(
    train_df: DataFrame, dataset_name: str, save_dir: str, compression=""
) -> None:
    """
    Saves the train data to a CSV file.

    Args:
        train_df (DataFrame): The train dataset.
        dataset_name (str): The name of the dataset.
        save_dir (str): The path where the processed datasets are stored.
        compression (str): The compression type to use when saving the CSV file.
                            Options: ["", ".gz", ".zip"]
    """
    train_df.to_csv(
        os.path.join(save_dir, f"{dataset_name}_train.csv{compression}"),
        index=False,
    )


def save_test_no_target_data(
    test_df: DataFrame,
    target_name: str,
    past_covariates: List[str],
    dataset_name: str,
    save_dir: str,
    compression="",
) -> None:
    """
    Saves the test data without the target column to a CSV file.

    Args:
        test_df (DataFrame): The test dataset.
        target_name (str): The name of the target column.
        past_covariates (List[str]): The names of the past covariates.
        dataset_name (str): The name of the dataset.
        save_dir (str): The path where the processed datasets are stored.
        compression (str): The compression type to use when saving the CSV file.
                            Options: ["", ".gz", ".zip"]
    """
    test_no_target_df_no_past_cov = test_df.drop(
        columns=past_covariates + [target_name], axis=1
    )
    test_no_target_df_no_past_cov.to_csv(
        os.path.join(save_dir, f"{dataset_name}_test.csv{compression}"),
        index=False,
    )


def get_past_covariates(schema: dict) -> list:
    """
    Extracts the names of all past covariates from a schema dictionary.

    Args:
        schema (dict): A schema represented as a dictionary.

    Returns:
        list: A list containing the names of all past covariates. Returns
        an empty list if there are no past covariates in the schema.

    """
    # Check if 'pastCovariates' exists in the schema and is a list
    if "pastCovariates" in schema and isinstance(schema["pastCovariates"], list):
        # Extract and return the names of the past covariates
        return [covariate["name"] for covariate in schema["pastCovariates"]]

    # Return an empty list if there are no past covariates
    return []


def save_test_key_data(
    test_df: DataFrame,
    id_name: str,
    time_name: str,
    target_name: str,
    dataset_name: str,
    save_dir: str,
    compression="",
) -> None:
    """
    Saves the test key data to a CSV file.

    Args:
        test_df (DataFrame): The test dataset.
        id_name (str): The name of the ID column.
        time_name (str): The name of the time column.
        target_name (str): The name of the target column.
        dataset_name (str): The name of the dataset.
        save_dir (str): The path where the processed datasets are saved.
        compression (str): The compression type to use when saving the CSV file.
                            Options: ["", ".gz", ".zip"]
    """
    test_key_df = test_df[[id_name, time_name, target_name]]
    test_key_df.to_csv(
        os.path.join(save_dir, f"{dataset_name}_test_key.csv{compression}"),
        index=False,
    )


from sklearn.preprocessing import StandardScaler
import pandas as pd


grouped_datasets = {}

def create_train_test_testkey_files_for_dataset(
        fold_num: int,
        dataset: pd.DataFrame,
        dataset_name: str,
        schema: dict,
        dataset_cfg: pd.Series,
        save_dir: str,
    ) -> None:
    """
    Creates train, test, and test key files for each dataset marked for use in the metadata.
    """

    if dataset_cfg["use_dataset"] == 0:
        return

    forecast_length = schema["forecastLength"]
    dataset_variant_name = (
        dataset_name + f"_fcst_len_{forecast_length}"
        + f"_fold_{fold_num}"
    )
    print("Creating train/test files for dataset:", dataset_variant_name)

    if schema["timeField"]["dataType"] != "INT":
        dataset[schema["timeField"]["name"]] = pd.to_datetime(
            dataset[schema["timeField"]["name"]]
        )

    if dataset_name not in grouped_datasets:
        grouped_datasets[dataset_name] = dataset.groupby(schema["idField"]["name"])

    kfold_roll_window_size = dataset_cfg["kfold_roll_window_size"]
    grouped = grouped_datasets[dataset_name]
    series_len = grouped.size().iloc[0]
    train_end = series_len - (5 - fold_num) * kfold_roll_window_size - forecast_length

    # Extract the target column for scaling
    target_col = schema["forecastTarget"]["name"]

    train_dfs = []
    test_dfs = []
    for _, group in grouped:
        # Split the group into train and test sets
        train_data = group.iloc[:train_end]
        test_data = group.iloc[train_end:train_end+forecast_length]

        # Apply standard scaling to the target column in train data
        scaler = StandardScaler()
        train_target_scaled = scaler.fit_transform(train_data[[target_col]])
        test_target_scaled = scaler.transform(test_data[[target_col]])

        # Replace the original target column with the scaled values
        train_data.loc[:, target_col] = train_target_scaled.round(5)
        test_data.loc[:, target_col] = test_target_scaled.round(5)

        # Append the scaled data to the list
        train_dfs.append(train_data)
        test_dfs.append(test_data)

    # Concatenate all the train and test splits into two DataFrames
    train_df = pd.concat(train_dfs)
    test_df = pd.concat(test_dfs)

    # Save train/test data
    save_train_data(train_df, dataset_variant_name, save_dir, compression="")

    # Save test data without target
    past_covariates = get_past_covariates(schema)
    save_test_no_target_data(
        test_df,
        schema["forecastTarget"]["name"],
        past_covariates,  # these will be dropped from the test data
        dataset_variant_name,
        save_dir,
        compression="",
    )

    # Save test key data
    save_test_key_data(
        test_df,
        schema["idField"]["name"],
        schema["timeField"]["name"],
        schema["forecastTarget"]["name"],
        dataset_variant_name,
        save_dir,
        compression="",
    )


def create_train_test_testkey_files(
    dataset_cfg_path: str, processed_datasets_path: str
) -> None:
    """
    Creates train, test, and test key files for each dataset marked for use in the metadata.
    """

    # Load the metadata
    dataset_metadata = utils.load_metadata(dataset_cfg_path)

    # Iterate through each dataset marked for use in the metadata
    for _, dataset_row in dataset_metadata[
        dataset_metadata["use_dataset"] == 1
    ].iterrows():
        if dataset_row["use_dataset"] == 0:
            continue

        dataset_name = dataset_row["name"]

        if dataset_name.startswith("store_sales"):
            continue

        # Read dataset
        dataset = utils.load_dataset(dataset_name, processed_datasets_path)

        # Read schema
        schema = utils.load_schema(dataset_name, processed_datasets_path)

        if schema["timeField"]["dataType"] != "INT":
            dataset[schema["timeField"]["name"]] = pd.to_datetime(
                dataset[schema["timeField"]["name"]]
            )

        # dataset_train_dfs = []
        # dataset_test_dfs = []

        # dataset_series_list = dataset[schema["idField"]["name"]].unique().tolist()
        forecast_length = schema["forecastLength"]

        grouped = dataset.groupby(schema["idField"]["name"])

        train_dfs = [group.iloc[:-forecast_length] for _, group in grouped]
        test_dfs = [group.iloc[-forecast_length:] for _, group in grouped]

        # Concatenate all the train and test splits into two DataFrames
        train_df = pd.concat(train_dfs)
        test_df = pd.concat(test_dfs)

        # Save train/test data
        save_train_data(train_df, dataset_name, processed_datasets_path)

        # Save test data without target
        past_covariates = get_past_covariates(schema)
        save_test_no_target_data(
            test_df,
            schema["forecastTarget"]["name"],
            past_covariates,  # these will be dropped from the test data
            dataset_name,
            processed_datasets_path,
        )

        # Save test key data
        save_test_key_data(
            test_df,
            schema["idField"]["name"],
            schema["timeField"]["name"],
            schema["forecastTarget"]["name"],
            dataset_name,
            processed_datasets_path,
        )


def run_train_test_testkey_files_gen():
    """Creates train, test, and test key files for each dataset marked for use in the metadata."""
    create_train_test_testkey_files(
        dataset_cfg_path=paths.dataset_cfg_path,
        processed_datasets_path=paths.processed_datasets_path,
    )


if __name__ == "__main__":
    run_train_test_testkey_files_gen()
