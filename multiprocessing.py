import json
import numpy as np

class Process:
	def __init__(self, _metadata, _data, _process):
		self.metadata = _metadata
		self.data = _data
		self.results = []
		self.process = _process

	def run(self, _n):
		for i in range(_n):
			self.results.append(self.process(self.metadata, self.data))

	def save(self, _output="random.json"):
		with open(_output, "r") as f:
			data = json.load(f)
			data["results"].append(self.results)

		with open(_output, "w") as f:
			json.dump(data, f)

a = np.array([1,2])
b = np.array([1,2])

def fn(a,b):
	return 1

p = Process(a,b, fn)
p.run(10)
p.save()