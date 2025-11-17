import csv
from datetime import datetime, time
import graphics

# === Global Constants ===
window_start = time(0, 0)   # 00:00
window_end = time(12, 0)    # 12:00 (not including 12:00)

# === Dictionaries ===
defined_airport_codes = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas",
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

# === Global data list (cleared each loop) ===
data_list = []


def load_csv_file(filename):
    """
    Load CSV file into global data_list. Clears previous data.
    """
    global data_list
    data_list.clear()
    try:
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                if len(row) >= 11:  # Ensure row has all columns
                    data_list.append(row)
    except FileNotFoundError:
        print(f"Error: {filename} not found in directory.")
        return False
    except Exception as e:
        print(f"Error loading file: {e}")
        return False
    return True


def get_valid_airport_code():
    """Prompt and validate 3-letter airport code."""
    while True:
        code = input("Please enter a three-letter city code: ").strip().upper()
        if len(code) != 3:
            print("Wrong code length - please enter a three-letter city code")
            continue
        if code not in defined_airport_codes:
            print("Unavailable city code - please enter a valid city code")
            continue
        return code


def get_valid_year():
    """Prompt and validate year between 2000 and 2025."""
    while True:
        year_input = input("Please enter the year required in the format YYYY: ").strip()
        if not year_input.isdigit() or len(year_input) != 4:
            print("Wrong data type - please enter a four-digit year value")
            continue
        year = int(year_input)
        if not (2000 <= year <= 2025):
            print("Out of range - please enter a value from 2000 to 2025")
            continue
        return str(year)


def count_flights_and_rain_hours():
    """Count total flights and hours with rain."""
    total_flights = 0
    rain_hours = set()
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            if window_start <= dep_time < window_end:
                total_flights += 1
                if "rain" in row[10].lower():
                    rain_hours.add(dep_time.hour)
        except:
            continue
    return total_flights, len(rain_hours)


def count_terminal_2_flights():
    """Count flights from Terminal 2."""
    count = 0
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            if window_start <= dep_time < window_end and row[8] == "2":
                count += 1
        except:
            continue
    return count


def count_under_600_miles():
    """Count flights under 600 miles."""
    count = 0
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            if window_start <= dep_time < window_end and int(row[5]) < 600:
                count += 1
        except:
            continue
    return count


def count_air_france_flights():
    """Count total and delayed Air France flights."""
    total = delayed = 0
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            airline = row[1][:2].upper()
            if airline == "AF" and window_start <= dep_time < window_end:
                total += 1
                if row[2] != row[3]:
                    delayed += 1
        except:
            continue
    return total, delayed


def count_below_15_degrees():
    """Count flights departing below 15°C."""
    count = 0
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            temp_str = row[10].split("°")[0].strip()
            if temp_str.isdigit() and int(temp_str) < 15 and window_start <= dep_time < window_end:
                count += 1
        except:
            continue
    return count


def count_british_airways_flights():
    """Count total British Airways flights."""
    count = 0
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            airline = row[1][:2].upper()
            if airline == "BA" and window_start <= dep_time < window_end:
                count += 1
        except:
            continue
    return count


def find_least_common_destinations():
    """Return full names of least common destination(s)."""
    dest_count = {}
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            dest = row[4]
            if window_start <= dep_time < window_end and dest in defined_airport_codes:
                dest_count[dest] = dest_count.get(dest, 0) + 1
        except:
            continue
    if not dest_count:
        return []
    min_count = min(dest_count.values())
    least_dests = [defined_airport_codes[d] for d, c in dest_count.items() if c == min_count]
    return least_dests


def get_flights_per_hour_by_airline(airline_code):
    """Return list of 12 flight counts per hour for given airline."""
    hourly_counts = [0] * 12
    for row in data_list:
        try:
            dep_time = datetime.strptime(row[3], "%H:%M").time()
            airline = row[1][:2].upper()
            if airline == airline_code.upper() and window_start <= dep_time < window_end:
                hourly_counts[dep_time.hour] += 1
        except:
            continue
    return hourly_counts


def get_valid_airline_code():
    """Prompt and validate 2-letter airline code."""
    while True:
        code = input("Enter a two-character Airline code to plot a histogram: ").strip().upper()
        if code in defined_airlines:
            return code
        print("Unavailable Airline code please try again.")


