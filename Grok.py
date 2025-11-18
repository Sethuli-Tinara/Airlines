import csv
from datetime import datetime, time as dtime
from graphics import *

# ================================
# GLOBALS
# ================================
window_start = dtime(0, 0)
window_end = dtime(12, 0)

data_list = []   # Main data container

defined_airport_codes = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Bajaras",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International"
}

defined_airlines = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}

# Initial empty dictionary for histogram counting
flights_per_hour = {hour: 0 for hour in range(12)}

# ================================
# CSV LOADING
# ================================
def load_csv_(CSV_chosen):
    data_list.clear()
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)

# ================================
# FUNCTIONS
# ================================
def count_flights_and_rain_hours(data_list):
    total_departure_flights_12hr = 0
    rainy_hours = set()

    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            if window_start <= dep_time < window_end:
                total_departure_flights_12hr += 1
                if "rain" in row[10].lower():
                    rainy_hours.add(dep_time.hour)
        except:
            continue

    return total_departure_flights_12hr, rainy_hours


def count_two_terminal_flights(data_list):
    total_departure_T2 = 0
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            if int(row[8]) == 2 and window_start <= dep_time < window_end:
                total_departure_T2 += 1
        except:
            continue
    return total_departure_T2


def count_Air_France_flights(data_list):
    total_AF_airline_flights = 0
    delayed_AF_flights = 0

    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            airline = row[1][:2]
            if airline == "AF" and window_start <= dep_time < window_end:
                total_AF_airline_flights += 1
                if row[2] != row[3]:
                    delayed_AF_flights += 1
        except:
            continue
    return total_AF_airline_flights, delayed_AF_flights


def count_flights_under_15_degrees(data_list):
    total_flights_temp = 0
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            temperature = int(row[10][0:2])
            if temperature < 15 and window_start <= dep_time < window_end:
                total_flights_temp += 1
        except:
            continue
    return total_flights_temp


def count_flights_under_600_miles(data_list):
    total_flights_under_600 = 0
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            if int(row[5]) < 600 and window_start <= dep_time < window_end:
                total_flights_under_600 += 1
        except:
            continue
    return total_flights_under_600


def count_least_common_destinations(data_list, defined_airport_codes):
    count_of_destinations = {}

    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            destination = row[4]

            if window_start <= dep_time < window_end and destination in defined_airport_codes:
                count_of_destinations[destination] = count_of_destinations.get(destination, 0) + 1

        except:
            continue

    if not count_of_destinations:
        return []

    least_common_count = min(count_of_destinations.values())

    least_common_destinations = [
        defined_airport_codes[d]
        for d, count in count_of_destinations.items()
        if count == least_common_count
    ]

    return least_common_destinations


def count_airline_flights(data_list):
    total_BA_airline_flights = 0
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            airline = row[1][:2]
            if airline == "BA" and window_start <= dep_time < window_end:
                total_BA_airline_flights += 1
        except:
            continue
    return total_BA_airline_flights


def count_flights_per_airline_by_hour(data_list, airline_code):
    flights_per_hour.update({h: 0 for h in range(12)})  # reset

    if airline_code not in defined_airlines:
        print("Invalid airline code.")
        return flights_per_hour

    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            if airline_code == row[1][:2] and window_start <= dep_time < window_end:
                flights_per_hour[dep_time.hour] += 1
        except:
            continue

    return flights_per_hour


# ================================
# HISTOGRAM (MERGED + IMPROVED)
# ================================
def draw_histogram(airline_code, airport_code, year, flights_dict):
    try:
        airline_name = defined_airlines.get(airline_code, airline_code)
        airport_name = defined_airport_codes.get(airport_code, airport_code)

        win = GraphWin("Histogram", 1200, 800)
        win.setCoords(0,0, 100, 100)
        win.setBackground(color_rgb(245, 255, 240))

        # Title
        title = f"Departures by hour for {airline_name} from {airport_name} {year}"
        title_obj = Text(Point(50, 95), title)
        title_obj.setSize(14)
        title_obj.setStyle("bold")
        title_obj.draw(win)

        max_count = max(flights_dict.values()) if max(flights_dict.values()) > 0 else 1
        scale = 70 / max_count  # bar length scaling

        start_y = 80
        step_y = 6
        current_y = start_y

        # Y-axis label block
        y_label = Text(Point(10, start_y + 5), "Hours\n00:00\nto\n12:00")
        y_label.setSize(10)
        y_label.setTextColor("gray")
        y_label.draw(win)

        # Bars
        for hour in range(12):
            count = flights_dict[hour]
            length = count * scale

            # Hour label
            hour_label = Text(Point(18, current_y + 1.5), f"{hour:02d}")
            hour_label.draw(win)

            # Bar rectangle
            bar = Rectangle(Point(22, current_y), Point(22 + length, current_y + 3))
            bar.setFill(color_rgb(255, 180, 180))
            bar.setOutline("gray")
            bar.draw(win)

            # Count value at end of bar
            count_label = Text(Point(24 + length, current_y + 1.5), str(count))
            count_label.draw(win)

            current_y -= step_y

        win.getMouse()
        win.close()

    except GraphicsError:
        pass


# ================================
# MAIN PROGRAM
# ================================
def main():
    while True:
        city_code = input("Enter 3-letter city code: ").upper()
        if city_code in defined_airport_codes:
            break
        print("Invalid code. Try again.")

    while True:
        try:
            year = int(input("Enter year (2000–2025): "))
            if 2000 <= year <= 2025:
                year = str(year)
                break
            else:
                print("Out of range.")
        except ValueError:
            print("Invalid input.")

    filename = f"{city_code}{year}.csv"
    print("*" * 50)
    print(f"File {filename} selected – Planes departing {defined_airport_codes[city_code]} {year}")
    print("*" * 50)

    load_csv_(filename)

    # Compute values
    total_departure_flights, rainy_hours = count_flights_and_rain_hours(data_list)
    total_departure_T2 = count_two_terminal_flights(data_list)
    total_flights_under_600 = count_flights_under_600_miles(data_list)
    total_AF_airline_flights, delayed_AF_flights = count_Air_France_flights(data_list)
    total_flights_temp = count_flights_under_15_degrees(data_list)
    total_BA_airline_flights = count_airline_flights(data_list)
    least_common_destinations_full_form = count_least_common_destinations(data_list, defined_airport_codes)

    # Display results
    print(f"Total departures: {total_departure_flights}")
    print(f"Terminal 2 departures: {total_departure_T2}")
    print(f"Flights under 600 miles: {total_flights_under_600}")
    print(f"Air France flights: {total_AF_airline_flights}")
    print(f"Delayed AF flights: {delayed_AF_flights}")
    print(f"Under 15 degrees: {total_flights_temp}")
    print(f"Least common destination(s): {least_common_destinations_full_form}")

    # Histogram
    airline_code = input("Enter airline code for histogram: ").upper()
    hourly_counts = count_flights_per_airline_by_hour(data_list, airline_code)
    draw_histogram(airline_code, city_code, year, hourly_counts)


if __name__ == "__main__":
    main()

    while True:
        choice = input("Select new file? (Y/N): ").lower()
        if choice == "y":
            main()
        elif choice == "n":
            print("Thank you. End of run.")
            break
        else:
            print("Invalid. Enter Y or N only.")
