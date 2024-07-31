import os
import pandas as pd

import paths
from utils import load_dataset


def preprocess_and_unpivot_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the given dataset and unpivots it from wide to long format.

    The preprocessing steps include:
    1. Renaming the "date" column to "dt".
    2. Converting the "dt" column to datetime format.
    3. Dropping duplicate rows.

    The unpivoting step transforms the dataset such that each row contains a single observation,
    with columns for date ("dt"), series identifier ("series_id"), and the observed value ("value").

    Args:
        dataset (pd.DataFrame): The input dataset to preprocess and unpivot.

    Returns:
        pd.DataFrame: The preprocessed and unpivoted dataset.
    """
    dataset.rename(columns={"date": "dt"}, inplace=True)
    dataset["dt"] = pd.to_datetime(dataset["dt"])
    dataset = dataset.drop_duplicates()
    unpivoted = dataset.melt(id_vars=["dt"], var_name="series_id", value_name="value")
    return unpivoted


def get_electricity_or_traffic_dataset(
        dataset_name: str,
        raw_dir_path: str = os.path.join(paths.raw_datasets_path)
    ):
    """
    Loads, preprocesses, and unpivots the dataset. Also renames certain series for convenience.

    The dataset is first loaded from the specified directory. Then, the columns are renamed
    to have a prefix "ser_" for all columns except "date". The dataset is then preprocessed
    and unpivoted using the `preprocess_and_unpivot_dataset` function.

    Args:
        dataset_name (str): The name of the dataset to load.
        raw_dir_path (str): The path to the directory containing the raw dataset.

    Returns:
        pd.DataFrame: The preprocessed and unpivoted electricity dataset.
    """
    dataset = load_dataset(dataset_name=dataset_name, dir_path=raw_dir_path)
    dataset.columns = [f"ser_{c}" if c != "date" else "date" for c in dataset.columns]
    unpivoted = preprocess_and_unpivot_dataset(dataset)
    return unpivoted


def get_dataset(
        dataset_name: str,
        raw_dir_path: str = os.path.join(paths.raw_datasets_path)
    ):
    """
    Loads, preprocesses, and unpivots a generic dataset.

    The dataset is first loaded from the specified directory. It is then preprocessed
    and unpivoted using the `preprocess_and_unpivot_dataset` function.

    Args:
        dataset_name (str): The name of the dataset to load.
        raw_dir_path (str): The path to the directory containing the raw dataset.

    Returns:
        pd.DataFrame: The preprocessed and unpivoted dataset.
    """
    dataset = load_dataset(dataset_name=dataset_name, dir_path=raw_dir_path)
    unpivoted = preprocess_and_unpivot_dataset(dataset)
    return unpivoted


def save_dataset(main_dataset_df: pd.DataFrame, dataset_name: str, save_dir: str):
    """Save dataset to disk with .gz compression

    Args:
        main_dataset_df (pd.DataFrame): The dataset to save
        dataset_name (str): The name of the dataset
        save_dir (str): Datasets directory to save file.

    """
    print(f"Saving main file for dataset {dataset_name}...")
    os.makedirs(save_dir, exist_ok=True)
    full_fpath = os.path.join(save_dir, f"{dataset_name}.csv.gz")
    if not os.path.exists(full_fpath):
        main_dataset_df.to_csv(full_fpath, index=False)


def get_main_dataset_df(dataset_name):
    """Load, process and return dataset

    Args:
        dataset_name (_type_): Name of dataset to load

    Returns:
        d.DataFrame): Loaded dataframe
    """
    if dataset_name in ["electricity", "traffic"]:
        return get_electricity_or_traffic_dataset(dataset_name)
    else:
        return get_dataset(dataset_name)
