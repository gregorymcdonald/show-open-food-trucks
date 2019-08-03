import requests
import sys
from datetime import datetime, time

class MobileFoodScheduleEntry:
    """
    Class representing an entry in the mobile food schedule.
    """

    def __init__(self, address: str, name: str, dayOfWeek: str, startTime: str, endTime: str):
        self.address = address # type: str
        self.name = name # type: str
        self.dayOfWeek = dayOfWeek # type: str
        self.startTime = startTime # type: str
        self.endTime = endTime # type: str

    def __str__(self):
        """
        Returns the string representation of this mobile food schedule entry.
        """
        return f'{self.name} {self.address}'

    def is_open(self, date: datetime) -> bool:
        """
        Returns True if this mobile food schedule entry is open (i.e. doing business)
        at the specified datetime. Returns False if this mobile food schedule entry is
        closed at the specified datetime.
        """
        start_hour = int(self.startTime[0:2])
        start_minute = int(self.startTime[3:])
        end_hour = int(self.endTime[0:2])
        end_minute = int(self.endTime[3:])
        return date.strftime('%A') == self.dayOfWeek \
               and (date.hour > start_hour or (date.hour == start_hour and date.minute >= start_minute)) \
               and (date.hour < end_hour or (date.hour == end_hour and date.minute <= end_minute))


def create_food_truck_from_json(json):
    address = json['location']
    foodTruckName = json['applicant']
    dayOfWeek = json['dayofweekstr']
    return MobileFoodScheduleEntry(address, foodTruckName, dayOfWeek, json['start24'], json['end24'])


def get_food_trucks():
    datasf_mobile_food_schedule_url = "http://data.sfgov.org/resource/bbb8-hzi6.json"
    mobile_food_schedule_response = requests.get(datasf_mobile_food_schedule_url)
    if mobile_food_schedule_response.status_code == 200:
        mobile_food_schedule_json = mobile_food_schedule_response.json()
        food_trucks = []
        for i in range(0, len(mobile_food_schedule_json)):
            food_truck = create_food_truck_from_json(mobile_food_schedule_json[i])
            food_trucks.append(food_truck)
        return food_trucks
    else:
        raise RuntimeError(f'GET request for {datasf_mobile_food_schedule_url} responded \
                      with status code {mobile_food_schedule_response.status_code}.')


def main() -> None:
    """
    The entry point of the program if this module is executed.
    """
    try:
        # Load ALL food trucks.
        food_trucks = get_food_trucks()
    except:
        print('An error occurred loading food truck data. Program will now exit.', flush=True)
        sys.exit(1)
   
    # Get all food trucks that are open at the current time.
    current_time = datetime.now()
    open_food_trucks = [f for f in food_trucks if f.is_open(current_time)]

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

        # After 10 food trucks are printed, block until the user presses Enter.
        if current_food_truck_index % 10 == 0:
            input('Press Enter to view more food trucks...')


if __name__ == '__main__':
    # Parse command line arguments.

    main()
        