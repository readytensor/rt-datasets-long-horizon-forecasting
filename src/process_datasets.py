import os
import pandas as pd
from pathlib import Path
from datetime import timedelta, datetime
from gluonts.dataset.repository import get_dataset, dataset_names

import paths


def get_electricity_dataset(
    dataset_name: str, save_dir: str = os.path.join(paths.raw_datasets_path)
):
    gluon_ts_dataset_name = "electricity_hourly"
    dataset_path = Path(os.path.join(save_dir, gluon_ts_dataset_name))
    gluonts_dataset = get_dataset(
        gluon_ts_dataset_name, regenerate=False, path=dataset_path
    )
    test_data = pd.DataFrame(gluonts_dataset.test)
    all_ts = []
    for idx, ts in test_data.iterrows():
        start_time = ts["start"]
        values = ts["target"]
        # Create a DataFrame for the current series
        temp_df = pd.DataFrame(
            {
                "series_id": ts["item_id"],
                "ds": pd.date_range(
                    start=start_time.to_timestamp(),
                    periods=len(values),
                    freq=start_time.freq,
                ),
                "y": ts["target"],
            }
        )
        all_ts.append(temp_df)

    all_ts_df = pd.concat(all_ts)
    return all_ts_df


def get_etth_datasets(dataset_name: str, save_dir: str = paths.raw_datasets_path):
    if dataset_name in ["etth1", "etth2"]:
        gluonts_dataset_name = "ett_small_1h"
    elif dataset_name in ["ettm1", "ettm2"]:
        gluonts_dataset_name = "ett_small_15min"
    else:
        raise ValueError(f"Unrecognized variant name for ETT dataset: {dataset_name}")

    dataset_path = Path(os.path.join(save_dir, gluonts_dataset_name))
    gluonts_dataset = get_dataset(
        gluonts_dataset_name, regenerate=False, path=dataset_path
    )
    # print(gluonts_dataset.metadata.json())
    test_data = pd.DataFrame(gluonts_dataset.test)
    if dataset_name in ["etth1", "ettm1"]:
        test_data = test_data.iloc[:7]
    else:
        test_data = test_data.iloc[7:]

    all_ts = []
    for idx, ts in test_data.iterrows():
        start_time = ts["start"]
        values = ts["target"]
        # Create a DataFrame for the current series
        temp_df = pd.DataFrame(
            {
                "series_id": ts["item_id"],
                "ds": pd.date_range(
                    start=start_time.to_timestamp(),
                    periods=len(values),
                    freq=start_time.freq,
                ),
                "y": ts["target"],
            }
        )
        all_ts.append(temp_df)

    all_ts_df = pd.concat(all_ts)
    return all_ts_df


def get_weather_dataset(dataset_name: str, raw_dir: str = paths.raw_datasets_path):
    raw_data_fpath = os.path.join(raw_dir, "weather", "weather.csv")
    weather_df = pd.read_csv(raw_data_fpath, encoding="latin-1", parse_dates=["date"])
    print(weather_df.shape)
    weather_df = weather_df.drop_duplicates()
    print(weather_df.shape)
    exit()
    unpivoted_weather_df = weather_df.melt(
        id_vars=["date"], var_name="series_id", value_name="value"
    )
    return unpivoted_weather_df


def get_traffic_dataset(raw_dir: str = paths.raw_datasets_path):
    raw_data_fpath = os.path.join(
        raw_dir, "traffic", "traffic_hourly_dataset", "traffic_hourly_dataset.tsf"
    )
    with open(raw_data_fpath, "r") as file:
        lines = file.readlines()

    data_started = False
    data = []

    for line in lines:
        line = line.strip()
        if not data_started:
            if line.startswith("@data"):
                data_started = True
            continue

        series_name, rest = line.split(":", 1)
        start_timestamp_str, values_str = rest.split(":", 1)

        start_timestamp = datetime.strptime(start_timestamp_str, "%Y-%m-%d %H-%M-%S")
        values = [float(v) for v in values_str.split(",")]

        for i, value in enumerate(values):
            timestamp = start_timestamp + timedelta(hours=i)
            data.append((series_name, timestamp, value))

    df = pd.DataFrame(data, columns=["series_id", "timestamp", "value"])
    return df


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
    if dataset_name == "electricity":
        return get_electricity_dataset(dataset_name)
    elif dataset_name in ["etth1", "etth2", "ettm1", "ettm2"]:
        return get_etth_datasets(dataset_name)
    elif dataset_name == "weather":
        return get_weather_dataset(dataset_name)
    elif dataset_name == "traffic":
        return get_traffic_dataset()
    else:
        raise ValueError(f"Unrecognized dataset: {dataset_name}")
