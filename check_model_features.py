import pickle
import pandas as pd

# Load the model
try:
    with open("flight_price_rf.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    
    # Print the feature names that the model was trained with
    print("Model Feature Names:")
    if hasattr(model, 'feature_names_in_'):
        for i, feature in enumerate(model.feature_names_in_):
            print(f"{i+1}. {feature}")
    else:
        print("Model does not have feature_names_in_ attribute")
    
except FileNotFoundError:
    print("Model file not found")
except Exception as e:
    print(f"Error: {e}")