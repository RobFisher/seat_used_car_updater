#!/bin/bash

if [ -f cars.csv ]; then
    cat cars.csv >> cars_history.csv
fi

URL=$(cat car_search_url)

wget "$URL" -O cars.html
python3 read_cars.py > cars.csv

