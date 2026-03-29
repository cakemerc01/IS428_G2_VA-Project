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


# MUSICAL GROUP

import pandas as pd
import math

# Load your master file
df = pd.read_csv('../data/mc1_1a.csv')

# 1. Find the group and members
her_groups = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'MemberOf')]['name_target'].unique()
members_df = df[(df['name_target'].isin(her_groups)) & (df['Edge Type'] == 'MemberOf')].copy()

# 2. Create a list of unique Nodes (The Group + The Artists)
nodes = list(members_df['name_source'].unique()) + list(members_df['name_target'].unique())
nodes = list(set(nodes)) # Remove duplicates

# 3. Calculate X and Y coordinates (Circular Layout)
# We place the Group (Ivy Echos) at the center (0,0) 
# and the members around it.
plot_data = []
center_node = "Ivy Echos"
members = [n for n in nodes if n != center_node]

# Center point
plot_data.append({'Name': center_node, 'X': 0, 'Y': 0, 'Type': 'Group'})

# Circle points
for i, member in enumerate(members):
    angle = (2 * math.pi * i) / len(members)
    x = math.cos(angle)
    y = math.sin(angle)
    plot_data.append({'Name': member, 'X': x, 'Y': y, 'Type': 'Artist'})

coords_df = pd.DataFrame(plot_data)

# 4. Create the "Links" table for Tableau
# Tableau needs two rows for every line (Start point and End point)
links = []
for member in members:
    # Row for the Group (Start of line)
    links.append({'Artist': member, 'Group': center_node, 'X': 0, 'Y': 0, 'LineID': member})
    # Row for the Artist (End of line)
    member_coords = coords_df[coords_df['Name'] == member]
    links.append({
        'Artist': member, 
        'Group': center_node, 
        'X': member_coords['X'].values[0], 
        'Y': member_coords['Y'].values[0], 
        'LineID': member
    })

final_network = pd.DataFrame(links)
final_network.to_csv('../data/sailor_network_with_coords.csv', index=False)