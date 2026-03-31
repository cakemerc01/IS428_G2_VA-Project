import pandas as pd

df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Megan's works
megan_works = df[(df['name_source'] == 'Megan Bennett') & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Influence links
influence_types = ['InStyleOf', 'InterpolatesFrom', 'DirectlySamples', 'LyricalReferenceTo', 'CoverOf']
influence_data = df[(df['name_target'].isin(megan_works)) & (df['Edge Type'].isin(influence_types))].copy()

# 3. New Artists
referencing_songs = influence_data['name_source'].unique()
new_performers = df[(df['name_target'].isin(referencing_songs)) & (df['Edge Type'] == 'PerformerOf')].copy()

# 4. Merge
sankey_df = pd.merge(
    influence_data[['name_target', 'Edge Type', 'name_source']], 
    new_performers[['name_source', 'name_target']], 
    left_on='name_source', right_on='name_target', how='inner'
)

# Keep New_Song for counting purposes
sankey_df = sankey_df[['name_target_x', 'Edge Type', 'name_source_y', 'name_source_x']]
sankey_df.columns = ['Megans_Original_Work', 'Influence_Type', 'New_Artist', 'New_Song']
sankey_df['Weight'] = 1

sankey_df.to_csv('../data/megan_bennett_influence_sankey.csv', index=False)



# URSZULA STOCHMAL

import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify all songs/albums performed by Urszula Stochmal
target_person = 'Urszula Stochmal'
urszula_works = df[(df['name_source'] == target_person) & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Find anything that references HER work
# Source: The New Artist/Song -> Target: Urszula's Work
influence_types = ['InStyleOf', 'InterpolatesFrom', 'DirectlySamples', 'LyricalReferenceTo', 'CoverOf']
influence_data = df[(df['name_target'].isin(urszula_works)) & (df['Edge Type'].isin(influence_types))].copy()

# 3. Identify the PERFORMERS of the songs that referenced Urszula
referencing_songs = influence_data['name_source'].unique()
new_performers = df[(df['name_target'].isin(referencing_songs)) & (df['Edge Type'] == 'PerformerOf')].copy()

# 4. Merge to create the 3-Layer Flow: 
# Urszula's Work -> The Influence Type -> The New Artist
sankey_df = pd.merge(
    influence_data[['name_target', 'Edge Type', 'name_source']], 
    new_performers[['name_source', 'name_target']], 
    left_on='name_source',   # Match the referencing song
    right_on='name_target',  # To the performer's target
    how='inner'
)

# Rename and organize for Tableau
# We keep New_Song in the dataframe so you can use it for "Distinct Counts" in tooltips
sankey_df = sankey_df[['name_target_x', 'Edge Type', 'name_source_y', 'name_source_x']]
sankey_df.columns = ['Urszulas_Original_Work', 'Influence_Type', 'New_Artist', 'New_Song']
sankey_df['Weight'] = 1

# Save the file
output_path = '../data/urszula_stochmal_influence_sankey.csv'
sankey_df.to_csv(output_path, index=False)



# SAILOR SHIFT

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify all songs/albums performed by Sailor Shift
target_person = 'Sailor Shift'
sailor_works = df[(df['name_source'] == target_person) & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Find anything that references HER work
influence_types = ['InStyleOf', 'InterpolatesFrom', 'DirectlySamples', 'LyricalReferenceTo', 'CoverOf']
influence_data = df[(df['name_target'].isin(sailor_works)) & (df['Edge Type'].isin(influence_types))].copy()

# 3. Identify the PERFORMERS of the songs that referenced Sailor
referencing_songs = influence_data['name_source'].unique()
new_performers = df[(df['name_target'].isin(referencing_songs)) & (df['Edge Type'] == 'PerformerOf')].copy()

# 4. Merge to create the 3-Layer Flow: 
sankey_df = pd.merge(
    influence_data[['name_target', 'Edge Type', 'name_source']], 
    new_performers[['name_source', 'name_target']], 
    left_on='name_source',   # Match the referencing song
    right_on='name_target',  # To the performer's target
    how='inner'
)

# Rename and organize for Tableau
# We keep New_Song in the dataframe so you can use it for "Distinct Counts" in tooltips
sankey_df = sankey_df[['name_target_x', 'Edge Type', 'name_source_y', 'name_source_x']]
sankey_df.columns = ['Sailor_Original_Work', 'Influence_Type', 'New_Artist', 'New_Song']
sankey_df['Weight'] = 1

# Save the file
output_path = '../data/sailor_shift_influence_sankey.csv'
sankey_df.to_csv(output_path, index=False)


# KIMBERLY SNYDER

import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify all songs/albums performed by Kimberly Snyder
target_person = 'Kimberly Snyder'
kimberly_works = df[(df['name_source'] == target_person) & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Find anything that references HER work
# Source: The New Artist/Song -> Target: Kimberly's Work
influence_types = ['InStyleOf', 'InterpolatesFrom', 'DirectlySamples', 'LyricalReferenceTo', 'CoverOf']
influence_data = df[(df['name_target'].isin(kimberly_works)) & (df['Edge Type'].isin(influence_types))].copy()

# 3. Identify the PERFORMERS of the songs that referenced Kimberly
referencing_songs = influence_data['name_source'].unique()
new_performers = df[(df['name_target'].isin(referencing_songs)) & (df['Edge Type'] == 'PerformerOf')].copy()

# 4. Merge to create the 3-Layer Flow: 
# Kimberly's Work -> The Influence Type -> The New Artist
sankey_df = pd.merge(
    influence_data[['name_target', 'Edge Type', 'name_source']], 
    new_performers[['name_source', 'name_target']], 
    left_on='name_source',   # Match the referencing song
    right_on='name_target',  # To the performer's target
    how='inner'
)

# Rename and organize for Tableau
sankey_df = sankey_df[['name_target_x', 'Edge Type', 'name_source_y', 'name_source_x']]
sankey_df.columns = ['Kimberlys_Original_Work', 'Influence_Type', 'New_Artist', 'New_Song']
sankey_df['Weight'] = 1

# Save the file
output_path = '../data/kimberly_snyder_influence_sankey.csv'
sankey_df.to_csv(output_path, index=False)


# YONG ZHENG

import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify all songs/albums performed by Yong Zheng
target_person = 'Yong Zheng'
yz_works = df[(df['name_source'] == target_person) & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Find anything that references HIS work
# Source: The New Artist/Song -> Target: Yong Zheng's Work
influence_types = ['InStyleOf', 'InterpolatesFrom', 'DirectlySamples', 'LyricalReferenceTo', 'CoverOf']
influence_data = df[(df['name_target'].isin(yz_works)) & (df['Edge Type'].isin(influence_types))].copy()

# 3. Identify the PERFORMERS of the songs that referenced Yong Zheng
referencing_songs = influence_data['name_source'].unique()
new_performers = df[(df['name_target'].isin(referencing_songs)) & (df['Edge Type'] == 'PerformerOf')].copy()

# 4. Merge to create the 3-Layer Flow: 
# Yong Zheng's Work -> The Influence Type -> The New Artist
sankey_df = pd.merge(
    influence_data[['name_target', 'Edge Type', 'name_source']], 
    new_performers[['name_source', 'name_target']], 
    left_on='name_source',   # Match the referencing song
    right_on='name_target',  # To the performer's target
    how='inner'
)

# Rename and organize for Tableau
sankey_df = sankey_df[['name_target_x', 'Edge Type', 'name_source_y', 'name_source_x']]
sankey_df.columns = ['Yong_Zheng_Original_Work', 'Influence_Type', 'New_Artist', 'New_Song']
sankey_df['Weight'] = 1

# Save the file
output_path = '../data/yong_zheng_influence_sankey.csv'
sankey_df.to_csv(output_path, index=False)