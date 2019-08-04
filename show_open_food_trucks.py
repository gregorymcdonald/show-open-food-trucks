import requests
import sys
from datetime import datetime, time
from typing import List

class FoodTruck:
    """
    Class representing a food truck at a specific location and time, 
    i.e. an entry in the mobile food schedule.

    Attributes:
        address     the location of the food truck, e.g. '3119 ALEMANY BLVD'.
        name        the name of the food truck, e.g. 'San Pancho's Tacos'.
        dayOfWeek   the day of the week the food truck is open, e.g. 'Tuesday'.
        openTime    the time that the food truck first opens, e.g. '15:00'.
        closeTime   the time that the food truck closes, e.g. '23:00'.
    """

    def __init__(self, address: str, name: str, dayOfWeek: str, openTime: str, closeTime: str):
        self.address = address      # type: str
        self.name = name            # type: str
        self.dayOfWeek = dayOfWeek  # type: str
        self.openTime = openTime    # type: str
        self.closeTime = closeTime  # type: str

    @classmethod
    def from_json(cls, json):
        """
        Create a food truck from the specified JSON object.
        :return: A FoodTruck if the specified JSON object is well-formed; otherwise, None.
        """
        # Get all fields from the input JSON.
        address = json.get('location')
        foodTruckName = json.get('applicant')
        dayOfWeek = json.get('dayofweekstr')
        openTime = json.get('start24')
        closeTime = json.get('end24')
        return cls(address, foodTruckName, dayOfWeek, openTime, closeTime)

    def __str__(self) -> str:
        """
        Returns the string representation of this food truck.
        """
        return f'{self.name} {self.address}'

    def is_open(self, date: datetime) -> bool:
        """
        Returns True if this mobile food schedule entry is open (i.e. doing business)
        at the specified datetime. Returns False if this mobile food schedule entry is
        closed at the specified datetime.
        """
        # Parses the hours and minutes component from the open and close times.
        open_hour = int(self.openTime[0:2])
        open_minute = int(self.openTime[3:])
        close_hour = int(self.closeTime[0:2])
        close_minute = int(self.closeTime[3:])

        # True if the specified date is on the same day as this food truck's schedule.
        sameDay = date.strftime('%A') == self.dayOfWeek
        # True if the specified time is at or after the food truck's open.
        afterOpen = date.hour > open_hour or (date.hour == open_hour and date.minute >= open_minute)
        # True if the specified time is at or before the food truck's close.
        beforeClose = date.hour < close_hour or (date.hour == close_hour and date.minute <= close_minute)
        return sameDay and afterOpen and beforeClose


def get_food_trucks() -> List[FoodTruck]:
    """
    Returns all food truck mobile food schedule entries.
    """
    # Issues a GET request to DataSF government mobile food schedule dataset.
    datasf_mobile_food_schedule_url = "http://data.sfgov.org/resource/bbb8-hzi6.json"
    mobile_food_schedule_response = requests.get(datasf_mobile_food_schedule_url)

    if mobile_food_schedule_response.status_code == 200:
        # Get the response data as JSON.
        mobile_food_schedule_json = mobile_food_schedule_response.json()

        # Iterate through the JSON data and create a food truck for each entry.
        food_trucks = []
        for entry in mobile_food_schedule_json:
            food_truck = FoodTruck.from_json(entry)
            food_trucks.append(food_truck)

        return food_trucks
    else:
        raise Exception(f'GET request for {datasf_mobile_food_schedule_url} responded \
                      with status code {mobile_food_schedule_response.status_code}.')


def main() -> None:
    """
    The entry point of the program.
    """
    try:
        # Load ALL food trucks.
        food_trucks = get_food_trucks()
    except:
        print('An error occurred loading food truck data. Program will now exit.', flush=True)
        sys.exit(1)
   
    # Get all food trucks that are open at the current time.
    # NOTE: perform tests by changing current_time to the desired time like:
    # datetime.strptime('Monday 08:50', '%A %H:%M').
    current_time = datetime.now()
    open_food_trucks = [f for f in food_trucks if f and f.is_open(current_time)]

    # Handle the case where there are no open food trucks.
    if len(open_food_trucks) == 0:
        print('There are currently no open food trucks.', flush=True)
        sys.exit(0)

    # Sort the food trucks alphabetically by name.
    open_food_trucks.sort(key=lambda f: f.name)

    # Print food trucks in groups of 10.
    current_food_truck_index = 0
    while current_food_truck_index < len(open_food_trucks):
        print(open_food_trucks[current_food_truck_index])
        current_food_truck_index += 1

        # After 10 food trucks are printed, block until the user presses 
        # the Enter key (unless there are no more food trucks).
        if current_food_truck_index % 10 == 0 and current_food_truck_index != len(open_food_trucks):
            input('Press Enter to view more food trucks...')


if __name__ == '__main__':
    main()
        