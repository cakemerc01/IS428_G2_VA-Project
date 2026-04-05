# CONTRIBUTORS OF SONGS SAILOR PERFORMED

import pandas as pd

# Load your master file
# Added low_memory=False to handle the mixed-type warning you saw earlier
df = pd.read_csv('../data/mc1_1a.csv', low_memory=False)

# 1. Identify the target IDs of all works performed by Sailor Shift
her_performed_ids = df[(df['name_source'] == 'Sailor Shift') & (df['Edge Type'] == 'PerformerOf')]['id_target'].unique()

# 2. Define only individual creator credit types (Removed RecordedBy)
credit_types = ['ComposerOf', 'ProducerOf', 'LyricistOf']

# 3. Find the credits for these specific works
# This now only captures the humans (Composers, Producers, Lyricists)
credits_df = df[(df['id_target'].isin(her_performed_ids)) & (df['Edge Type'].isin(credit_types))].copy()

# 4. Add a column for easier filtering in Tableau
credits_df['Main Artist'] = 'Sailor Shift'

# Save the file
output_path = '../data/sailor_credits.csv'
credits_df.to_csv(output_path, index=False)


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




# SAILOR EGO NETWORK
# Load your master file
df = pd.read_csv('../data/mc1_1a.csv')

# 1. Find all rows where Sailor Shift is either the source or the target
# This captures everything she is DIRECTLY connected to (Degree 1)
ego_edges = df[(df['name_source'] == 'Sailor Shift') | (df['name_target'] == 'Sailor Shift')].copy()

# 2. Extract the unique names of all connected nodes
# If she is the source, the connection is the target; if she is target, the connection is the source.
connections = []
for index, row in ego_edges.iterrows():
    if row['name_source'] == 'Sailor Shift':
        connections.append({'Name': row['name_target'], 'Type': row['Node Type_target'], 'Edge': row['Edge Type']})
    else:
        connections.append({'Name': row['name_source'], 'Type': row['Node Type_source'], 'Edge': row['Edge Type']})

# Remove duplicates (a node might be connected via multiple edges)
connections_df = pd.DataFrame(connections).drop_duplicates(subset=['Name'])
unique_connections = connections_df['Name'].tolist()

# 3. Calculate Coordinates (Sailor Shift at center 0,0)
plot_data = []
center_name = "Sailor Shift"

# Circle points for connections
num_conn = len(unique_connections)
for i, name in enumerate(unique_connections):
    angle = (2 * math.pi * i) / num_conn
    # Radius of 1 for the circle
    x = math.cos(angle)
    y = math.sin(angle)
    
    # Get the type and edge for this specific connection
    c_info = connections_df[connections_df['Name'] == name].iloc[0]
    
    # Row for the center (Start of line)
    plot_data.append({
        'NodeName': center_name, 'PartnerName': name, 
        'X': 0, 'Y': 0, 'LineID': name, 'NodeType': 'Artist', 'EdgeType': c_info['Edge']
    })
    # Row for the connection (End of line)
    plot_data.append({
        'NodeName': name, 'PartnerName': name, 
        'X': x, 'Y': y, 'LineID': name, 'NodeType': c_info['Type'], 'EdgeType': c_info['Edge']
    })

final_ego_df = pd.DataFrame(plot_data)
final_ego_df.to_csv('../data/sailor_ego_network.csv', index=False)