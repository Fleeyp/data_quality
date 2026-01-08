import json
import openai

openai.api_key = "gen_ai_api_key_here"

def extract_features(title, description):
    prompt = f"""
    You are a data extraction assistant.
    Given the product title and description below,
    extract structured features in JSON format.

    Title: {title}

    Description: {description}

    Return only valid JSON with:
    - category
    - material
    - compatibility
    - main_features (list)
    """

    response = openai.ChatCompletion.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}],
        store=True
    )

    return json.loads(response.choices[0].message.content)

data = {
    "title": "Leather Case with Mirror for Samsung Galaxy S8 Plus",
    "description": "Premium PU Leather. RFID protection. Handmade..."
}

# Para fazer uso deste script da maneira desejada, altere o prompt como desejar, e altere também o conteúdo de data

features = extract_features(data["title"], data["description"])
print(features)
