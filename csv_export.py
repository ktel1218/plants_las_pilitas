import csv
from scraper import get_all_plants
import copy
from pprint import pprint



def expand(obj):
    copy = obj.copy()
    for k, v in obj.iteritems():
        if isinstance(v, list) and len(v) == 2:
            low, high = v
            copy[k + "_low"] = low
            copy[k + "_high"] = high
            del copy[k]
    return copy


def write(objs):
    with open('plants.csv', 'w') as csvfile:
        pilot = expand(plants[0])
        fieldnames = sorted(pilot.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for plant in plants:
            try:
                writer.writerow(expand(plant))
            except ValueError:
                continue


if __name__ == "__main__":
    plants = get_all_plants()
    write(plants)