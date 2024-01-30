import networkx as nx
import matplotlib.pyplot as plt
import pickle

from Environments import RLFourRoomsEnvironment, RLTwoRoomsEnvironment


G = nx.Graph()
graph_name = "TwoRoomv2"

all_states = set()
two_rooms_env_v2 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment("v10",is_step_restricted=True,
                                                                step_limit=400)
four_rooms_env = RLFourRoomsEnvironment.RLFourRoomsEnvironment(is_step_restricted=True,
                                                                step_limit=200)



environment_adjacency_dict  = two_rooms_env_v2.getEnvironmentGraph()
for node in environment_adjacency_dict:
    neighbors = environment_adjacency_dict[node]
    G.add_node(node)
    all_states.add(node)
    for neighbor in neighbors:
        print("neighbor : ", neighbor)
        G.add_edge(node, neighbor)
        all_states.add(neighbor)
# plt.subplot(121)
options = {
     'node_color': 'white',
     'node_size': 600,
     'width': 5,
     "font_size": 15,
    "edge_color": "red",
"font_color": "green"}
# pos = nx.nx_agraph.pygraphviz_layout(G)
# nx.draw(G, pos=pos, with_labels=True, **options)
# plt.show()

# print(nx.shortest_path_length(G, 1, 209))
distance_dict = {}


for source in all_states:
    print("Source : ", source)
    distance_dict[source] = {}
    for target in all_states:
        distance_dict[source][target] = nx.shortest_path_length(G, source, target)






pickle.dump(G, open(graph_name+".pck", "wb"))
pickle.dump(distance_dict, open(graph_name+"DistanceDict"+".pck", "wb"))
print("Graph saved...")

