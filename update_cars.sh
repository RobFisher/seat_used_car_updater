#!/bin/bash

URL=$(cat car_search_url)

wget "$URL" -O cars.html
python3 read_cars.py > cars.csv

echo $(date --iso-8601=minutes) >> cars_history
cat cars.csv >> cars_history

