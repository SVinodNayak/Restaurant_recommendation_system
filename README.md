# Restaurant_recommendation_system

## **Overview**
This project is a Python-based recommendation system designed to help users discover restaurants that align with their preferences. It combines location-based filtering, content-based filtering, and hybrid scoring to provide personalized suggestions.

---

## **Features**
- **Location-Based Recommendations**: Finds restaurants within a specified radius of the user's location.
- **Content-Based Filtering**: Matches user preferences (cuisine, budget, occasion) using text similarity and machine learning.
- **Hybrid Scoring**: Combines similarity scores and restaurant ratings for improved rankings.
- **User-Friendly Input**: Accepts address, preferences, and optionally, a liked restaurant for better recommendations.

---

## **How It Works**
1. **Input**:
   - User provides an address, preferred cuisine, budget, occasion, and optionally, a liked restaurant.
2. **Geocoding**:
   - The address is converted into geographic coordinates (latitude and longitude) using the LocationIQ API.
3. **Filtering**:
   - Filters restaurants within the given radius based on location.
   - Further narrows down options using user preferences and restaurant features.
4. **Recommendation**:
   - Generates a ranked list of restaurants based on weighted scores combining similarity and ratings.

---

## **Setup Instructions**

### **Prerequisites**
Ensure you have the following installed:
- **Python**: Version 3.8 or higher
- Required Python libraries:  
  - `pandas`
  - `scikit-learn`
  - `fuzzywuzzy`
  - `requests`

### **Clone the Repository**
```bash
git clone https://github.com/YourUsername/RepositoryName.git
cd RepositoryName
```

### **Install Dependencies**
Run the following command to install all necessary libraries:
```bash
pip install -r requirements.txt
```

### **Prepare the Dataset**
1. Save your restaurant data as `preprocessed_data.csv` in the project directory.  
   - Ensure the file includes columns like `Cuisine`, `Price_For_Two`, `Signature_Dishes`, `Ratings`, `More_Info`, `Latitude`, and `Longitude`.

2. If you don’t have preprocessed TF-IDF files (`tfidf_vectorizer.pkl` and `tfidf_matrix.pkl`), the script will generate them automatically during runtime.

---

## **Run the Application**
Execute the script to start the recommendation process:
```bash
python content_based_filtering.py
```

### **User Input**
1. **Enter your address**: *e.g., "123 Main Street, City, Country"*.  
   (Uses LocationIQ API to fetch latitude and longitude.)  
2. **Enter preferred cuisine**: *e.g., "Italian"*.  
3. **Enter budget for two people**: *e.g., 1000*.  
4. **Enter the occasion**: *e.g., "Dinner"*.  
5. **Enter a restaurant you liked (optional)**: *e.g., "Pizza Palace"*.  

The system will display a list of recommended restaurants based on your input.

---


## **API Configuration**
This script uses the **LocationIQ API** for geocoding (converting addresses to geographic coordinates).  

1. Sign up for an API key at [LocationIQ](https://locationiq.com/).  
2. Replace the placeholder API key in the script with your API key:
   ```python
   access_token = "your_api_key_here"
   ```

---

## **Example Usage**
- Address: *"vizag"*  
- Preferred Cuisine: *"Chinese"*  
- Budget for Two: *500*  
- Occasion: *"Lunch"*  
- Liked Restaurant: *"Golden Dragon"*  

