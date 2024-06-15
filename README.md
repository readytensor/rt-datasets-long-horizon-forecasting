# Datasets for Long-Forecasting model category on Ready Tensor

This repo contains files related to the datasets used for benchmarking models under the **Forecasting** category on Ready tensor. There are a total of 24 benchmarking datasets used in this category. Additionally, there is a 25th dataset for smoke testing of models. The list of datasets is as follows:
| Dataset | Dataset Industry | Time Granularity | Series Length | # of Series | # Past Covariates | # Future Covariates | # Static Covariates |
|-------------------------------------------------------|:---------------------------:|:----------------:|:-------------:|:-----------:|:-----------------:|:-------------------:|:-------------------:|


More information about each dataset is provided in the sections below.

---

## Repository Structure

The `datasets` folder contains the main data files and the schema files for all the benchmark datasets.

- `processed` folder contains the processed files. These files are used in the Ready Tensor platform for model benchmarking.
  - The CSV file with suffix `_train.csv` is used for training. This file excludes the forecast horizon. The forecast horizon is the time period for which the model is expected to generate forecasts. This file contains columns for the series id, time, and the target value. It may also contain columns for past and future covariates.
  - The CSV file with suffix `_test.csv` is used for input to the forecast step. It represents the forecast horizon for which the model is expected to generate forecasts. This file contains columns for the series id, and time. It may also contain columns for future covariates. The target value is not included in this file.
  - `_test_key.csv` contains the data for the forecast horizon. This test key file is used to generate scores by comparing with forecasts. This file contains columns for the series id, time, and the target value.
  - The JSON file with suffix `_schema.json` is the schema file for the corresponding dataset.
  - The CSV file with the dataset name, and no other suffix, is the full data made of both training data, and data from the forecast horizon.
  - In case of some datasets, `.png` files are also included to visualize the data.
- The folder `config` contains two csv files - one called `forecasting_datasets.csv` which contains the dataset level attribute information. The second csv called `forecasting_datasets_fields.csv` contains information regarding all the fields in each of the datasets.
- The `raw` folder contains the original data files from the source (see attributions below). The Jupyter notebook file within each dataset folder is used to convert the raw data file for each dataset into the processed form in `processed` folder.
- `generate_schemas.py`: contains the code to generate the schema files for each dataset. These are saved in the `datasets/processed` folder.
- `create_train_test_key_files.py`: contains the code to generate the train, test, and test-key files for each dataset. These are saved in the `datasets/processed` folder.
- `run_all.py`: This is used to run the above two scripts in sequence.

Below is the description of datasets in this repo. One of the datasets is a "smoke test" dataset that is used for quick testing of models to ensure that they are working as expected. The smoke test dataset is not used for scoring and benchmarking in the Ready Tensor platform.

---



