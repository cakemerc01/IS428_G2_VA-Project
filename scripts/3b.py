# SIENNA FOX

import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify all songs/albums performed by Sienna Fox
target_person = 'Sienna Fox'
sf_works = df[(df['name_source'] == target_person) & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Find anything that references HIS work
# Source: The New Artist/Song -> Target: Sienna Fox's Work
influence_types = ['InStyleOf', 'InterpolatesFrom', 'DirectlySamples', 'LyricalReferenceTo', 'CoverOf']
influence_data = df[(df['name_target'].isin(sf_works)) & (df['Edge Type'].isin(influence_types))].copy()

# 3. Identify the PERFORMERS of the songs that referenced Yong Zheng
referencing_songs = influence_data['name_source'].unique()
new_performers = df[(df['name_target'].isin(referencing_songs)) & (df['Edge Type'] == 'PerformerOf')].copy()

# 4. Merge to create the 3-Layer Flow: 
# Sienna Fox's Work -> The Influence Type -> The New Artist
sankey_df = pd.merge(
    influence_data[['name_target', 'Edge Type', 'name_source']], 
    new_performers[['name_source', 'name_target']], 
    left_on='name_source',   # Match the referencing song
    right_on='name_target',  # To the performer's target
    how='inner'
)

# Rename and organize for Tableau
sankey_df = sankey_df[['name_target_x', 'Edge Type', 'name_source_y', 'name_source_x']]
sankey_df.columns = ['Sienna_Fox_Original_Work', 'Influence_Type', 'New_Artist', 'New_Song']
sankey_df['Weight'] = 1

# Save the file
output_path = '../data/sienna_fox_influence_sankey.csv'
sankey_df.to_csv(output_path, index=False)








# SYLAS DUNE

import pandas as pd

df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Use a flexible search for the name
target_name = "Sylas Dune"

# 2. Get all works associated with him
# We use .str.contains to handle potential trailing spaces or case issues
sylas_works = df[df['name_source'].str.contains(target_name, na=False, case=False) & 
                 (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 3. Create a master list of EVERYTHING that represents him (Songs + Person Name)
all_targets = list(sylas_works) + [target_name]

# 4. Find ANY influence pointing to that list
influence_types = ['InStyleOf', 'InterpolatesFrom', 'DirectlySamples', 'LyricalReferenceTo', 'CoverOf']
influence_data = df[df['name_target'].isin(all_targets) & 
                    df['Edge Type'].isin(influence_types)].copy()

# 5. Get the performers of those referencing songs
if not influence_data.empty:
    referencing_entities = influence_data['name_source'].unique()
    new_performers = df[df['name_target'].isin(referencing_entities) & 
                        (df['Edge Type'] == 'PerformerOf')].copy()

    # 6. Merge
    sankey_df = pd.merge(
        influence_data[['name_target', 'Edge Type', 'name_source']], 
        new_performers[['name_source', 'name_target']], 
        left_on='name_source', right_on='name_target', how='inner'
    )
    
    sankey_df.columns = ['Original_Legacy', 'Influence_Type', 'New_Artist', 'New_Song']
    sankey_df['Weight'] = 1
    sankey_df.to_csv('../data/sylas_dune_influence_sankey.csv', index=False)
    print(f"Success! Found {len(sankey_df)} connections.")
else:
    print(f"Still empty. This means NO ONE in the dataset is recorded as being influenced by {target_name}.")