# Seat used car search script.

## Instructions
Install dependencies:

    python -m pip install -r requirements.txt

Do an advanced search on the approved used page here:
https://usedcars.seat.co.uk/en/used-cars/seat/model-search#searchmask

Copy the URL to the file `car_search_url` (the file should be a single line; no newline at the end).
For an example, see `car_search_url_example`.

Run the script `./update_cars.sh` periodically.

It will announce new cars, cars previously seen that are now gone, and previously gone cars that
have come back.

A CSV file of the current search results will be in `cars.csv`.

All the history is stored in `cars_history` so you will never completely lose a car even if it
disappears from the search results.

