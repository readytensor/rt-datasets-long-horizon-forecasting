import os
import pandas as pd
import json
from typing import Dict, List, Union
from utils import JSONEncoder


def filter_features_for_dataset(
    dataset_name: str, field_type: str, features_config: pd.DataFrame
) -> pd.DataFrame:
    """
    Filters the features configuration for the given dataset and field type.

    Args:
    dataset_name (str): The name of the dataset.
    field_type (str): The type of field to filter for.
    features_config (pd.DataFrame): The features configuration data.

    Returns:
    pd.DataFrame: The filtered features configuration.
    """

    # Filter features related to this dataset
    dataset_df = features_config[features_config["name"] == dataset_name]
    if dataset_df.empty:
        raise ValueError(f"Error: No features for {dataset_name}")
    if field_type == "feature":
        feature_field_types = ["past_covariate", "future_covariate", "static_covariate"]
    else:
        feature_field_types = [field_type]
    filtered_features = dataset_df[dataset_df["field_type"].isin(feature_field_types)]
    return filtered_features


def create_id_section(dataset_name: str, features_config: pd.DataFrame) -> Dict:
    """
    Create the id section of the schema.

    Args:
    dataset_name (str): The name of the dataset.
    features_config (pd.DataFrame): The features configuration data.

    Returns:
    Dict: The id section of the schema.
    """
    # Filter features related to this dataset
    filtered = filter_features_for_dataset(dataset_name, "id", features_config)
    if filtered.empty or filtered.shape[0] > 1:
        raise ValueError(f"Error: No id field or more than id field for {dataset_name}")
    # Create the id section
    field_section = {
        "name": filtered["field_name"].values[0],
        "description": filtered["field_description"].values[0],
    }
    return field_section


def create_target_section(
    dataset_name: str, dataset: pd.DataFrame, features_config: pd.DataFrame
) -> Dict:
    """
    Create the target section of the schema.

    Args:
    dataset_name (str): The name of the dataset.
    dataset (pd.DataFrame): The dataset.
    features_config (pd.DataFrame): The features configuration data.

    Returns:
    Dict: The target section of the schema.
    """

    filtered = filter_features_for_dataset(dataset_name, "target", features_config)
    if filtered.empty or filtered.shape[0] > 1:
        raise ValueError(
            f"Error: No target field or more than target field for {dataset_name}"
        )

    # Create the target section
    target_name = filtered["field_name"].values[0]
    data_type = filtered["data_type"].values[0]
    field_section = {
        "name": target_name,
        "description": filtered["field_description"].values[0],
        "dataType": data_type,
        "example": dataset[target_name].dropna().iloc[0],
    }
    return field_section


def create_time_section(
    dataset_name: str, dataset: pd.DataFrame, features_config: pd.DataFrame
) -> Union[None, Dict]:
    """
    Create the time section of the schema.

    Args:
    dataset_name (str): The name of the dataset.
    dataset (pd.DataFrame): The dataset.
    features_config (pd.DataFrame): The features configuration data.

    Returns:
    Union[None, Dict]: The time section of the schema.
    """

    filtered = filter_features_for_dataset(dataset_name, "time", features_config)
    # If no time field in the dataset, return None
    if filtered.empty:
        return None

    if filtered.shape[0] > 1:
        raise ValueError(f"Error: More than one time field for {dataset_name}")

    # Create the target section
    time_field_name = filtered["field_name"].values[0]
    data_type = filtered["data_type"].values[0]
    field_section = {
        "name": time_field_name,
        "description": filtered["field_description"].values[0],
        "dataType": data_type,
        "example": dataset[time_field_name].dropna().iloc[0],
    }
    return field_section


