import requests
import math
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process


def load_csv(file_path):
    return pd.read_csv(file_path)

def load_pkl(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)
    

def get_lat_lon_from_address(address, access_token):
    try:
        url = f"https://us1.locationiq.com/v1/search.php?key={access_token}&q={address}&format=json"
        response = requests.get(url)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching geocode for {address}: {e}")
        return None, None

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def filter_by_location(user_lat, user_lon, restaurants, radius=7):
    filtered_restaurants = []
    for _, row in restaurants.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):  
            restaurant_lat = float(row['latitude'])
            restaurant_lon = float(row['longitude'])
            distance = haversine_distance(user_lat, user_lon, restaurant_lat, restaurant_lon)
            if distance <= radius:
                filtered_restaurants.append(row)
    return pd.DataFrame(filtered_restaurants)


data = load_csv(r"C:\Users\Vinod\OneDrive\vinodnayak desktop\project-gradious\preprocessed_data.csv")
data['profile'] = (
    data['Cuisine'].fillna('') + " " +
    data['Price_For_Two'].astype(str) + " " +
    data['Signature_Dishes'].fillna('') + " " +
    data['Special_Features'].fillna('') + " " +
    data['More_Info'].fillna('')
)


try:
    vectorizer = load_pkl("tfidf_vectorizer.pkl")
    tfidf_matrix = load_pkl("tfidf_matrix.pkl")
    print("Loaded TF-IDF vectorizer and matrix from pickle files.")
except FileNotFoundError:
    print("Pickle files not found. Generating TF-IDF vectorizer and matrix...")
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(data['profile'])
    with open("tfidf_vectorizer.pkl", "wb") as file:
        pickle.dump(vectorizer, file)
    with open("tfidf_matrix.pkl", "wb") as file:
        pickle.dump(tfidf_matrix, file)


def recommend_restaurants(user_lat, user_lon, cuisine, price_for_two, planning_for, liked_restaurant=None, top_n=5, radius=7):
    """Recommend restaurants based on location, profile similarity, and hybrid scoring."""
    location_filtered_data = filter_by_location(user_lat, user_lon, data, radius)
    if location_filtered_data.empty:
        print("No restaurants found in your location radius.")
        return pd.DataFrame()

    content_filtered_data = location_filtered_data[
        (location_filtered_data['Cuisine'].str.contains(cuisine, case=False, na=False)) &
        (location_filtered_data['Price_For_Two'] <= price_for_two) &
        (location_filtered_data['More_Info'].str.contains(planning_for, case=False, na=False))
    ].copy()

    if len(content_filtered_data) < top_n:
        related_cuisines = location_filtered_data[location_filtered_data['Cuisine'].str.contains(cuisine, case=False, na=False)]
        content_filtered_data = pd.concat([content_filtered_data, related_cuisines]).drop_duplicates()

    liked_index = None
    if liked_restaurant:
        match = process.extractOne(liked_restaurant, data['Names'])
        if match and match[1] >= 80:
            liked_index = data[data['Names'] == match[0]].index[0]

    if liked_index is not None:
        similarity_scores = cosine_similarity(tfidf_matrix[liked_index], tfidf_matrix[content_filtered_data.index]).flatten()
        content_filtered_data['similarity_score'] = similarity_scores
    else:
        content_filtered_data['similarity_score'] = 1  # Default similarity if no liked restaurant provided

    content_filtered_data['weighted_score'] = (
        0.5 * content_filtered_data['similarity_score'] +
        0.5 * (content_filtered_data['Ratings'] / data['Ratings'].max())
    )
    recommendations = content_filtered_data.sort_values(by='weighted_score', ascending=False).head(top_n)
    return recommendations[['Names', 'Cuisine', 'Price_For_Two', 'Ratings', 'Signature_Dishes', 'Location', 'Special_Features']]

address = input("Enter your address: ")
access_token = "pk.e28403f26ee75af55812430de27b810e" 
user_lat, user_lon = get_lat_lon_from_address(address, access_token)

if user_lat is None or user_lon is None:
    print("Could not find coordinates for the given address.")
else:
    cuisine = input("Enter preferred cuisine: ")
    price_for_two = int(input("Enter your budget for two people: "))
    planning_for = input("Enter the occasion: ")
    liked_restaurant = input("Enter a restaurant you liked (leave blank if none): ")
    result = recommend_restaurants(user_lat, user_lon, cuisine, price_for_two, planning_for, liked_restaurant)
    print(result)

