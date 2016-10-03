import json, math


def load_data(filepath='Бары.json'):
    with open(filepath) as data_file:
        data = json.load(data_file)
    return data


def get_biggest_bar(data):
    max = (data[0]['Cells']['Name'], data[0]['Cells']['SeatsCount'])
    for json_object in data:
        if max[1] < json_object['Cells']['SeatsCount']:
            max = (json_object['Cells']['Name'], json_object['Cells']['SeatsCount'])
    print('The largest place is "%s"' % max[0])


def get_smallest_bar(data):
    min = (data[0]['Cells']['Name'], data[0]['Cells']['SeatsCount'])
    for json_object in data:
        if min[1] > json_object['Cells']['SeatsCount']:
            min = (json_object['Cells']['Name'], json_object['Cells']['SeatsCount'])
    print('The smallest place is "%s"' % min[0])


def get_closest_bar(data, longitude, latitude):
    def distance(f1, f2, l1, l2):
        R = 6.371

        f1 = math.radians(f1)
        f2 = math.radians(f2)
        df = math.radians(f2 - f1)
        dl = math.radians(l2 - l1)

        a = math.sin(df/2)**2 + math.cos(f1)*math.cos(f2)*(math.sin(dl/2)**2)
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R*c

    nearest = {'name': data[0]['Cells']['Name'],
           'dist': distance(
               latitude,
               float(data[0]['Cells']['geoData']['coordinates'][0]),
               longitude,
               float(data[0]['Cells']['geoData']['coordinates'][1]),
           ),
           }

    for json_object in data:
        if nearest['dist'] > distance(latitude, float(json_object['Cells']['geoData']['coordinates'][0]), longitude, float(json_object['Cells']['geoData']['coordinates'][1])):
            nearest['name'] = json_object['Cells']['Name']
            nearest['dist'] = distance(latitude, float(json_object['Cells']['geoData']['coordinates'][0]), longitude, float(json_object['Cells']['geoData']['coordinates'][1]))

    print('The nearest place is "%s"' % nearest['name'])

if __name__ == '__main__':
    print('Enter the path to the file:')
    i = input()
    if i == '':
        data = load_data()
    else:
        data = load_data(i)

    get_biggest_bar(data)
    get_smallest_bar(data)

    print('Enter the latitude:')
    latitude = float(input())
    print('Enter the longitude:')
    longitude = float(input())
    get_closest_bar(data, longitude, latitude)
