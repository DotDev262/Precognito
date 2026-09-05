"""
Train ML anomaly detection model on predictive_maintenance.csv
"""

import pandas as pd
import pickle
import json
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Artifacts live beside this file so the runtime loader finds them.
BASE_PATH = Path(__file__).parent
CSV_PATH = BASE_PATH / 'predictive_maintenance.csv'

def load_and_preprocess_data():
    """Loads the predictive maintenance dataset and prepares features for training.

    Reads 'predictive_maintenance.csv', extracts relevant sensor columns,
    encodes the categorical 'Type' feature, and prepares the target labels.

    Returns:
        tuple: A tuple containing:
            - X (pd.DataFrame): Preprocessed feature matrix.
            - y (pd.Series): Target labels (0 for normal, 1 for anomaly).
            - feature_names (list): List of feature names in the correct order.
            - le (LabelEncoder): The fitted label encoder for categorical data.
    """
    print("Loading dataset...")
    df = pd.read_csv(CSV_PATH)
    
    # Features for anomaly detection
    feature_cols = [
        'Air temperature [K]', 
        'Process temperature [K]', 
        'Rotational speed [rpm]', 
        'Torque [Nm]', 
        'Tool wear [min]',
        'Type'
    ]
    
    # Prepare features
    X = df[feature_cols].copy()
    y = df['Target']  # 0 = normal, 1 = anomaly
    
    # Encode categorical variable
    le = LabelEncoder()
    X['Type_encoded'] = le.fit_transform(X['Type'])
    X = X.drop('Type', axis=1)
    
    # Feature names for later use
    feature_names = X.columns.tolist()
    
    print(f"Dataset shape: {X.shape}")
    print(f"Anomalies: {y.sum()} ({y.sum()/len(y)*100:.1f}%)")
    
    return X, y, feature_names, le

def train_isolation_forest(X, y):
    """Trains a supervised failure classifier with a tuned alarm threshold.

    Labels exist, so a supervised model replaces the previous unsupervised
    approach. Splits data into train/validation/test, fits a balanced
    random forest, then picks the lowest validation false-discovery
    threshold that keeps recall at or above 20 percent.

    Args:
        X (pd.DataFrame): Feature matrix.
        y (pd.Series): Target labels.

    Returns:
        tuple: (classifier, scaler, threshold).
    """
    print("Training supervised failure classifier...")

    # Split data
    X_train, X_tmp, y_train, y_tmp = train_test_split(
        X, y, test_size=0.4, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_tmp, y_tmp, test_size=0.5, random_state=42, stratify=y_tmp
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    # Train classifier (labels are available, so supervised beats unsupervised)
    clf = RandomForestClassifier(
        n_estimators=300,
        min_samples_leaf=5,
        class_weight="balanced_subsample",
        random_state=42,
        # Single-threaded inference: callers parallelize, avoiding oversubscription
        n_jobs=1,
    )
    clf.fit(X_train_scaled, y_train)

    # Tune alarm threshold on validation: lowest false discovery with recall >= 20%
    val_proba = clf.predict_proba(X_val_scaled)[:, 1]
    y_val_arr = y_val.to_numpy() if hasattr(y_val, "to_numpy") else y_val
    best = None
    for thr in [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9]:
        pred = val_proba >= thr
        tp = int(((pred == 1) & (y_val_arr == 1)).sum())
        fp = int(((pred == 1) & (y_val_arr == 0)).sum())
        fn = int(((pred == 0) & (y_val_arr == 1)).sum())
        rec = tp / (tp + fn) * 100 if tp + fn else 0
        fdr = fp / (tp + fp) * 100 if tp + fp else 0.0
        if rec >= 20.0 and (best is None or fdr < best[1]):
            best = (thr, fdr, rec)
    threshold = best[0] if best else 0.8
    print(f"Chosen threshold: {threshold} (val fdr={best[1]:.1f}, val rec={best[2]:.1f})"
          if best else "No threshold met recall floor; using 0.8")

    # Evaluate once on the held-out test set
    test_pred = (clf.predict_proba(X_test_scaled)[:, 1] >= threshold).astype(int)
    print("\nModel Evaluation (held-out test):")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, test_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, test_pred))

    return clf, scaler, threshold

