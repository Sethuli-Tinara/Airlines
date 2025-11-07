import csv
from datetime import datetime,time

window_start= time(0,0)#Start of 12-hour window(midnight)
window_end=time(12,0)#End of 12 hour window(noon)

data_list = []   # data_list An empty list to load and hold data from csv file

def load_csv_(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)
            
selected_data_file = 'CDG2021.csv'  # Example CSV file name
load_csv_(selected_data_file) #calling the function to load the csv file into data_list

#Creating a dictionary with airport code and it's respective airport name
defined_airport_codes={
    "LHR":"Londom Heathrow",
    "MAD":"Madrid Adolfo Suarez-Bajara",
    "CDG":"Charles De Gaulle International",
    "IST":"Istanbul Airport International",
    "AMS":"Amsterdam Schiphol",
    "LIS":"Lisbon Portela",
    "FRA":"Frankfurt Main",
    "FCO":"Rome Fiumicino",
    "MUC":"Munich International",
    "BCN":"Barcelona International"
    }

#Creating a dictionary for airlines
defined_airlines={
    "BA":"British Airways",
    "AF":"Air France",
    "AY":"Finnair",
    "KL":"KLM",
    "SK":"Scandavian Airlines",
    "TP":"TAP Air Portugal",
    "TK":"Turkish Airlines",
    "W6":"Wizz Air",
    "U2":"easyJet",
    "FR":"Ryanair",
    "A3":"Aegean Airlines",
    "SN":"Brussels Airlines",
    "EK":"Emirates",
    "QR":"Qatar Airways",
    "IB":"Iberia",
    "LH":"Lufthansa"
    }


def count_flights_and_rain_hours(data_list):
    '''This function counts the total number of flights departing and the hours in which rain fell in the 12-hour window'''
    
    total_departure_flights_12hr= 0
    rainy_hours= set() #Using a set to avoid duplicate hours

    for row in data_list:
        try:

            #Total departure flights in the 12-hour window
            dep_time= datetime.strptime(row[3],"%H:%M").time()
            if window_start <= dep_time < window_end:
                total_departure_flights_12hr+=1
                #Checking for rain hours
                if "rain" in row[10].lower():
                    rainy_hours.add(dep_time.hour)
        
        except Exception as e:
            
            print(f"Error processing row: {e}")
            continue
    
    return total_departure_flights_12hr, rainy_hours


def count_two_terminal_flights(data_list):
    '''This function counts the total number of flights departing from Terminal 2'''
    
    total_departure_T2=0
    for row in data_list:
        try:

            dep_time= datetime.strptime(row[3],"%H:%M").time()
            if int(row[8])== 2 and window_start <= dep_time < window_end:
                total_departure_T2+=1
        
        except Exception as e:
            
            print(f"Error processing row: {e}")
            continue

    return total_departure_T2


def count_Air_France_flights(data_list):
    '''This function counts the toal number of Air France flights'''
 
    total_AF_airline_flights=0
    delayed_AF_flights=0
    for row in data_list:
        try:

            dep_time= datetime.strptime(row[3],"%H:%M").time()
            airline=row[1][:2]
            if airline=="AF" and window_start <= dep_time < window_end:
                total_AF_airline_flights+=1
                if row[2]!=row[3]:
                    delayed_AF_flights+=1

        
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
    
    return total_AF_airline_flights,delayed_AF_flights


def count_flights_under_15_degrees(data_list):
    '''This function counts the total number of departures of flights thaat are under 15 Celsius degrees'''
    
    total_flights_temp=0
    for row in data_list:
        try:

            dep_time= datetime.strptime(row[3],"%H:%M").time()
            temperature=int(row[10][0:2])
            if temperature < 15 and window_start <= dep_time < window_end:
                total_flights_temp+=1
        
        except Exception as e:

            print(f"Error processing row: {e}:")
            continue

    return total_flights_temp


def count_flights_under_600_miles(data_list):
    '''This function counts the total number of departures of flights that are under 600 miles'''
    
    total_flights_under_600=0
    for row in data_list:
        try:

            dep_time= datetime.strptime(row[3],"%H:%M").time()
            if int(row[5])< 600 and window_start<= dep_time < window_end:
                total_flights_under_600+=1
        
        except Exception as e:
            
            print(f"Error processing row: {e})")
            continue
    
    return total_flights_under_600