def create_feature_section(
    dataset_name: str,
    dataset_row: pd.Series,
    dataset: pd.DataFrame,
    features_config: pd.DataFrame,
) -> List[Dict]:
    """
    Create the feature section of the schema.

    Args:
    dataset_name (str): The name of the dataset.
    dataset_row (pd.Series): The metadata for the dataset.
    dataset (pd.DataFrame): The dataset.
    features_config (pd.DataFrame): The features configuration data.

    Returns:
    List[Dict]: The features section of the schema.
    """
    features_config = features_config[features_config["name"] == dataset_row["name"]]
    # Filter features related to this dataset
    filtered = filter_features_for_dataset(dataset_name, "feature", features_config)
    # create the features section
    past_covariates = []
    future_covariates = []
    static_covariates = []
    if filtered.empty:
        # no exogenous covariates
        return past_covariates, future_covariates, static_covariates
    for _, feature_row in filtered.iterrows():
        feature = {
            "name": feature_row["field_name"],
            "description": feature_row["field_description"],
            "dataType": feature_row["data_type"].upper(),
            "example": dataset[feature_row["field_name"]].dropna().iloc[0],
        }
        if feature_row["field_type"] == "past_covariate":
            past_covariates.append(feature)
        elif feature_row["field_type"] == "future_covariate":
            future_covariates.append(feature)
        elif feature_row["field_type"] == "static_covariate":
            static_covariates.append(feature)
        else:
            raise ValueError(f"Error: Unknown feature type for {dataset_name}")
    return past_covariates, future_covariates, static_covariates


def generate_schema(
    dataset: pd.DataFrame,
    dataset_cfg: pd.Series,
    features_config: pd.DataFrame,
    forecast_len: int,
    save_dir: str,
):
    """
    Generate the schema for each dataset.

    Args:
        dataset (pd.DataFrame): The dataset.
        dataset_cfg (pd.DataFrame): The metadata for all the datasets.
        features_config (pd.DataFrame): The features configuration data.
        forecast_len (int): The forecast length.
        save_dir (str): The path where the processed datasets are saved.
    """

    if dataset_cfg["use_dataset"] == 0:
        return

    desc_suffix = f" In this specific variation, the test set is designed to use a forecast length of {forecast_len} time steps."

    dataset_name = dataset_cfg["name"].strip()
    dataset_name_with_forecast_len = dataset_name + f"_forecast_len_{forecast_len}"
    print("Creating schema for dataset", dataset_name_with_forecast_len)
    schema = {}
    schema["title"] = dataset_cfg["title"] + f" Forecast Length {forecast_len}"
    schema["description"] = dataset_cfg["description"] + desc_suffix
    schema["modelCategory"] = dataset_cfg["model_category"]
    schema["schemaVersion"] = 1.0
    schema["inputDataFormat"] = "CSV"
    schema["encoding"] = dataset_cfg["encoding"]
    schema["frequency"] = dataset_cfg["frequency"]
    schema["forecastLength"] = forecast_len

    schema["idField"] = create_id_section(dataset_name, features_config)

    time_section = create_time_section(dataset_name, dataset, features_config)

    if time_section is not None:
        schema["timeField"] = time_section

    schema["forecastTarget"] = create_target_section(
        dataset_name, dataset, features_config
    )

    past_covariates, future_covariates, static_covariates = create_feature_section(
        dataset_name, dataset_cfg, dataset, features_config
    )

    schema["pastCovariates"] = past_covariates
    schema["futureCovariates"] = future_covariates
    schema["staticCovariates"] = static_covariates

    # Write the schemas in JSON format to disk
    os.makedirs(save_dir, exist_ok=True)
    output_fpath = os.path.join(
        save_dir, f"{dataset_name_with_forecast_len}_schema.json"
    )
    with open(output_fpath, "w", encoding="utf-8") as file_:
        json.dump(schema, file_, cls=JSONEncoder, indent=2)

    return schema


# def run_schema_gen():
#     """Generate the schema for each dataset."""
#     dataset_metadata = load_metadata(dataset_cfg_path=paths.dataset_cfg_path)
#     features_config = load_features_config(
#         features_cfg_path=paths.features_cfg_path)\
#             .apply(strip_quotes)

#     generate_schemas(
#         dataset_metadata=dataset_metadata,
#         processed_datasets_path=paths.processed_datasets_path,
#         features_config=features_config
#     )


# if __name__ == "__main__":
#     run_schema_gen()
