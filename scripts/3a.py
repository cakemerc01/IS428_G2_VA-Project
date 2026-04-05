import pandas as pd

# 1. Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# List of target artists to analyze for their outward influence
target_artists = [
    'Megan Bennett', 
    'Urszula Stochmal', 
    'Sailor Shift', 
    'Kimberly Snyder', 
    'Yong Zheng'
]

# Influence types that show others referencing the target artist
influence_types = ['InStyleOf', 'InterpolatesFrom', 'DirectlySamples', 'LyricalReferenceTo', 'CoverOf']

# List to collect data for the final file
all_influence_flows = []

for artist in target_artists:
    # A. Identify the artist's performed works
    works = df[(df['name_source'] == artist) & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()
    
    # B. Find songs that reference these works
    # name_source here is the 'New Song', name_target is the 'Original Work'
    influence_links = df[(df['name_target'].isin(works)) & (df['Edge Type'].isin(influence_types))].copy()
    
    # C. Identify the performers of those new referencing songs
    referencing_songs = influence_links['name_source'].unique()
    new_performers = df[(df['name_target'].isin(referencing_songs)) & (df['Edge Type'] == 'PerformerOf')].copy()
    
    # D. Merge to create the 3-Layer Flow: Original Work -> Influence Type -> New Artist
    flow = pd.merge(
        influence_links[['name_target', 'Edge Type', 'name_source']], 
        new_performers[['name_source', 'name_target']], 
        left_on='name_source',   # Match the referencing song
        right_on='name_target',  # To the performer's song target
        how='inner'
    )
    
    if not flow.empty:
        # E. Clean and standardize columns
        flow = flow[['name_target_x', 'Edge Type', 'name_source_y', 'name_source_x']]
        flow.columns = ['Original_Work', 'Influence_Type', 'New_Artist', 'New_Song']
        
        # F. Add Metadata for filtering and weighting
        flow['Target_Artist'] = artist  # Use this to filter your dashboard
        flow['Weight'] = 1
        
        all_influence_flows.append(flow)

# 2. Combine and Save
final_sankey_df = pd.concat(all_influence_flows, ignore_index=True)
final_sankey_df.to_csv('../data/combined_influence_sankey.csv', index=False)

print(f"Success! Generated combined_influence_sankey.csv with {len(target_artists)} target artists.")