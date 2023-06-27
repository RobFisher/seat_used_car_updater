import sys
from bs4 import BeautifulSoup

# paste your HTML here
with open('cars.html', 'r') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

# create a list to hold all vehicles
vehicles = []

def is_new_car(vehicle_id):
    # path to the file where IDs of seen cars are stored
    seen_cars_file_path = "seen_cars.txt"
    try:
        with open(seen_cars_file_path, "r") as file:
            seen_car_ids = file.read().splitlines()
    except FileNotFoundError:
        seen_car_ids = []

    if vehicle_id not in seen_car_ids:
        # this is a new car, add its ID to the file
        with open(seen_cars_file_path, "a") as file:
            file.write(vehicle_id + "\n")
        return True
    else:
        return False


def print_changed_availability_cars(vehicles):
    last_seen_cars_file_path = "last_seen_cars.txt"
    ids = [ v['id'] for v in vehicles ]
    try:
        with open(last_seen_cars_file_path, "r") as f:
            last_seen_cars = f.read().splitlines()
    except FileNotFoundError:
        last_seen_cars = []

    for id in last_seen_cars:
        if id not in ids:
            print(f'Car {id} is gone!', file=sys.stderr)

    for id in ids:
        if id not in last_seen_cars and not is_new_car(id):
            print(f'Car {id} is back again!', file=sys.stderr)

    with open(last_seen_cars_file_path, "w") as f:
        for id in ids:
            f.write(f'{id}\n')


new_cars = ''

# find all articles (each one represents a vehicle)
for article in soup.find_all('article'):
    # create a dictionary to hold this vehicle's data
    vehicle = {}
    
    # extract data
    id = article.get('id')
    vehicle['id'] = id
    if is_new_car(id):
        new_cars += id + '\n'

    vehicle['link'] = article.get('data-link')
    vehicle['title'] = article.find(class_='vehicle__title-model').text
    vehicle['description'] = article.find(class_='vehicle__details-subline').text
    vehicle['dealer_name'] = article.find(class_='vehicle__dealer-name').text
    vehicle['dealer_distance'] = article.find(class_='vehicle__dealer-distance').text
    vehicle['price'] = article.find(class_='price__value').text.strip().replace('£', '').replace(',', '')


    # extract vehicle specifications
    for li in article.find_all('li'):
        title = li.get('title')
        if title:
            value = li.find(class_='list-value')
            if value:
                t = value.text
                vehicle[title.lower()] = t

    if 'mileage' in vehicle:
        vehicle['mileage'] = vehicle['mileage'].replace(',', '')

    # add this vehicle to the list
    vehicles.append(vehicle)

# print out in CSV format
print('id,link,title,description,dealer_name,dealer_distance,price,mileage,fuel,registered,transmission,previous owners')
for vehicle in vehicles:
    print(f"{vehicle.get('id')},{vehicle.get('link')},{vehicle.get('title')},{vehicle.get('description')},{vehicle.get('dealer_name')},{vehicle.get('dealer_distance')},{vehicle.get('price')},{vehicle.get('mileage')},{vehicle.get('fuel')},{vehicle.get('registered')},{vehicle.get('transmission')},{vehicle.get('previous owners')}")

if len(new_cars) > 0:
    print('New cars found!\n' + new_cars, file=sys.stderr)

print_changed_availability_cars(vehicles)

