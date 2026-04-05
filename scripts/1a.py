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

# COVERS

# Load your master file
df = pd.read_csv('../data/mc1_1a.csv')

# 1. Find the names of songs performed by Sailor Shift
her_songs = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Find rows where those songs are covering something
covers_df = df[(df['name_source'].isin(her_songs)) & (df['Edge Type'] == 'CoverOf')].copy()

# 3. Add her name as the 'Performer' so Tableau can filter it
covers_df['Performer'] = 'Sailor Shift'

# Save this simple version
covers_df.to_csv('../data/sailor_covers.csv', index=False)

# INSPIRATION

import pandas as pd

df = pd.read_csv('../data/mc1_1a.csv')

# 1. Identify all songs performed by Sailor Shift
her_songs = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Define the "Aesthetic" influence types
inspiration_types = ['InStyleOf', 'InterpolatesFrom', 'DirectlySamples', 'LyricalReferenceTo']

# 3. Filter for those types where HER song is the source
inspirations_df = df[(df['name_source'].isin(her_songs)) & (df['Edge Type'].isin(inspiration_types))].copy()

# 4. Add a column for easier filtering in Tableau
inspirations_df['Artist'] = 'Sailor Shift'

# Save the file
inspirations_df.to_csv('../data/sailor_inspirations.csv', index=False)

# PERFORMER OF WORKS SAILOR REFERENCED

import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify her performed songs/albums
her_works = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Filter for her outward influences
# We keep the 'name_target' (the song she referenced) to look up its performer later
sankey_data = df[(df['name_source'].isin(her_works)) & 
                 (df['Edge Type'].isin(['InStyleOf', 'CoverOf', 'InterpolatesFrom', 'LyricalReferenceTo']))].copy()

# 3. Find the performers of the songs Sailor Shift referenced
# 'name_target' in sankey_data is the song being referenced
referenced_songs = sankey_data['name_target'].unique()

# Look for the performers of these referenced songs
performers_of_referenced = df[(df['name_target'].isin(referenced_songs)) & 
                              (df['Edge Type'] == 'PerformerOf')][['name_source', 'name_target']]

# 4. Merge to create the 3-layer relationship
# We join the influence data with the performer data on the song name
three_layer_df = pd.merge(
    sankey_data[['name_source', 'genre_target', 'name_target']], 
    performers_of_referenced, 
    on='name_target', 
    how='inner'
)

# 5. Prepare for Tableau Viz Extension
# Layer 1: Song_Source (Sailor's Work)
# Layer 2: Genre_Target (The Genre of the song she referenced)
# Layer 3: Original_Performer (The artist who made that referenced song)
extension_prep = three_layer_df[['name_source_x', 'genre_target', 'name_source_y']].rename(columns={
    'name_source_x': 'Sailor_Work',
    'genre_target': 'Reference_Genre',
    'name_source_y': 'Original_Performer'
})

# 6. Add a weight
extension_prep['Weight'] = 1

# Save the file
extension_prep.to_csv('../data/sailor_sankey_performers.csv', index=False)


# PRODUCER OF WORKS SAILOR REFERENCED

import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify her performed songs/albums
her_works = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Filter for her outward influences
sankey_data = df[(df['name_source'].isin(her_works)) & 
                 (df['Edge Type'].isin(['InStyleOf', 'CoverOf', 'InterpolatesFrom', 'LyricalReferenceTo']))].copy()

# 3. Find the PRODUCERS of the songs Sailor Shift referenced
referenced_songs = sankey_data['name_target'].unique()

# Look for the PRODUCERS instead of performers
producers_of_referenced = df[(df['name_target'].isin(referenced_songs)) & 
                             (df['Edge Type'] == 'ProducerOf')][['name_source', 'name_target']]

# 4. Merge to create the 3-layer relationship
three_layer_df = pd.merge(
    sankey_data[['name_source', 'genre_target', 'name_target']], 
    producers_of_referenced, 
    on='name_target', 
    how='inner'
)

