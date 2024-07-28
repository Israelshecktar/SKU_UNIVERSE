import requests

# Define the base URL of your Flask app
base_url = "http://localhost:5000/api/skus/brand"

# List of brands and their categories (extracted from the Excel sheet)
brands_categories = {
    "DULUX": [
        "water-based",
        "solvent-based",
        "Industrials",
        "DULUX EMULSION",
        "DULUX SILK EMULSION",
        "DULUX WEATHERSHIELD SMOOTH",
        "DULUX TEXMATT",
    ],
    "SANDTEX": [
        "water-based",
        "solvent-based",
        "industrials",
        "Sandtex specials",
        "SANDTEX VME",
        "SANDTEX GLOSS",
        "SANDTEX FINEBUILD",
    ],
    "CAPLUX": ["water-based", "solvent-based", "CAPLUX specials", "CAPLUX EMULSION"],
    "Hempel": ["MARINE PROTECTIVE COATING"],
    "Project": ["water-based", "solvent-based", "Project Industrials"],
}


# Function to test the API for each brand and category
def test_api():
    for brand, categories in brands_categories.items():
        for category in categories:
            url = f"{base_url}/{brand}?subcategory={category}"
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Success: {brand} - {category}")
                print(response.json())
            else:
                print(
                    f"Failed: {brand} - {category} with status code {response.status_code}"
                )


# Run the test
test_api()
