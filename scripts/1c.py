# import pandas as pd

# # Load master file
# df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# # 1. Find the "Inner Circle": People who worked on Sailor Shift's songs
# # Get the IDs of all songs she performed
# ss_work_ids = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['id_target'].unique()

# # Get the names of everyone else who has a credit on those same songs
# inner_circle = df[(df['id_target'].isin(ss_work_ids)) & 
#                   (df['name_source'] != 'Sailor Shift')]['name_source'].unique()

# # 2. Trace the "Ripple Effect": What did these people do NEXT in Oceanus Folk?
# # Look for all songs in the 'Oceanus Folk' genre performed by her collaborators
# ripple_effect = df[(df['name_source'].isin(inner_circle)) & 
#                    (df['genre_target'] == 'Oceanus Folk') &
#                    (~df['id_target'].isin(ss_work_ids))].copy()

# # 3. Format for Tableau (The "Launchpad" Dataset)
# # We want to see: Collaborator -> Their Role -> Their Success outside Sailor Shift
# ripple_effect['Source_of_Influence'] = 'Sailor Shift'
# ripple_effect.to_csv('../data/sailor_ripple_effect.csv', index=False)




# BEFORE AFTER SAILOR COLLAB
import pandas as pd

# Load master file
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Create a clean 'year' column from release_date_target
# This takes the first 4 characters (e.g., "2014" from "2014-05-12")
df['year_clean'] = pd.to_numeric(df['release_date_target'].astype(str).str[:4], errors='coerce')

# 2. Identify Sailor Shift's work IDs
# We use id_target because it's the unique identifier for the song/album
ss_work_ids = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['id_target'].unique()

# 3. Identify the Collaborators and their FIRST year working with her
# (Everyone else credited on those same songs)
collaborator_credits = df[df['id_target'].isin(ss_work_ids) & (df['name_source'] != 'Sailor Shift')]

# Calculate the minimum year each collaborator appeared on a Sailor Shift track
first_collab_year = collaborator_credits.dropna(subset=['year_clean']).groupby('name_source')['year_clean'].min().reset_index()
first_collab_year.columns = ['name_source', 'first_ss_year']

# 4. Filter for all Oceanus Folk works by these specific collaborators
collab_names = first_collab_year['name_source'].unique()
# From your printout, 'genre_target' is the correct column name
all_collab_works = df[df['name_source'].isin(collab_names) & (df['genre_target'] == 'Oceanus Folk')].copy()

# 5. Merge the 'First Year' info back in to compare dates
all_collab_works = pd.merge(all_collab_works, first_collab_year, on='name_source')

# 6. Create the "Career Phase" Column
def determine_phase(row):
    if row['id_target'] in ss_work_ids:
        return 'With Sailor Shift'
    elif row['year_clean'] < row['first_ss_year']:
        return 'Before Collab'
    else:
        return 'After Collab'

# Drop rows without a valid year so we can do the math
all_collab_works = all_collab_works.dropna(subset=['year_clean'])
all_collab_works['Career_Phase'] = all_collab_works.apply(determine_phase, axis=1)

# 7. Save for Tableau
output_path = '../data/sailor_career_phases.csv'
all_collab_works.to_csv(output_path, index=False)

print(f"Success! Created {output_path}")
print("\nQuick Career Phase Count:")
print(all_collab_works['Career_Phase'].value_counts())


# COLLABORAOTRS CAREER

import pandas as pd

df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Clean the Year
df['Year'] = pd.to_numeric(df['release_date_target'].astype(str).str[:4], errors='coerce')

# 2. Get Sailor's Song IDs
ss_work_ids = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['id_target'].unique()

# 3. Get the SPECIFIC collaborator list (Matching your Script 1 logic)
credit_types = ['ComposerOf', 'ProducerOf', 'LyricistOf', 'PerformerOf'] # Added PerformerOf to get bandmates
collaborator_names = df[
    (df['id_target'].isin(ss_work_ids)) & 
    (df['Edge Type'].isin(credit_types)) & 
    (df['name_source'] != 'Sailor Shift') &
    (df['Node Type_source'] == 'Person') # This filters out Record Labels automatically
]['name_source'].unique()

# 4. TRACE FULL CAREERS (All roles, all genres)
# This finds every credit those people ever had
full_career_df = df[df['name_source'].isin(collaborator_names)].copy()

# 5. Create Categories for your Tooltip
full_career_df['Genre_Category'] = full_career_df['genre_target'].apply(
    lambda x: 'Oceanus Folk' if x == 'Oceanus Folk' else 'Other Genres'
)

# 6. Save
output_path = '../data/collaborator_careers.csv'
full_career_df.to_csv(output_path, index=False)