def draw_histogram(airline_code, airport_code, year, hourly_flights):
    """
    Draw horizontal histogram using graphics.py safely.
    """
    try:
        airline_name = defined_airlines.get(airline_code, airline_code)
        airport_name = defined_airport_codes.get(airport_code, airport_code)
        title = f"Departures by hour for {airline_name} from {airport_name} {year}"

        max_flights = max(hourly_flights) if max(hourly_flights) > 0 else 1
        win_width = 800
        win_height = 500
        bar_height = 30
        margin_left = 100
        margin_top = 80
        bar_spacing = 35

        win = graphics.GraphWin(title, win_width, win_height)
        win.setBackground("white")

        # Title
        title_text = graphics.Text(graphics.Point(win_width // 2, 30), title)
        title_text.setSize(14)
        title_text.setStyle("bold")
        title_text.draw(win)

        # Y-axis label
        y_label = graphics.Text(graphics.Point(40, win_height // 2), "Hours")
        y_label.setSize(12)
        y_label.setStyle("bold")
        y_label.draw(win)

        # X-axis label
        x_label = graphics.Text(graphics.Point(win_width // 2, win_height - 20), "Number of Flights")
        x_label.setSize(12)
        x_label.setStyle("bold")
        x_label.draw(win)

        # Draw bars
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                  "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#aec7e8", "#ffbb78"]

        for hour in range(12):
            count = hourly_flights[hour]
            bar_width = (count / max_flights) * (win_width - margin_left - 100) if max_flights > 0 else 0
            y_center = margin_top + hour * bar_spacing + bar_height // 2

            # Bar
            bar = graphics.Rectangle(
                graphics.Point(margin_left, y_center - bar_height // 2),
                graphics.Point(margin_left + bar_width, y_center + bar_height // 2)
            )
            bar.setFill(colors[hour % len(colors)])
            bar.setOutline("black")
            bar.draw(win)

            # Hour label
            hour_label = graphics.Text(graphics.Point(margin_left - 30, y_center), f"{hour:02d}:00")
            hour_label.setSize(10)
            hour_label.draw(win)

            # Count label
            count_label = graphics.Text(graphics.Point(margin_left + bar_width + 15, y_center), str(count))
            count_label.setSize(10)
            count_label.draw(win)

        # Wait for click and close safely
        if not win.isClosed():
            win.getMouse()
            win.close()

    except graphics.GraphicsError:
        print("Graphics window was closed before interaction.")


def save_results_to_file(airport_code, year, results):
    """Append results to results.txt"""
    airport_name = defined_airport_codes[airport_code]
    text = f"File {airport_code}{year}.csv selected - Planes departing {airport_name} {year}"
    line = "*" * len(text)

    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.write(text + "\n")
        f.write(line + "\n")
        for result_line in results:
            f.write(result_line + "\n")


def print_and_collect_results(airport_code, year):
    """Calculate, print, and return results as list of strings."""
    total_flights, rain_hours = count_flights_and_rain_hours()
    t2_flights = count_terminal_2_flights()
    under_600 = count_under_600_miles()
    af_total, af_delayed = count_air_france_flights()
    below_15 = count_below_15_degrees()
    ba_flights = count_british_airways_flights()
    least_dests = find_least_common_destinations()

    avg_ba = round(ba_flights / 12, 2) if total_flights > 0 else 0
    perc_ba = round((ba_flights / total_flights) * 100, 2) if total_flights > 0 else 0
    perc_af_delayed = round((af_delayed / af_total) * 100, 2) if af_total > 0 else 0

    results = [
        f"The total number of flights from this airport was {total_flights}",
        f"The total number of flights departing Terminal Two was {t2_flights}",
        f"The total number of departures on flights under 600 miles was {under_600}",
        f"There were {af_total} Air France flights from this airport",
        f"There were {below_15} flights departing in temperatures below 15 degrees",
        f"There was an average of {avg_ba} British Airways flights per hour from this airport",
        f"British Airways planes made up {perc_ba}% of all departures",
        f"{perc_af_delayed}% of Air France departures were delayed",
        f"There were {rain_hours} hours in which rain fell",
        f"The least common destinations are {least_dests}"
    ]

    airport_name = defined_airport_codes[airport_code]
    header = f"File {airport_code}{year}.csv selected - Planes departing {airport_name} {year}"
    line = "*" * len(header)

    print(line)
    print(header)
    print(line)
    for line in results:
        print(line)

    save_results_to_file(airport_code, year, results)
    return results


def main_loop():
    """Main program loop - handles one full CSV analysis."""
    # Task A: Get valid inputs
    airport_code = get_valid_airport_code()
    year = get_valid_year()
    filename = f"{airport_code}{year}.csv"

    # Load file
    if not load_csv_file(filename):
        return False

    # Task B & C: Process and save
    print_and_collect_results(airport_code, year)

    # Task D: Histogram
    airline_code = get_valid_airline_code()
    hourly_flights = get_flights_per_hour_by_airline(airline_code)
    draw_histogram(airline_code, airport_code, year, hourly_flights)

    return True


# === Main Program ===
if __name__ == "_main_":
    print("European Airports Departure Analyzer")
    while True:
        success = main_loop()
        if not success:
            print("File processing failed. Please try again.")
        
        while True:
            choice = input("Do you want to select a new data file? Y/N: ").strip().lower()
            if choice in ['y', 'n']:
                break
            print("Invalid choice. Please enter Y or N only.")
        
        if choice == 'n':
            print("Thank you. End of run")
            break
