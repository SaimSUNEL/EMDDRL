import networkx as nx
import matplotlib.pyplot as plt
import pickle

from Environments import RLDDEnvironment, RLFourRoomsEnvironment, RLTwoRoomsEnvironment, RLPOMDPTwoRoomsEnvironment, RLPOMDPFourRoomsEnvironment, RLZigzagEnvironment, RLSampleEnvironment, RLSixRoomsEnvironment


G = nx.Graph()
graph_name = "DDRoom" # "ZigzagRoom" # "POMDPFourRoomsV4"



all_states = set()
two_rooms_env_v2 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment("v10",is_step_restricted=True,
                                                                step_limit=400)
four_rooms_env = RLFourRoomsEnvironment.RLFourRoomsEnvironment(is_step_restricted=True,
                                                                step_limit=200)
pomdp_two_rooms_env_3 = RLPOMDPTwoRoomsEnvironment.RLPOMDPTwoRoomsEnvironment('v3', is_step_restricted=False, step_limit=400)

pomdp_four_rooms_env_3 = RLPOMDPFourRoomsEnvironment.RLPOMDPFourRoomsEnvironment('v3', is_step_restricted=False, step_limit=400)
pomdp_four_rooms_env_4 = RLPOMDPFourRoomsEnvironment.RLPOMDPFourRoomsEnvironment('v4', is_step_restricted=False, step_limit=400)
zigzag_room_env = RLZigzagEnvironment.RLZigzagEnvironment("v0", is_step_restricted=True, step_limit=1000)
six_rooms_env = RLSixRoomsEnvironment.RLSixRoomsEnvironment("v0", is_step_restricted=True, step_limit=100)

sample_environment_v0 = RLSampleEnvironment.RLSampleEnvironment("v0", is_step_restricted=True, step_limit=1000)
sample_environment_v1 = RLSampleEnvironment.RLSampleEnvironment("v1", is_step_restricted=True, step_limit=1000)
dd_room_env_v0 = RLDDEnvironment.RLDDEnvironment("v0")


two_rooms_env_v2 = dd_room_env_v0 # zigzag_room_env
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