def count_least_common_destinations(data_list,defined_airport_codes):
    '''This functions finds the least common destination(s) from the data list'''

    count_of_destinations={} #Creating a dictionary to find the least common destinations
    for row in data_list:
        try:

            dep_time=datetime.strptime(row[3],"%H:%M").time()
            #Finding the destinations with the least number of flights
            destination=row[4]
            if window_start <= dep_time < window_end and destination in defined_airport_codes:
                #Add 1 to the destination if it already exists else start at 1
                count_of_destinations[destination]= count_of_destinations.get(destination,0)+1

        
        except Exception as e:
            print(f"Error processing row: {e}:")
            continue

    if not count_of_destinations:
        return [] #Return an empty list if there are no destinations found
               
    least_common_destination_count=min(count_of_destinations.values()) #Finding the minimum value in the dictionary of count of destinations
    least_common_destinations=[] #List to hold the least common destinations
    for destination,count in count_of_destinations.items():
        if count==least_common_destination_count:
            least_common_destinations.append(destination)

    least_common_destinations_full_form=[]#List to hold the full form of least common destinations      
    for destination in least_common_destinations:
        least_common_destinations_full_form.append(defined_airport_codes[destination])
            
        
    return least_common_destinations_full_form

def count_airline_flights(data_list):
    '''This function counts the total number of flights for a given airline code'''
    total_BA_airline_flights=0
    for row in data_list:
        try:

            dep_time=datetime.strptime(row[3],"%H:%M").time()
    
            airline=row[1][:2]
            if airline=="BA" and window_start <= dep_time < window_end:
                total_BA_airline_flights+=1
        
        except Exception as e:
            print(f"Error processing row: {e}:")
            continue


    return total_BA_airline_flights

#Main Program
def main():


    while True:
        
        city_code=input("Please enter a three-letter city code: ").upper()#Allowing lower case

        city_found=False #Flag variable to make sure city exists

        for code in defined_airport_codes:#Checking if city_code exist in defined list of airport codes

            if city_code==code:
                city_found=True #Marking city as found

            if city_code not in defined_airport_codes:
                if len(city_code)!=3:#Validating length
                    city_code=input("Wrong code length-please enter a three-letter city code: ").upper()
                    continue
                else:
                    city_code=input("Unavailable city code-please enter a valid city code: ").upper()
                    continue
        break

    while True:
        
        try:

            year=int(input("Please enter the year required in the format YYYY: "))
            if year>=2000 and year<=2025:
                    year=str(year)

                    break #Breaks when year is valid
            else:
                print("Out of range-Please enter a value from 2000 to 2025.")

        except ValueError:
                print("Wrong data type-Please enter a four-digit year value: ")

    

    filename=f"{city_code}{year}.csv"
    print("*"*100)
    print(f"File {filename} selected-Planes departing {defined_airport_codes[city_code]} {year}")
    print("*"*100)

    #Passing argument(File) and clearing previous data
    data_list.clear()
    load_csv_(filename)



    #Calling functions and Calculating required values
    total_departure_flights,rainy_hours=count_flights_and_rain_hours(data_list)
    total_departure_T2=count_two_terminal_flights(data_list)
    total_flights_under_600=count_flights_under_600_miles(data_list)
    total_AF_airline_flights,delayed_AF_flights=count_Air_France_flights(data_list)
    total_flights_temp=count_flights_under_15_degrees(data_list)
    total_BA_airline_flights=count_airline_flights(data_list)
    least_common_destinations_full_form=count_least_common_destinations(data_list,defined_airport_codes)

    average_BA_flights=round(total_AF_airline_flights/12,2)
    percentage_BA_flights=round((total_BA_airline_flights/total_departure_flights)*100,2)
    percentage_delayed_AF_flights=round((delayed_AF_flights/total_AF_airline_flights)*100,2)

    with open ("results.txt","a") as fo:
        lines=[
            
                f"The total number of departure flights from this airport was {total_departure_flights}\n",
                f"The total number of flights departing from Terminal Two was {total_departure_T2}\n",
                f"The total number of departures of flights that are under 600 miles was {total_flights_under_600}\n",
                f"There were {total_AF_airline_flights} Air France flights from this airport\n",
                f"There were {total_flights_temp} flights departing in temperatures below 15 degrees\n",
                f"There was an average of {average_BA_flights} British Airways flights per hour from this airport\n",
                f"British Airways planes made up {percentage_BA_flights} of all departures\n",
                f"{percentage_delayed_AF_flights} of Air France departures were delayed\n",
                f"They were {len(rainy_hours)} hours in which rain fell\n",
                f"The least common destination(s) are {least_common_destinations_full_form}\n"
            ]
        for line in lines:
            fo.write(line)
            print(line,end="")

if __name__=="__main__":
    main()
