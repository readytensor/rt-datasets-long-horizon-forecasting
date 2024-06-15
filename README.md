# Datasets for Long-Forecasting model category on Ready Tensor

This repo contains files related to the datasets used for benchmarking models under the **Forecasting** category on Ready tensor. There are a total of 6 benchmarking datasets used in this category each dataset has 4 versions for 4 different forecasting horizon values [96,192,336,720].
| Dataset | Dataset Industry | Time Granularity | Series Length | # of Series | # Past Covariates | # Future Covariates | # Static Covariates |
|-------------------------------------------------------|:---------------------------:|:----------------:|:-------------:|:-----------:|:-----------------:|:-------------------:|:-------------------:|
| Electricty | Energy | hourly | 26,304 | 321 | 0 | 0 | 0 |
| ETTh1 | Energy | hourly | 17,420 | 1 | 0 | 6 | 0 |
| ETTh2 | Energy | hourly | 17,420 | 1 | 0 | 6 | 0 |
| ETTm1 | Energy | other | 69680 | 1 | 0 | 6 | 0 |
| ETTm2 | Energy | other | 69680 | 1 | 0 | 6 | 0 |
| weather | Enivironmental Science | other | 5000 | 746 | 0 | 0 | 0 |


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

## Electricity - X

#### Alias (on scoreboards): electricity_forecast_len_X

#### Domain / Industry: Energy

#### Description

The Electricity dataset contains hourly electricity consumption data from 321 different sites. The dataset has a total of 26,304 time points. The dataset does not contain any past or future covariates.

#### Dataset characteristics

- Number of series = 321
- Series length = 26,304
- Forecast length = 96, 192, 336, 720
- Time granularity = Hourly
- Number of past covariates = 0
- Number of future covariates = 0
- Number of static covariates = 0

#### Attribution

The dataset is sourced from the UCI Machine Learning Repository. The dataset is available at the following link: [UCI Machine Learning Repository - Electricity dataset](https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014)

---

## ETTh1 - X

#### Alias (on scoreboards): etth1_forecast_len_X

#### Domain / Industry: Energy

#### Description

The ETTh1 dataset contains hourly electricity consumption data from a single county in China. The dataset has a total of 17,420 time points. The dataset contains 6 future covariates.

#### Dataset characteristics

- Number of series = 1
- Series length = 17,420
- Forecast length = 96, 192, 336, 720
- Time granularity = Hourly
- Number of past covariates = 0
- Number of future covariates = 6
- Number of static covariates = 0

#### Attribution

- [Official Repository](https://github.com/zhouhaoyi/ETDataset)
- [Research Paper](https://arxiv.org/abs/2012.07436)

---

## ETTh2 - X

#### Alias (on scoreboards): etth2_forecast_len_X

#### Domain / Industry: Energy

#### Description

The ETTh2 dataset contains hourly electricity consumption data from another county in China. The dataset has a total of 17,420 time points. The dataset contains 6 future covariates.

#### Dataset characteristics

- Number of series = 1
- Series length = 17,420
- Forecast length = 96, 192, 336, 720
- Time granularity = Hourly
- Number of past covariates = 0
- Number of future covariates = 6
- Number of static covariates = 0

#### Attribution

- [Official Repository](https://github.com/zhouhaoyi/ETDataset)
- [Research Paper](https://arxiv.org/abs/2012.07436)

---

## ETTm1 - X

#### Alias (on scoreboards): ettm1_forecast_len_X

#### Domain / Industry: Energy

#### Description

The ETTm1 dataset contains electricity consumption data from a single county in China. The dataset has a total of 69,680 time points. The dataset contains 6 future covariates.

#### Dataset characteristics

- Number of series = 1
- Series length = 69,680
- Forecast length = 96, 192, 336, 720
- Time granularity = 15 min
- Number of past covariates = 0
- Number of future covariates = 6
- Number of static covariates = 0

#### Attribution

- [Official Repository](https://github.com/zhouhaoyi/ETDataset)
- [Research Paper](https://arxiv.org/abs/2012.07436)

---

## ETTm2 - X

#### Alias (on scoreboards): ettm2_forecast_len_X

#### Domain / Industry: Energy

#### Description

The ETTm2 dataset contains electricity consumption data from another county in China. The dataset has a total of 69,680 time points. The dataset contains 6 future covariates.

#### Dataset characteristics

- Number of series = 1
- Series length = 69,680
- Forecast length = 96, 192, 336, 720
- Time granularity = 15 min
- Number of past covariates = 0
- Number of future covariates = 6
- Number of static covariates = 0

#### Attribution

- [Official Repository](https://github.com/zhouhaoyi/ETDataset)
- [Research Paper](https://arxiv.org/abs/2012.07436)

---

## Weather - X

#### Alias (on scoreboards): weather_forecast_len_X

#### Domain / Industry: Enviromental Science

#### Description

The Weather dataset contains weather data from 746 different weather stations representing maxtemp measured at the weather stations in Australia. The dataset has a total of 5,000 time points by either slicing each series or padding if necessary. The dataset does not contain any past or future covariates.

#### Dataset characteristics

- Number of series = 746
- Series length = 5,000
- Forecast length = 96, 192, 336, 720
- Time granularity = Other
- Number of past covariates = 0
- Number of future covariates = 0
- Number of static covariates = 0

#### Attribution

The dataset is sourced from Monash Time Series Forecasting Repository. The dataset is available at the following link: [Monash Time Series Forecasting Repository - Weather dataset](https://zenodo.org/records/4654822)
