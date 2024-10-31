import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from transformers import pipeline  # Hugging Face transformers library
from backend.chat_history import load_history, save_history  # Ensure these imports are present
from deep_translator import GoogleTranslator  # Use Deep Translator for language translation

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
client = OpenAI(api_key=api_key)

sentiment_analyzer = pipeline("sentiment-analysis")

def load_stores_data():
    file_path = os.path.join('data', 'stores_data.json')  # Adjust the path as necessary
    with open(file_path, 'r') as file:
        return json.load(file)

def fetch_online_store_recommendations(user_preferences):
    stores_data = load_stores_data()  # Load stores data from JSON
    preferred_types = user_preferences.get("coffee_types", [])
    user_location = user_preferences.get("location", "Global")
    desired_services = user_preferences.get("services", [])
    recommended_stores = []
    for store in stores_data:
        score = 0
        if (any(coffee in store["types"] for coffee in preferred_types) and 
                (store["location"] == user_location or store["location"] == "Global")):
            score += 1  # Increase score for matching types and location
            
            # Check for matching services
            matching_services = set(store["services"]) & set(desired_services)
            score += len(matching_services)  # Increase score based on number of matching services

            recommended_stores.append({
                "name": store["name"],
                "url": store["url"],
                "services": list(matching_services),
                "score": score  # Store the score for potential future sorting
            })

    # Sort recommended stores by score in descending order
    recommended_stores.sort(key=lambda x: x['score'], reverse=True)

    # If no specific recommendations, return top 3 global stores
    if not recommended_stores:
        recommended_stores = [{"name": store["name"], "url": store["url"], "services": store["services"]}
                              for store in stores_data[:3]]
    return recommended_stores

def fetch_coffee_image_and_fact(user_preferences):
    prompt = (
        f"Provide a URL to an image of coffee and a fun, interesting fact about coffee. "
        f"Consider user preferences such as coffee type or flavor profile: {user_preferences}. "
        "The response should include an 'image_url' and a 'fact'."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    
    content = response.choices[0].message.content
    image_url = "sample-coffee.jpg"  # Default or parsed from response
    fact = content.strip()  # Assume response only includes the fact if no strict JSON is returned

    return {
        "image_url": image_url,
        "fact": fact
    }

def translate_response(response_text, target_language):
    try:
        translation = GoogleTranslator(source='auto', target=target_language).translate(response_text)
        return translation
    except Exception as e:
        print(f"Error during translation: {e}")
        return response_text  # Fallback to original text if translation fails

def get_coffee_recommendation(user_id, user_input, user_preferences):
    save_history(user_id, {"role": "user", "content": user_input})
    history = load_history(user_id)

    language = user_preferences.get("language", "English")
    tone = user_preferences.get("tone", "friendly")
    detail_level = user_preferences.get("detail_level", "concise")
    sentiment = sentiment_analyzer(user_input)[0]  # Analyze the sentiment of the latest user input
    user_sentiment = sentiment['label']
    online_store_suggestions = fetch_online_store_recommendations(user_preferences)
    coffee_image_fact = fetch_coffee_image_and_fact(user_preferences)

    recommendation_prompt = (
        f"Based on user preferences {user_preferences}, language: {language}, tone: {tone}, "
        f"detail level: {detail_level}, and sentiment analysis: {user_sentiment}. "
        f"Consider user chat history: {history}. "
        "Provide an engaging and personalized coffee recommendation, including sample serving images, "
        f"interesting facts: {coffee_image_fact['fact']}, and store suggestions: {online_store_suggestions}."
    )
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": recommendation_prompt}],
    )

    response = completion.choices[0].message.content
    translated_response = translate_response(response, language)
    save_history(user_id, {"role": "assistant", "content": translated_response})
    return translated_response
