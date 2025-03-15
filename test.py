import os
os.makedirs("data", exist_ok=True)
print("Data folder exists:", os.path.exists("data"))
# This should print: Data folder exists: True

# Create an empty file to test
with open("data/cosmetics_cleaned.csv", "w") as f:
    f.write("clean_ingredients\n")

print("Test file created:", os.path.exists("data/cosmetics_cleaned.csv"))
