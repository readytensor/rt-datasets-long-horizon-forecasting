# Datasets for Long-Forecasting model category on Ready Tensor

This repo contains files related to the datasets used for benchmarking models under the **Forecasting** category on Ready tensor. There are a total of 6 benchmarking datasets used in this category each dataset has 4 versions for 4 different forecasting horizon values [96,192,336,720].
| Dataset | Dataset Industry | Time Granularity | Series Length | # of Series | # Past Covariates | # Future Covariates | # Static Covariates |
|-------------------------------------------------------|:---------------------------:|:----------------:|:-------------:|:-----------:|:-----------------:|:-------------------:|:-------------------:|
| Electricity | Energy | hourly | 26,304 | 321 | 0 | 0 | 0 |
| ETTh1 | Energy | hourly | 17,420 | 7 | 0 | 0 | 0 |
| ETTh2 | Energy | hourly | 17,420 | 7 | 0 | 0 | 0 |
| ETTm1 | Energy | 15-minutes | 69,680 | 7 | 0 | 0 | 0 |
| ETTm2 | Energy | 15-minutes | 69,680 | 7 | 0 | 0 | 0 |
| Traffic | Urban Planning | hourly | 17,544 | 862 | 0 | 0 | 0 |
| Weather | Environmental Science | 10-minutes | 52,696 | 21 | 0 | 0 | 0 |

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
- The `raw` folder contains the original data files from the source (see attributions below).
- `src/process_datasets.py`: contains the code to download or read the original raw data from source and convert into the required CSV format (read into a pandas DataFrame). The CSV file is saved in the `datasets/processed/<dataset_name>` folder. This dataset is further divided into train/test splits.
- `src/generate_schemas.py`: contains the code to generate the schema files for each dataset. These are saved in the `datasets/processed/<dataset_name>` folder.
- `src/create_train_test_key_files.py`: contains the code to generate the train, test, and test-key files for each dataset. These are saved in the `datasets/processed/<dataset_name>` folder.
- `src/run_all.py`: This is used to run the above three scripts in sequence.

Below is the description of datasets in this repo. One of the datasets is a "smoke test" dataset that is used for quick testing of models to ensure that they are working as expected. The smoke test dataset is not used for scoring and benchmarking in the Ready Tensor platform.

---

## Electricity - X

#### Alias (on scoreboards): electricity_forecast_len_X

#### Domain / Industry: Energy

#### Description

The `Electricity` dataset represents the electricity consumption of 370 clients recorded in 15-minutes periods in Kilowatt (kW) from 2011 to 2014. This is an aggregated version of the original dataset used by Lai et al. (2017). It contains 321 hourly time series from 2012 to 2014. Four variants of the dataset are available, each with a different forecast horizon: 96, 192, 336, and 720.

#### Dataset characteristics

- Number of series = 321
- Series length = 26,304
- Forecast length = 96, 192, 336, 720
- Time granularity = Hourly
- Number of past covariates = 0
- Number of future covariates = 0
- Number of static covariates = 0

#### Attribution

The dataset is sourced from the UCI Machine Learning Repository. The original dataset is available at the following link: [UCI Machine Learning Repository - Electricity dataset](https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014)

The aggregated dataset is sourced from the GluonTS package. See script `src/process_datasets.py` for more details.

---

## ETTh1 - X

#### Alias (on scoreboards): etth1_forecast_len_X

#### Domain / Industry: Energy

#### Description

The Electricity Transformer Temperature (ETT) dataset is a crucial resource for studying the long-term deployment of electric power infrastructure. It contains data collected over two years from two regions of a province of China. This variant called ETTh1 represents data from one of these regions at an hourly granularity. Each data point includes the target value `oil temperature` and six power load features. For the purpose of univariate time series analysis, the original dataset, which contains a single series with 7 features, has been converted into 7 separate univariate series. This dataset is particularly valuable for analyzing temperature variations and trends on an hourly basis, facilitating the development of models that can predict short-term temperature changes. Make note that another subset, named ETTh2, contains similar data from the second county's transformer. Four variants of the dataset are available, each with a different forecast horizon: 96, 192, 336, and 720.

#### Dataset characteristics

- Number of series = 7
- Series length = 17,420
- Forecast length = 96, 192, 336, 720
- Time granularity = Hourly
- Number of past covariates = 0
- Number of future covariates = 0
- Number of static covariates = 0

#### Attribution

