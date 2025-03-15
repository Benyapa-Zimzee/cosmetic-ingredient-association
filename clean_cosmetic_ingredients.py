import pandas as pd
import re

# --- Helper Functions ---

def is_valid_ingredient(token):
    """
    Check if a token is a valid ingredient:
    - At least 2 characters.
    - Contains at least one alphabetical character.
    """
    token = token.strip()
    if len(token) < 2:
        return False
    if not re.search(r'[a-zA-Z]', token):
        return False
    return True

def clean_ingredient_token(token):
    """
    Clean an individual ingredient token by:
      - Stripping extra whitespace and unwanted leading characters (like '-' or '*')
      - Removing trademark symbols (®, ™) and similar special characters
      - Handling colon-separated strings: for tokens starting with 'active ingredient' or 'ingredient',
        keep the part after the colon; otherwise, drop any description after a colon.
      - Removing percentage values (e.g., 20%, 20 %, 20.5%)
    """
    token = token.strip()
    token = token.lstrip("-*")
    token = token.replace("®", "").replace("™", "").replace("*", "")
    
    if ":" in token:
        parts = token.split(":", 1)
        lower_token = token.lower()
        if lower_token.startswith("active ingredient") or lower_token.startswith("ingredient"):
            token = parts[1].strip()
        else:
            token = parts[0].strip()
    
    token = re.sub(r'\d+(?:\.\d+)?\s*%', '', token)
    return token.strip()

def clean_ingredients(ingredient_str):
    """
    Clean a full ingredient string by:
      - Replacing 'and' and semicolons with commas.
      - Splitting into tokens.
      - Cleaning each token.
      - Filtering and normalizing valid ingredients.
      - Removing duplicates while preserving order.
      - Joining tokens with a comma separator.
    """
    if pd.isna(ingredient_str):
        return ""
    
    # Standardize delimiters
    ingredient_str = ingredient_str.replace(" and ", ",").replace(";", ",")
    tokens = ingredient_str.split(",")
    cleaned_tokens = []
    
    for token in tokens:
        cleaned = clean_ingredient_token(token)
        if is_valid_ingredient(cleaned):
            cleaned_tokens.append(cleaned.lower())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tokens = []
    for token in cleaned_tokens:
        if token not in seen:
            seen.add(token)
            unique_tokens.append(token)
    
    return ", ".join(unique_tokens)

# --- Main Processing ---

def main():
    # Read raw cosmetic data from the data folder
    df = pd.read_csv("data/cosmetic.csv")
    
    # Clean ingredients and create a new column 'clean_ingredients'
    df["clean_ingredients"] = df["ingredients"].apply(clean_ingredients)
    
    # Save the cleaned data back to the data folder
    df.to_csv("data/cosmetics_cleaned.csv", index=False)
    print("Cleaning complete. The cleaned file is saved as 'data/cosmetics_cleaned.csv'.")

if __name__ == "__main__":
    main()
