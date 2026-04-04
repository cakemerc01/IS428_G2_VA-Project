# RANKING OF PERSON AND GENRE INFLUENCE

import pandas as pd

# 1. Load the three heritage CSVs
try:
    perf_df = pd.read_csv('../data/sailor_sankey_performers.csv')
    prod_df = pd.read_csv('../data/sailor_sankey_producers.csv')
    lyric_df = pd.read_csv('../data/sailor_sankey_lyricists.csv')
except FileNotFoundError:
    print("Error: Ensure your 3 Sankey CSVs are in the ../data/ folder!")

# 2. Unify the names for a Master Count
p_names = perf_df[['Original_Performer']].rename(columns={'Original_Performer': 'Name'})
pr_names = prod_df[['Original_Producer']].rename(columns={'Original_Producer': 'Name'})
l_names = lyric_df[['Original_Lyricist']].rename(columns={'Original_Lyricist': 'Name'})

# 3. Combine and find the Top 5 People
all_names = pd.concat([p_names, pr_names, l_names])
top_10_list = all_names['Name'].value_counts().head(10).index.tolist()

# 4. Generate the Detailed Breakdown Table
breakdown_data = []

for person in top_10_list:
    p_count = len(perf_df[perf_df['Original_Performer'] == person])
    pr_count = len(prod_df[prod_df['Original_Producer'] == person])
    l_count = len(lyric_df[lyric_df['Original_Lyricist'] == person])
    total = p_count + pr_count + l_count
    
    breakdown_data.append({
        'Influencer': person,
        'Perf_Hits': p_count,
        'Prod_Hits': pr_count,
        'Lyric_Hits': l_count,
        'Total_Score': total
    })

# Create a DataFrame for a professional look
results_df = pd.DataFrame(breakdown_data)

# Calculate a "Dominance %" to show how much the #1 person leads
total_all_influence = len(all_names)
results_df['Influence_%'] = (results_df['Total_Score'] / total_all_influence * 100).round(1)

print("--- TOP 10 INFLUENCER BREAKDOWN (Total Heritage) ---")
print(results_df.to_string(index=False))

# 5. Genre Ranking (Top 5 Genres from Performers)
print("\n--- TOP 10 INFLUENTIAL GENRES ---")
genre_counts = perf_df['Reference_Genre'].value_counts().head(10)
print(genre_counts)