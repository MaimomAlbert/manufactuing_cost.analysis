import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
import joblib


def build_pipeline():
    # Columns
    categorical = ["material_type"]
    numerical = [
        "material_cost_per_kg",
        "quantity",
        "machine_hours",
        "machine_rate_per_hr",
        "labor_hours",
        "labor_rate_per_hr",
        "energy_consumption_kWh",
        "energy_rate_per_kWh",
        "overhead_cost",
        "defect_rate",
        "inventory_time_days",
        "inventory_cost_per_day",
    ]

    # Preprocessing for numeric: impute missing with median
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
    ])

    # Categorical: one-hot encode, handle unknowns
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numerical),
            ("cat", categorical_transformer, categorical),
        ],
        remainder='drop'
    )

    # Full pipeline
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=200, random_state=42))
    ])

    return pipeline


def train_and_save_model(csv_path: str, model_path: str = "models/model.pkl") -> None:
    df = pd.read_csv(csv_path)
    X = df.drop(columns=["total_cost"])  # features
    y = df["total_cost"]

    pipeline = build_pipeline()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    print(f"Trained model RMSE: {rmse:.2f}")

    # Save
    joblib.dump(pipeline, model_path)
    print(f"Model saved to: {model_path}")


def load_model(model_path: str = "models/model.pkl"):
    return joblib.load(model_path)