import csv

def read_from_file(filename):
    with open(filename, 'r') as csvfile:
        list_of_data = []
        data = csv.reader(csvfile)
        for row in data:
            list_of_data.append(row)
    return list_of_data
def read_from_dict_file(filename, fieldnames):
    with open(filename, 'r') as csvfile:
        list_of_data = []
        data = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in data:
            list_of_data.append(row)
    return list_of_data
def write_to_file(filename):
def write_to_dict_file(filename, fieldnames):
def append_to_file(filename):
def append_to_dict_file(filename, fieldnames):