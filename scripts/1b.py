import pandas as pd

# Load your master file
df = pd.read_csv('../data/mc1_1a.csv')

# 1. Identify the target IDs of all works performed by Sailor Shift
her_performed_ids = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['id_target'].unique()

# 2. Define the credit types (Added RecordedBy here)
# RecordedBy usually points to the Record Label
credit_types = ['ComposerOf', 'ProducerOf', 'LyricistOf', 'RecordedBy']

# 3. Find the credits and labels for these specific works
credits_df = df[(df['id_target'].isin(her_performed_ids)) & (df['Edge Type'].isin(credit_types))].copy()

# 4. Add a column for easier filtering in Tableau
credits_df['Main Artist'] = 'Sailor Shift'

# Save the file
credits_df.to_csv('../data/sailor_credits.csv', index=False)