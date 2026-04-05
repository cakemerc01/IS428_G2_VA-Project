import pandas as pd

# Load your CSVs
nodes = pd.read_csv('../data/mc1_nodes.csv')
edges = pd.read_csv('../data/mc1_edges.csv')

# 1. Filter edges for "PerformerOf" or "MemberOf" to find her works
# 2. Merge edges with nodes to get Source Names and Target Names
master_df = edges.merge(nodes, left_on='source', right_on='id', how='left')
master_df = master_df.merge(nodes, left_on='target', right_on='id', how='left', suffixes=('_source', '_target'))

# This creates columns like 'name_source' and 'name_target'
# Now you can easily filter 'name_source' = 'Sailor Shift' 
# to see all her 'name_target' (Albums/Songs)
master_df.to_csv('../data/mc1_1a.csv', index=False)



# WHO INFLUENCED SAILOR
import pandas as pd

# 1. Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 2. Identify Sailor Shift's performed songs/albums
target_artist = 'Sailor Shift'
her_works = df[(df['name_source'] == target_artist) & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 3. Filter for her outward influences
# We keep the 'name_target' (the song she referenced) to look up its credits later
influence_data = df[(df['name_source'].isin(her_works)) & 
                    (df['Edge Type'].isin(['InStyleOf', 'CoverOf', 'InterpolatesFrom', 'LyricalReferenceTo']))].copy()

# 4. Define the mapping for different contribution types
roles_to_process = {
    'PerformerOf': 'Performer',
    'ProducerOf': 'Producer',
    'LyricistOf': 'Lyricist',
    'ComposerOf': 'Composer'
}

# List to collect the results for each role
all_role_data = []

for edge_type, role_label in roles_to_process.items():
    # Find the specific contributors for the referenced songs
    referenced_songs = influence_data['name_target'].unique()
    
    contributors = df[(df['name_target'].isin(referenced_songs)) & 
                      (df['Edge Type'] == edge_type)][['name_source', 'name_target']]
    
    # Merge influence data with contributor data
    # Sailor Song -> Influence Genre -> Original Song -> Original Contributor
    flow = pd.merge(
        influence_data[['name_source', 'genre_target', 'name_target']], 
        contributors, 
        on='name_target', 
        how='inner'
    )
    
    if not flow.empty:
        # Prepare and standardize columns
        role_df = flow[['name_source_x', 'genre_target', 'name_source_y']].rename(columns={
            'name_source_x': 'Sailor_Work',
            'genre_target': 'Reference_Genre',
            'name_source_y': 'Original_Contributor'
        })
        
        # Add metadata
        role_df['Contribution_Type'] = role_label
        role_df['Weight'] = 1
        
        all_role_data.append(role_df)

# 5. Combine all roles into one master dataframe
final_combined_df = pd.concat(all_role_data, ignore_index=True)

# 6. Save to a single CSV
final_combined_df.to_csv('../data/combined_sailor_sankey_influenced.csv', index=False)
