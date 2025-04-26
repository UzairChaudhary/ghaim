import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Load your updated places dataset
places_file = "UAE_Places_file2 (1).csv"  # Make sure this is in your folder
places_df = pd.read_csv(places_file, encoding="cp1252")

# Step 2: Encode categorical columns
le_weather = LabelEncoder()
le_emirate = LabelEncoder()
le_category = LabelEncoder()
le_place = LabelEncoder()

places_df['Weather Category'] = le_weather.fit_transform(places_df['Weather Category'])
places_df['Emirate'] = le_emirate.fit_transform(places_df['Emirate'])
places_df['Category'] = le_category.fit_transform(places_df['Category'])
places_df['Suggested Place'] = le_place.fit_transform(places_df['Suggested Place'])

# Step 3: Define features (X) and target (y)
X = places_df[['Weather Category', 'Emirate', 'Category']]
y = places_df['Suggested Place']

# Step 4: Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=18)

# Step 5: Train the model
model = GradientBoostingClassifier(random_state=18)
model.fit(X_train, y_train)

# Step 6: Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Step 7: Save the model and encoders
joblib.dump(model, "place_model.pkl")
joblib.dump(le_weather, "weather_encoder_places.pkl")
joblib.dump(le_emirate, "emirate_encoder_places.pkl")
joblib.dump(le_category, "category_encoder.pkl")
joblib.dump(le_place, "place_encoder.pkl")

print("✅ place_model.pkl and encoders saved successfully!")
