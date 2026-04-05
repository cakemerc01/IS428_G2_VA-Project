import pandas as pd

# 1. Load Data
nodes = pd.read_csv('../data/mc1_nodes.csv')
edges = pd.read_csv('../data/mc1_edges.csv')

# 2. Pre-process Data
nodes['release_date_numeric'] = pd.to_numeric(nodes['release_date'], errors='coerce')
nodes['notable_bool'] = nodes['notable'].astype(str).str.strip().str.upper() == 'TRUE'
ss_id = 17255 # Sailor Shift's Node ID

# 3. Define Artist Work Roles
work_edge_types = ['PerformerOf', 'ComposerOf', 'LyricistOf', 'ProducerOf']

# 4. Map Artists to Unique Tracks (with Genre & Notable status)
artist_nodes = nodes[nodes['Node Type'].isin(['Person', 'MusicalGroup'])][['id', 'name']]
track_nodes = nodes[nodes['Node Type'].isin(['Song', 'Album'])][['id', 'genre', 'notable_bool', 'release_date_numeric']]

# Build a mapping of Artist ID -> Track ID
artist_to_tracks_raw = edges[
    (edges['source'].isin(artist_nodes['id'])) & 
    (edges['Edge Type'].isin(work_edge_types))
].merge(track_nodes, left_on='target', right_on='id')

# CRITICAL: Drop duplicates to ensure unique tracks (prevents double-counting multiple roles)
artist_to_tracks = artist_to_tracks_raw.drop_duplicates(subset=['source', 'target'])

# 5. Filter for 2030+ Debut Candidates
debuts = artist_to_tracks.groupby('source')['release_date_numeric'].min().reset_index()
debuts.columns = ['artist_id', 'debut_year']
candidates = debuts[debuts['debut_year'] >= 2030].copy()

# 6. Metric Calculations

# A. Volume & Quality
stats = artist_to_tracks.groupby('source').agg(
    num_songs=('target', 'count'),
    num_notable=('notable_bool', 'sum')
).reset_index().rename(columns={'source': 'artist_id'})

# B. Notable Debut (Did they have a notable song in their first year?)
candidate_tracks = artist_to_tracks.merge(candidates, left_on='source', right_on='artist_id')
notable_debut_ids = candidate_tracks[
    (candidate_tracks['release_date_numeric'] == candidate_tracks['debut_year']) & 
    (candidate_tracks['notable_bool'] == True)
]['artist_id'].unique()

# C. Collaboration with Sailor Shift (Shared credits on the same track)
ss_catalog = set(edges[(edges['source'] == ss_id) & (edges['Edge Type'].isin(work_edge_types))]['target'])
collaborators = set(edges[(edges['target'].isin(ss_catalog)) & (edges['Edge Type'].isin(work_edge_types))]['source'])
collaborators.discard(ss_id)

# D. NEW: Top Genre & Percentage
# Count genre occurrences per artist
genre_counts = artist_to_tracks.groupby(['source', 'genre']).size().reset_index(name='count')
# Sort by artist, then count (descending) to find the most frequent genre
genre_counts = genre_counts.sort_values(['source', 'count'], ascending=[True, False])
top_genres = genre_counts.groupby('source').first().reset_index()

# Calculate genre percentage: (genre_count / total_songs)
top_genres = top_genres.merge(stats[['artist_id', 'num_songs']], left_on='source', right_on='artist_id')
top_genres['genre_pct'] = (top_genres['count'] / top_genres['num_songs']) * 100
top_genres = top_genres[['source', 'genre', 'genre_pct']].rename(columns={'source': 'artist_id', 'genre': 'top_genre'})

# 7. Final Assembly and Ranking
final = candidates.merge(stats, on='artist_id', how='left')
final = final.merge(top_genres, on='artist_id', how='left')
final['notable_debut'] = final['artist_id'].isin(notable_debut_ids)
final['collab_ss'] = final['artist_id'].isin(collaborators)
final['name'] = final['artist_id'].map(artist_nodes.set_index('id')['name'])

# Ranking order: songs released -> notable works -> notable debut -> collaborated -> genre focus
top_10 = final.sort_values(
    by=['num_songs', 'num_notable', 'notable_debut', 'collab_ss', 'genre_pct'], 
    ascending=[False, False, False, False, False]
).head(10)

print(top_10[['name', 'debut_year', 'num_songs', 'num_notable', 'notable_debut', 'collab_ss', 'top_genre', 'genre_pct']])