def save_model_and_metadata(model, scaler, feature_names, label_encoder, threshold=0.8):
    """Saves the trained model, scaler, and associated metadata to disk.

    Args:
        model: The trained failure classifier.
        scaler (StandardScaler): The fitted feature scaler.
        feature_names (list): List of feature names used during training.
        label_encoder (LabelEncoder): The fitted label encoder for categorical data.
        threshold (float): Tuned alarm threshold on failure probability.
    """
    print("\nSaving model and metadata...")

    # Save model
    with open(BASE_PATH / 'anomaly_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Save scaler
    with open(BASE_PATH / 'scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    # Save feature names
    with open(BASE_PATH / 'feature_names.json', 'w') as f:
        json.dump(feature_names, f)

    # Save label encoder
    with open(BASE_PATH / 'label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)

    # Save feature statistics for validation
    feature_stats = {
        'feature_names': feature_names,
        'model_type': type(model).__name__,
        'threshold': threshold,
        'features_count': len(feature_names)
    }

    with open(BASE_PATH / 'feature_stats.json', 'w') as f:
        json.dump(feature_stats, f)

    print("Model and metadata saved successfully!")

def test_model_on_sample_data():
    """Tests the trained model and scaler on a set of predefined sample test cases.

    Loads the saved model and metadata from disk, runs predictions on several
    representative sensor telemetry samples, and prints the results.
    """
    print("\nTesting model on sample data...")
    with open(BASE_PATH / 'feature_stats.json', 'r') as f:
        threshold = json.load(f).get('threshold', 0.8)

    # Load model and scaler
    with open(BASE_PATH / 'anomaly_model.pkl', 'rb') as f:
        model = pickle.load(f)

    with open(BASE_PATH / 'scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    with open(BASE_PATH / 'feature_names.json', 'r') as f:
        feature_names = json.load(f)

    with open(BASE_PATH / 'label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Sample test cases
    test_cases = [
        # Normal case
        {
            'Air temperature [K]': 298.1,
            'Process temperature [K]': 308.6,
            'Rotational speed [rpm]': 1551,
            'Torque [Nm]': 42.8,
            'Tool wear [min]': 0,
            'Type': 'M'
        },
        # Potential anomaly (high temperature)
        {
            'Air temperature [K]': 304.0,
            'Process temperature [K]': 313.0,
            'Rotational speed [rpm]': 1551,
            'Torque [Nm]': 42.8,
            'Tool wear [min]': 50,
            'Type': 'M'
        },
        # Potential anomaly (low torque, high speed)
        {
            'Air temperature [K]': 298.1,
            'Process temperature [K]': 308.6,
            'Rotational speed [rpm]': 2800,
            'Torque [Nm]': 10.0,
            'Tool wear [min]': 100,
            'Type': 'L'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        # Prepare data
        df_test = pd.DataFrame([test_case])
        df_test['Type_encoded'] = label_encoder.transform(df_test['Type'])
        df_test = df_test.drop('Type', axis=1)
        
        # Ensure correct feature order
        X_test = df_test[feature_names]
        
        # Scale
        X_test_scaled = scaler.transform(X_test)
        
        # Predict
        failure_proba = float(model.predict_proba(X_test_scaled)[0][1])
        is_anomaly = failure_proba >= threshold

        print(f"\nTest Case {i}:")
        print(f"Data: {test_case}")
        print(f"Prediction: {'ANOMALY' if is_anomaly else 'NORMAL'}")
        print(f"Failure probability: {failure_proba:.4f} (threshold {threshold})")

def main():
    """Main training pipeline"""
    print("Starting ML Anomaly Detection Training Pipeline")
    print("=" * 60)
    
    try:
        # Load and preprocess data
        X, y, feature_names, label_encoder = load_and_preprocess_data()
        
        # Train model
        model, scaler, threshold = train_isolation_forest(X, y)

        # Save model and metadata
        save_model_and_metadata(model, scaler, feature_names, label_encoder, threshold)
        
        # Test on sample data
        test_model_on_sample_data()
        
        print("\n" + "=" * 60)
        print("Training completed successfully!")
        print("Model saved as: anomaly_model.pkl")
        print("Scaler saved as: scaler.pkl")
        
    except Exception as e:
        print(f"Error during training: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