# 5. Prepare for Tableau Viz Extension
# Layer 1: Sailor's Work
# Layer 2: The Genre of the reference
# Layer 3: Original_Producer
extension_prep = three_layer_df[['name_source_x', 'genre_target', 'name_source_y']].rename(columns={
    'name_source_x': 'Sailor_Work',
    'genre_target': 'Reference_Genre',
    'name_source_y': 'Original_Producer'
})

# 6. Add a weight
extension_prep['Weight'] = 1

# Save the file with a specific name for producers
extension_prep.to_csv('../data/sailor_sankey_producers.csv', index=False)


# LYRICIST OF WORKS SAILOR REFERENCED

import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify her performed songs/albums
her_works = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Filter for her outward influences
sankey_data = df[(df['name_source'].isin(her_works)) & 
                 (df['Edge Type'].isin(['InStyleOf', 'CoverOf', 'InterpolatesFrom', 'LyricalReferenceTo']))].copy()

# 3. Find the LYRICISTS of the songs Sailor Shift referenced
referenced_songs = sankey_data['name_target'].unique()

# Look for the LYRICISTS instead of performers or producers
lyricists_of_referenced = df[(df['name_target'].isin(referenced_songs)) & 
                             (df['Edge Type'] == 'LyricistOf')][['name_source', 'name_target']]

# 4. Merge to create the 3-layer relationship
three_layer_df = pd.merge(
    sankey_data[['name_source', 'genre_target', 'name_target']], 
    lyricists_of_referenced, 
    on='name_target', 
    how='inner'
)

# 5. Prepare for Tableau Viz Extension
# Layer 1: Sailor's Work
# Layer 2: The Genre of the reference
# Layer 3: Original_Lyricist
extension_prep = three_layer_df[['name_source_x', 'genre_target', 'name_source_y']].rename(columns={
    'name_source_x': 'Sailor_Work',
    'genre_target': 'Reference_Genre',
    'name_source_y': 'Original_Lyricist'
})

# 6. Add a weight
extension_prep['Weight'] = 1

# Save the file with a specific name for lyricists
extension_prep.to_csv('../data/sailor_sankey_lyricists.csv', index=False)


# COMPOSER OF WORK SAILOR REFERENCED

import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify her performed songs/albums
# We start by finding everything Sailor Shift actually released
her_works = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Filter for her outward influences
# This looks at what those specific Sailor Shift songs are "influenced by"
sankey_data = df[(df['name_source'].isin(her_works)) & 
                 (df['Edge Type'].isin(['InStyleOf', 'CoverOf', 'InterpolatesFrom', 'LyricalReferenceTo']))].copy()

# 3. Find the COMPOSERS of the songs Sailor Shift referenced
referenced_songs = sankey_data['name_target'].unique()

# We look for the 'ComposerOf' credit for those original songs
composers_of_referenced = df[(df['name_target'].isin(referenced_songs)) & 
                             (df['Edge Type'] == 'ComposerOf')][['name_source', 'name_target']]

# 4. Merge to create the 3-layer relationship
# This joins: Sailor Song -> Influence Genre -> Original Song -> Original Composer
three_layer_df = pd.merge(
    sankey_data[['name_source', 'genre_target', 'name_target']], 
    composers_of_referenced, 
    on='name_target', 
    how='inner'
)

# 5. Prepare for Tableau Viz Extension (Voz Sankey)
extension_prep = three_layer_df[['name_source_x', 'genre_target', 'name_source_y']].rename(columns={
    'name_source_x': 'Sailor_Work',
    'genre_target': 'Reference_Genre',
    'name_source_y': 'Original_Composer'
})

# 6. Add a weight for the Sankey flow
extension_prep['Weight'] = 1

# Save for Tableau
extension_prep.to_csv('../data/sailor_sankey_composers.csv', index=False)