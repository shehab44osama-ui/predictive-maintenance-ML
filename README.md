# Predictive Maintenance ML

Machine Learning project for predicting whether an industrial machine will fail within the next 24 hours.

## Project Overview

This project uses machine learning and sensor data to identify machines that are at risk of failure. The goal is to support predictive maintenance by detecting potential failures early and helping maintenance teams take preventive action.

The project includes:
- Data preprocessing and feature engineering
- Multiple machine learning models
- Model evaluation using classification metrics
- A professional Streamlit web application
- Real-time machine failure prediction
- Gemini AI-powered maintenance analysis and assistant
- Prediction history and analytics

## Dataset

The dataset contains **24,042 records** and **15 columns**.

The target variable is:

`failure_within_24h`

It indicates whether the machine is expected to fail within the next 24 hours.

### Class Distribution

- No Failure: 20,482 records (85.19%)
- Failure: 3,560 records (14.81%)

## Features

The project uses machine and sensor information such as:

- Machine type
- Vibration RMS
- Motor temperature
- Average phase current
- Pressure level
- RPM
- Operating mode
- Hours since maintenance
- Ambient temperature
- Timestamp

Additional engineered features include:

- Temperature difference
- Vibration/RPM ratio
- Current/RPM ratio
- Pressure/RPM ratio
- Maintenance load
- Day of week
- Month

## Data Preparation

The preprocessing pipeline includes:

- Missing-value imputation
- Numerical feature scaling using StandardScaler
- Categorical feature encoding using OneHotEncoder
- Feature engineering
- Feature selection

The following fields were excluded from the final model to reduce leakage or avoid using information that would not be available for prediction:

- `machine_id`
- `rul_hours`
- `failure_type`
- `estimated_repair_cost`
- Raw `timestamp`

## Machine Learning Models

The project evaluates four models:

1. Extra Trees
2. CatBoost
3. MLP Neural Network
4. XGBoost

### Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---:|---:|---:|---:|
| Extra Trees | 97.50% | 91.11% | 92.13% | 91.62% |
| CatBoost | 98.27% | 92.56% | 96.07% | 94.28% |
| MLP | 96.76% | 90.76% | 86.94% | 88.81% |
| XGBoost | 97.96% | 91.60% | 94.94% | 93.24% |

CatBoost is the model used by the application for machine failure prediction.

## Streamlit Application

The web application provides a professional dashboard for:

- Machine configuration
- Sensor data input
- Failure prediction
- Failure probability
- Engineered feature inspection
- Telemetry snapshot
- Prediction history
- Analytics
- CSV export
- AI maintenance analysis
- AI assistant chatbot

## Gemini AI Assistant

The application integrates Google's Gemini API to provide AI-assisted maintenance analysis.

The AI assistant uses the current machine prediction and supplied machine data to provide practical maintenance guidance.

**Important:** API keys are stored through Streamlit Secrets and are not included in the GitHub repository.

## Project Structure

```text
predictive-maintenance-ML/
│
├── app.py
├── app.ipynb
├── model.pkl
├── predictive_maintenance_v3.csv
├── predictive_maintenance_clean.csv
├── prediction_history.csv
├── requirements.txt
├── catboost_info/
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/shehab44osama-ui/predictive-maintenance-ML.git
cd predictive-maintenance-ML
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## Gemini Configuration

For local development, create:

```text
.streamlit/secrets.toml
```

and add:

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

Do not commit the secrets file or API key to GitHub.

## Deployment

The application can be deployed using Streamlit Community Cloud by connecting the GitHub repository and selecting:

- Repository: `shehab44osama-ui/predictive-maintenance-ML`
- Branch: `main`
- Main file: `app.py`

The Gemini API key should be added through the application's Streamlit Secrets settings.

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- CatBoost
- XGBoost
- Plotly
- Streamlit
- Google Gemini API
- Jupyter Notebook

## Objective

The main objective is to move from reactive maintenance to predictive maintenance by using machine learning to identify potential machine failures before they happen.

## Author

Machine Learning Project — Predictive Maintenance
