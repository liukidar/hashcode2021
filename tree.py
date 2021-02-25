from loader import load
from prepass import prepass
import networkx as nx
import numpy as np

epsilon = 0.0001
# balanced????
def softmax_mul(vector, mul):
	vector = np.array(vector) + epsilon
	res = vector / vector.sum() * mul
	return res

class Graph:
	# streets: ["time"]
	def __init__(self, intersections, streets, street_weigths, street_initials, n):
		self.street_initials = street_initials
		self.edges_tv = {}
		self.edges_tv_other_time = {}
		self.edges_final = {}
		self.nodes_tv = {}
		self.edges_by_name = {} # name => (start, end)
		self.edges_by_se = {} # (start, end) => name 
		self.edges_weight = {}
		self.n = n
		
		self.g = nx.DiGraph()
		self.g.add_nodes_from(range(intersections))

		for i in range(intersections):
			self.nodes_tv[i] = 0

		for street in streets:
			self.g.add_edge(street["start"], street["end"])
			self.edges_by_name[street["name"]] = (street["start"], street["end"])
			self.edges_by_se[(street["start"], street["end"])] = street["name"]
		
		# macchine complessive
		for key, value in street_weigths.items():
			self.edges_weight[self.edges_by_name[key]] = value

		# macchine all'inizio
		for key, value in street_initials.items():
			self.edges_tv[self.edges_by_name[key]] = value
			self.edges_tv_other_time[self.edges_by_name[key]] = []

	def update_to_nodes(self):
		for node in self.nodes_tv.keys():
			edges = self.g.in_edges(node)
			tvalue = 0
			for edge in edges:
				tvalue += self.edges_tv[tuple(edge)]

			self.nodes_tv[node] = tvalue

	def update_to_edges(self):		
		for node in self.nodes_tv.keys():
			edges = self.g.out_edges(node)
			edges_tv = list(softmax_mul([self.edges_weight[e] for e in edges], self.nodes_tv[node]))
			for edge, edge_tv in zip(edges, edges_tv):
				v = edge_tv
				self.edges_tv[tuple(edge)] = v
				self.edges_tv_other_time[tuple(edge)].append(v)

	def update(self):
		for i in range(self.n):
			self.update_to_nodes()
			self.update_to_edges()
			
	def output(self):
		for node in self.nodes_tv.keys():
			edges_in = self.g.in_edges(node)
			edges_ratio = np.zeros((self.n, len(edges_in)))
			for step in range(self.n):
				l = [self.edges_tv_other_time[tuple(edge)][step] for edge in edges_in]
				edges_value = softmax_mul(l, 1)
				edges_ratio[step] = edges_value

			edges_ratio = edges_ratio.mean(axis=0) + epsilon
			min_value = 1.0 / np.min(edges_ratio)
			edges_ratio = np.round(softmax_mul(edges_ratio, min_value)).astype(int) # / min
			for i, edge in enumerate(edges_in):
				self.edges_final[edge] = edges_ratio[i]

		
	def output_final(self, fname):
		n_intersections_considered = len(self.nodes_tv.keys())
		node_street_timers = []
		for node in self.nodes_tv.keys():
			street_timers = {}

			edges_in = self.g.in_edges(node)
			for edge in edges_in:
				street_timers[self.edges_by_se[tuple(edge)]] = self.edges_final[edge] + 1

			node_street_timers.append(street_timers)

		with open('./output/' + fname + '.txt', 'w') as f:
			f.write(str(n_intersections_considered) + '\n')

			for node in self.nodes_tv.keys():
				f.write(str(node) + '\n')
				f.write(str(len(node_street_timers[node])) + '\n')
				for edge in node_street_timers[node]:
					f.write(edge + ' ' + str(node_street_timers[node][edge]) + '\n')
			