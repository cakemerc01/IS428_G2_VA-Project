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
