import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv')

# 1. Identify her performed songs/albums
her_works = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['name_target'].unique()

# 2. Filter for her outward influences
# This creates the "Source -> Target" relationship
sankey_data = df[(df['name_source'].isin(her_works)) & 
                 (df['Edge Type'].isin(['InStyleOf', 'CoverOf', 'InterpolatesFrom', 'LyricalReferenceTo']))].copy()

# 3. Create the clean columns for the Viz Extension
# Source = Her Song, Target = The Influence Genre
extension_prep = sankey_data[['name_source', 'genre_target']].rename(columns={
    'name_source': 'Song_Source',
    'genre_target': 'Genre_Target'
})

# 4. Add a weight (Value) so the extension knows how thick to make the lines
extension_prep['Weight'] = 1

# Save the file
extension_prep.to_csv('../data/sailor_sankey.csv', index=False)