- [Official Repository](https://github.com/zhouhaoyi/ETDataset)
- [Research Paper](https://arxiv.org/abs/2012.07436)

---

## ETTh2 - X

#### Alias (on scoreboards): etth2_forecast_len_X

#### Domain / Industry: Energy

#### Description

The Electricity Transformer Temperature (ETT) dataset is a crucial resource for studying the long-term deployment of electric power infrastructure. It contains data collected over two years from two regions of a province of China. This specific variant, ETTh2, represents data collected over two years from the second of the two regions in China, aggregated at an hourly granularity. Each data point comprises the target value `oil temperature` and six power load features. For the purpose of univariate time series analysis, the original dataset, which contains a single series with 7 features, has been converted into 7 separate univariate series. This dataset is particularly useful for studying temperature variations and trends on an hourly basis, providing insights that are essential for developing models to predict short-term temperature changes. Note that there is another dataset, ETTh1, derived from the same source, covering a different region. Four variants of the dataset are available, each with a different forecast horizon: 96, 192, 336, and 720.

#### Dataset characteristics

- Number of series = 7
- Series length = 17,420
- Forecast length = 96, 192, 336, 720
- Time granularity = Hourly
- Number of past covariates = 0
- Number of future covariates = 0
- Number of static covariates = 0

#### Attribution

- [Official Repository](https://github.com/zhouhaoyi/ETDataset)
- [Research Paper](https://arxiv.org/abs/2012.07436)

---

## ETTm1 - X

#### Alias (on scoreboards): ettm1_forecast_len_X

#### Domain / Industry: Energy

#### Description

The Electricity Transformer Temperature (ETT) dataset is a crucial resource for studying the long-term deployment of electric power infrastructure. It contains data collected over two years from two regions of a province in China. This variant, called ETTm1, represents data from one of these two regions at a 15-minute granularity. Each data point includes the target value `oil temperature` and six power load features. For the purpose of univariate time series analysis, the original dataset, which contains a single series with 7 features, has been converted into 7 separate univariate series. Another subset, named ETTm2, contains similar data from the second region's transformer. Four variants of the dataset are available, each with a different forecast horizon: 96, 192, 336, and 720.

#### Dataset characteristics

- Number of series = 7
- Series length = 69,680
- Forecast length = 96, 192, 336, 720
- Time granularity = 15 minutes
- Number of past covariates = 0
- Number of future covariates = 0
- Number of static covariates = 0

#### Attribution

- [Official Repository](https://github.com/zhouhaoyi/ETDataset)
- [Research Paper](https://arxiv.org/abs/2012.07436)

---

## ETTm2 - X

#### Alias (on scoreboards): ettm2_forecast_len_X

#### Domain / Industry: Energy

#### Description

The Electricity Transformer Temperature (ETT) dataset is a crucial resource for studying the long-term deployment of electric power infrastructure. It contains data collected over two years from two regions of a province in China. This variant, called ETTm2, represents data from the second of these two regions at a 15-minute granularity. Each data point includes the target value `oil temperature` and six power load features. For the purpose of univariate time series analysis, the original dataset, which contains a single series with 7 features, has been converted into 7 separate univariate series. Another subset, named ETTm1, contains similar data from the other region's transformer. Four variants of the dataset are available, each with a different forecast horizon: 96, 192, 336, and 720.

#### Dataset characteristics

- Number of series = 7
- Series length = 69,680
- Forecast length = 96, 192, 336, 720
- Time granularity = 15 minutes
- Number of past covariates = 0
- Number of future covariates = 0
- Number of static covariates = 0

#### Attribution

- [Official Repository](https://github.com/zhouhaoyi/ETDataset)
- [Research Paper](https://arxiv.org/abs/2012.07436)

---

## Traffic - X

#### Alias (on scoreboards): traffic_forecast_len_X

#### Domain / Industry: Urban Planning

#### Description

This dataset contains the San Francisco Traffic dataset used by Lai et al. (2017). It contains 862 hourly time series showing the road occupancy rates on the San Francisco Bay area freeways from 2015 to 2016. Four variants of the dataset are available, each with a different forecast horizon: 96, 192, 336, and 720.

#### Dataset characteristics

- Number of series = 862
- Series length = 17,544
- Forecast length = 96, 192, 336, 720
- Time granularity = hourly
- Number of past covariates = 0
- Number of future covariates = 0
- Number of static covariates = 0

#### Attribution

Dataset can be sourced from here: https://zenodo.org/records/4656132
DOI: 10.5281/zenodo.4656132

---

## Weather - X

#### Alias (on scoreboards): weather_forecast_len_X

#### Domain / Industry: Enviromental Science

#### Description

This is the `Weather` dataset sourced from the Max-Planck-Institut. It contains weather observations recorded every 10 minutes for the 2020 whole year, containing 21 meteorological indicators, such as air temperature, humidity, etc. The original dataset can be downloaded at https://drive.google.com/file/d/1Tc7GeVN7DLEl-RAs-JVwG9yFMf--S8dy/view?usp=share_link. For the purpose of univariate time series analysis, the original dataset, which contains a single series with 21 features, has been converted into 21 separate univariate series. Four variants of the dataset are available, each with a different forecast horizon: 96, 192, 336, and 720.

#### Dataset characteristics

- Number of series = 21
- Series length = 52,696
- Forecast length = 96, 192, 336, 720
- Time granularity = 10-minutes
- Number of past covariates = 0
- Number of future covariates = 0
- Number of static covariates = 0

#### Attribution

Dataset info here: https://paperswithcode.com/dataset/weather-ltsf

Dataset can be downloaded from here:
https://drive.google.com/file/d/1Tc7GeVN7DLEl-RAs-JVwG9yFMf--S8dy/view
