import pandas as pd
import math

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

