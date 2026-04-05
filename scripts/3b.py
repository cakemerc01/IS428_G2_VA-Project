import pandas as pd

# 1. Load master file
df = pd.read_csv('../data/mc1_1a.csv')

# List of artists to process
artists = [
    'Megan Bennett', 
    'Urszula Stochmal', 
    'Yong Zheng', 
    'Kimberly Snyder', 
    'Sailor Shift', 
    'Julia Carter', 
    'Claire Holmes', 
    'Cassian Storm',
    'Sienna Fox',
    "Selkie's Hollow",
    "Sylas Dune"
]

# Influence types to track
influence_types = ['InStyleOf', 'CoverOf', 'InterpolatesFrom', 'LyricalReferenceTo']

# List to store dataframes for each artist
all_artist_data = []

for person in artists:
    # 2. Identify the artist's performed songs/albums
    her_works = df[(df['name_source'] == person) & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()
    
    # 3. Filter for those songs' outward influences (The "Source -> Target" relationship)
    sankey_data = df[(df['name_source'].isin(her_works)) & 
                     (df['Edge Type'].isin(influence_types))].copy()
    
    if not sankey_data.empty:
        # 4. Prepare columns for the Viz Extension
        extension_prep = sankey_data[['name_source', 'genre_target']].rename(columns={
            'name_source': 'Song_Source',
            'genre_target': 'Genre_Target'
        })
        
        # 5. Add identifying metadata
        extension_prep['Weight'] = 1
        extension_prep['Person'] = person  # Add the filter column
        
        all_artist_data.append(extension_prep)

# 6. Combine all artists into one master dataframe
final_combined_df = pd.concat(all_artist_data, ignore_index=True)

# 7. Save to a single CSV
final_combined_df.to_csv('../data/combined_artist_reference_sankey.csv', index=False)

print(f"Success! Processed {len(artists)} artists into combined_artist_reference_sankey.csv")