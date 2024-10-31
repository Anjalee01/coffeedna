import os
from dotenv import load_dotenv
from openai import OpenAI
from transformers import pipeline  # Hugging Face transformers library
from backend.chat_history import load_history, save_history  # Ensure these imports are present

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)
sentiment_analyzer = pipeline("sentiment-analysis")

def fetch_online_store_recommendations(user_preferences):
    return "Recommended stores based on preferences"

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
    
    # Extract image URL and fact from GPT-4 response
    content = response.choices[0].message.content
    
    # Parse the output for image_url and fact (assuming GPT-4 responds in JSON-like format)
    # Here we mock parsing for simplicity; ideally, the response should be parsed more robustly
    image_url = "sample-coffee.jpg"  # Default or parsed from response
    fact = content.strip()  # Assume response only includes the fact if no strict JSON is returned

    return {
        "image_url": image_url,
        "fact": fact
    }


def get_coffee_recommendation(user_id, user_input, user_preferences):

    save_history(user_id, {"role": "user", "content": user_input})
    history = load_history(user_id)

    language = user_preferences.get("language", "English")
    tone = user_preferences.get("tone", "friendly")
    detail_level = user_preferences.get("detail_level", "concise")
    
    # Analyze user sentiment using BERT
    sentiment = sentiment_analyzer(user_input)[0]  # Analyze the sentiment of the latest user input
    user_sentiment = sentiment['label']

    # Fetch online store recommendations and coffee images/facts
    online_store_suggestions = fetch_online_store_recommendations(user_preferences)
    coffee_image_fact = fetch_coffee_image_and_fact(user_preferences)

    # Construct the recommendation prompt
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
    save_history(user_id, {"role": "assistant", "content": response})
    return response
