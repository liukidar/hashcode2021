def load(fname):
	streets = []
	cars = []

	with open('./data/' + fname + '.txt') as f:
		i = 0
		for line in f:
			l = line.split()
			if i == 0:
				duration = int(l[0])
				intersections = int(l[1])
				street_nr = int(l[2])
				car_num = int(l[3])
				bonus = int(l[4])
			elif i < street_nr + 1:
				streets.append({
					"start": int(l[0]), 
					"end": int(l[1]), 
					"name": l[2],
					"time": int(l[3])
					})
			elif street_nr+1 <= i < street_nr + car_num + 1:
				cars.append({
					"nr": int(l[0]),
					"path": l[1:]
				})
			i += 1
			
	return duration, intersections, streets, cars, bonus

def test(fname):
	duration, intersections, streets, cars, bonus = load(fname)
	print('streets: {}'.format(streets))
	print('metadata: duration: {} intersections: {} bonus: {}'.format(duration, intersections, bonus))
	print('cars: {}'.format(cars))

if __name__ == '__main__':
	names = ["a", "b", "c", "d", "e", "f"]