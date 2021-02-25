from loader import load
from collections import Counter


def prepass(fname):
    duration, intersections, streets, cars, bonus = load(fname)

    res = []

    for street in streets:
        res.append(street["name"])

    for car in cars:
        for street in car['path']:
            res.append(street)

    return dict(Counter(res))


def snapshot(fname):
    duration, intersections, streets, cars, bonus = load(fname)

    res = {}
    for street in streets:
        res[street['name']] = 0

    for car in cars:
        res[car['path'][0]] += 1

    return res


def restriction(streets, cars, start_time=0, end_time=100):
    times = {s["name"]: s["time"] for s in streets}
    car_timestamps = []
    for car in cars:
        current_time = 0
        car_timestamps.append({})
        for i in range(len(car["path"])):
            if i >= 1:
                current_time += times[car["path"][i]]
            car_timestamps[-1][current_time] = car["path"][i] 
    
    for i in range(len(car_timestamps)):
        car_timestamps[i] = {k: v for k, v in car_timestamps[i].items() if start_time < k < end_time}
    
    return car_timestamps

if __name__ == '__main__':
    duration, intersections, streets, cars, bonus = load("a")
    print(restriction(streets, cars, 0, 6))
