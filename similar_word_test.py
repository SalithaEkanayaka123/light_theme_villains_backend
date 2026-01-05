import jellyfish
import pandas as pd

# Sample customer data
data = {
    "Customer_ID": [
        1, 2, 3, 4, 5, 6,
        7, 8, 9, 10, 11, 12,
        13, 14, 15, 16, 17, 18
    ],
    "Customer_Name": [
        "John Smith",
        "Jon Smith",
        "Jhon Smiht",
        "John Smyth",
        "Johnny Smith",
        "J. Smith",
        "Alice Brown",
        "Alic Brown",
        "Alise Brown",
        "Alice Brawn",
        "A. Brown",
        "Bob Miller",
        "Bobb Miller",
        "Robert Miller",
        "Robt Miller",
        "Bob Milner",
        "Smith John",
        "Jonathon Smith"
    ]
}

df = pd.DataFrame(data)

# Similarity threshold
THRESHOLD = 0.88

def find_similar_names(df):
    matches = []
    
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            name1 = df.loc[i, "Customer_Name"]
            name2 = df.loc[j, "Customer_Name"]
            
            similarity = jellyfish.jaro_winkler_similarity(name1, name2)
            
            if similarity >= THRESHOLD:
                matches.append({
                    "Name_1": name1,
                    "Name_2": name2,
                    "Similarity_Score": round(similarity, 3)
                })
    
    return pd.DataFrame(matches)

similar_names_df = find_similar_names(df)
print(similar_names_df)