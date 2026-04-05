import pandas as pd

# 1. Load Data
nodes = pd.read_csv('../data/mc1_nodes.csv')
edges = pd.read_csv('../data/mc1_edges.csv')

# 2. Pre-process Data
# Convert release dates to numeric and extract notable status
nodes['release_date_numeric'] = pd.to_numeric(nodes['release_date'], errors='coerce')
nodes['notable_bool'] = nodes['notable'].astype(str).str.strip().str.upper() == 'TRUE'

# Define Sailor Shift's ID
ss_id = 17255 

# 3. Identify Work and Reference Types
work_edge_types = ['PerformerOf', 'ComposerOf', 'LyricistOf', 'ProducerOf']
ref_edge_types = ['InterpolatesFrom', 'CoverOf', 'InStyleOf', 'LyricalReferenceTo', 'DirectlySamples']

# 4. Get Sailor Shift's Catalog
# Find all song/album IDs where Sailor Shift is a performer, composer, etc.
ss_catalog = set(edges[(edges['source'] == ss_id) & (edges['Edge Type'].isin(work_edge_types))]['target'])

# 5. Map Artists to their Works
# Get all "Artist" nodes (People or Musical Groups)
artist_nodes = nodes[nodes['Node Type'].isin(['Person', 'MusicalGroup'])]
artist_map = artist_nodes.set_index('id')['name'].to_dict()

# Link artists to their released tracks/albums
track_nodes = nodes[nodes['Node Type'].isin(['Song', 'Album'])][['id', 'release_date_numeric', 'notable_bool']]
artist_work_links = edges[(edges['source'].isin(artist_nodes['id'])) & (edges['Edge Type'].isin(work_edge_types))]
artist_to_track_data = artist_work_links.merge(track_nodes, left_on='target', right_on='id')

# 6. Calculate Metrics per Artist
# Debut Year (Earliest release)
debuts = artist_to_track_data.groupby('source')['release_date_numeric'].min().reset_index()
debuts.columns = ['artist_id', 'debut_year']

# Filter for those debuting 2030 onwards
candidates = debuts[debuts['debut_year'] >= 2030].copy()
candidate_ids = set(candidates['artist_id'])

# Metric A: Volume (Unique Songs/Albums)
volume = artist_to_track_data[artist_to_track_data['source'].isin(candidate_ids)].groupby('source')['target'].nunique().reset_index()
volume.columns = ['artist_id', 'num_songs']

# Metric B: Notability (Count of Notable Works)
notable = artist_to_track_data[(artist_to_track_data['source'].isin(candidate_ids)) & (artist_to_track_data['notable_bool'] == True)]
notability = notable.groupby('source')['target'].nunique().reset_index()
notability.columns = ['artist_id', 'num_notable']

# Metric C: Collaboration (Worked on the SAME track as Sailor Shift)
collaborators = set(edges[(edges['target'].isin(ss_catalog)) & (edges['Edge Type'].isin(work_edge_types))]['source'])
collaborators.discard(ss_id) # Remove self

# Metric D: References (Stylistic similarity/references to Sailor Shift's catalog)
# Count tracks by artist that reference a track in Sailor Shift's catalog
ref_edges = edges[(edges['target'].isin(ss_catalog)) & (edges['Edge Type'].isin(ref_edge_types))]
artist_refs = artist_work_links.merge(ref_edges, left_on='target', right_on='source')
ref_counts = artist_refs.groupby('source_x').size().reset_index()
ref_counts.columns = ['artist_id', 'ref_count']

# 7. Final Assembly and Ranking
final_ranking = candidates.merge(volume, on='artist_id', how='left')
final_ranking = final_ranking.merge(notability, on='artist_id', how='left').fillna(0)
final_ranking = final_ranking.merge(ref_counts, on='artist_id', how='left').fillna(0)
final_ranking['collab_ss'] = final_ranking['artist_id'].isin(collaborators)
final_ranking['name'] = final_ranking['artist_id'].map(artist_map)

# Sorting: By Volume, then Notability, then Collaboration, then References
top_10 = final_ranking.sort_values(
    by=['num_songs', 'num_notable', 'collab_ss', 'ref_count'], 
    ascending=False
).head(10)

print(top_10[['name', 'debut_year', 'num_songs', 'num_notable', 'collab_ss', 'ref_count']])