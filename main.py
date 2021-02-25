from loader import load
from prepass import *
from tree import Graph
import math

names = ["a", "b", "c", "d", "e", "f"]

if __name__ == "__main__":
	for name in names:
		duration, intersections, streets, cars, bonus = load(name)
		weights = prepass(name)
		initials = snapshot(name)
		g = Graph(intersections, streets, weights, initials, int(intersections))
		g.update()
		g.output()
		g.output_final(name)