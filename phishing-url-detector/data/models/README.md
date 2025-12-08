# Models Directory

This directory stores trained machine learning models.

## Files

- `phishing_model.pkl` - Trained ensemble classifier (not included in repository)

## Training Your Own Model

To train a model with your own data:

```bash
python scripts/train_model.py --data path/to/your_dataset.csv
```

The trained model will be saved here automatically.

## Model Format

Models are saved using joblib and include:
- Trained classifier (ensemble of Logistic Regression, Random Forest, XGBoost)
- Feature scaler (StandardScaler)
- Feature names
- Model metadata

## Note

Pre-trained models are not included in the repository due to size and licensing considerations. You must train your own model using labeled phishing/benign URL datasets.
