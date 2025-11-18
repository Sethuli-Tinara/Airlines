import csv
from datetime import datetime,time as dtime
from graphics import *


window_start= dtime(0,0)#Start of 12-hour window(midnight)
window_end= dtime(12,0)#End of 12 hour window(noon)

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
    
            

#Creating a dictionary with airport code and it's respective airport name
defined_airport_codes={
    "LHR":"London Heathrow",
    "MAD":"Madrid Adolfo Suárez-Bajaras",
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
    "SK":"Scandinavian Airlines",
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

#Creating a dictionary to count flights for each hour(From 00.00am - 11.00 am)

flights_per_hour={hour: 0 for hour in range(12)}

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
    '''This function counts the total number of flights departing from Terminal 2 in 12 hour window'''
    
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
    '''This function counts the total number of Air France flights in 12 hour window'''
 
    total_AF_airline_flights=0
    delayed_AF_flights=0
    for row in data_list:
        try:
            #
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
    '''This function counts the total number of departures of flights thaat are under 15 Celsius degrees in 12 hour window'''
    
    total_flights_temp=0
    for row in data_list:
        try:
            
            dep_time= datetime.strptime(row[3],"%H:%M").time()
            temperature= int(row[10][0:2])
            if temperature < 15 and window_start <= dep_time < window_end:
                total_flights_temp+=1
        
        except Exception as e:

            print(f"Error processing row: {e}:")
            continue

    return total_flights_temp


def count_flights_under_600_miles(data_list):
    '''This function counts the total number of departures of flights that are under 600 miles in 12 hour window'''
    
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
    '''This functions finds the least common destination(s) from the data list in 12 hour window'''

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
    for destination,count in count_of_destinations.items():#Appending items to the list after iterating over the dictionary checking if the destination has the least count
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
            #Checking time window and airline 
            if airline=="BA" and window_start <= dep_time < window_end:
                total_BA_airline_flights+=1
        
        except Exception as e:
            print(f"Error processing row: {e}:")
            continue


    return total_BA_airline_flights

def count_flights_per_airline_by_hour(data_list,airline_code):
    '''This function counts number of flights from an airport of a selected airline'''
    
    while airline_code not in defined_airlines: #Output Error message if airline code not available
            airline_code= input("Unavailable Airline code please try again: ")
    
    for row in data_list:
        try:
            #Count flights of the selected airline and checking time window
            dep_time=datetime.strptime(row[3],"%H:%M").time()
            if airline_code== row[1][:2] and window_start <= dep_time < window_end:
               flights_per_hour[dep_time.hour]+= 1 #if conditions match adding 1 to the respective hour
        
        except Exception as e:
             print(f"Error processing row: {e}:")
             continue


    return flights_per_hour

def create_histogram(airline_code,city_code,year,flights_per_hour):
    '''Creating histogram based on the user's input of airline code to output flights each hour of the respective airline '''

    try:
        window= GraphWin("Histogram",1920,1080)
        window.setCoords(0,0,100,100)
        window.setBackground("white")

        left_margin=15
        right_margin=5
        bottom_margin=10
        top_margin=10

        available_width= 100 - left_margin - right_margin
        n_hours= 12
        bar_gap= 4

        #Title
        title=f"Departures by hour for {defined_airlines.get(airline_code)} from {defined_airport_codes.get(city_code)} {year}"
        title_style=Text(Point(50,95),title)
        title_style.setSize(14)
        title_style.draw(window)
        

        #Checking if the dictionary is empty and outputing an error message
        max_count = max(flight_per_hour.values()) if flights_per_hour else 0
        if max_count <=0 :
            message = Text(Point(50,50),"No flights for this airline during this period")
            message.setSize(12)
            message.draw(window)
            window.getMouse()
            window.close()

            return

        #X axis and Y axis
        axis_line = Line (Point (left_margin-2, bottom_margin) , Point (left_margin-2, bottom_margin + n_hours *(available_width/n_hours)))
        axis_line.setWidth(1)
        axis_line.draw(window)

        #Individually looping 
        for i in range (n_hours):
            hour = i
            count = flights_per_hour.get(hour,0)

            #Y positioning
            y_bottom = bottom_margin+ i*(available_width/n_hours)+(available_width/n_hours - bar_height)/ 2 #Leaving space from x axis to the y axis
            y_top = y_botttom+ bar_height

            #Scaling bar width
            bar_width = (count/max_count) * available_width if max_count > 0 else 0
            
            
            #Hour Label
            hour_label = Text(Point(left_margin-5,(y_top+y_bottom)/2 ), f"{hour:02d}:00")
            hour_label.setSize(10)
            hour_label.draw(window)

            #Drawing Bars
            p1= Point(left_margin,y_bottom)
            p2= Point(left_margin+bar_width,y_top)
            bar=Rectangle(p1,p2)
            bar.setFill("purple")
            bar.draw(window)

            #Checking if bar is narrow
            if bar_width < 10:
                number_position= Point(left_margin+ bar_width + 2, (y_top + y_bottom)/2 )

            else:
                number_position= Point(left_margin + bar_width-3, (y_top + y_bottom)/2)

            number_text=Text(number_position,str(count))
            number_text.setSize(8)
            number_text.draw(window)

            max_text= Text(Point(left_margin + available_width,95-5), f"Max hour = {max_count}")
            max_text.setSize(12)
            max_text.draw(window)
            window.getMouse()
            window.close()

    except Exception as e:
        print("Error creating histogram:",e)
        

        
            
            
             
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

            year= int(input("Please enter the year required in the format YYYY: "))
            if year >= 2000 and year <= 2025:
                    year=str(year)

                    break #Breaks when year is valid
            else:
                print("Out of range-Please enter a value from 2000 to 2025.")

        except ValueError:
                print("Wrong data type-Please enter a four-digit year value: ")

    

    filename=f"{city_code}{year}.csv"
    text=f"File {filename} selected-Planes departing {defined_airport_codes[city_code]} {year}"
    print("*"*len(text))
    print(f"File {filename} selected-Planes departing {defined_airport_codes[city_code]} {year}")
    print("*"*len(text))

    #Passing argument(File) and clearing previous data
    data_list.clear()
    load_csv_(filename)



    #Calling functions and Calculating required values
    total_departure_flights,rainy_hours= count_flights_and_rain_hours(data_list)
    total_departure_T2= count_two_terminal_flights(data_list)
    total_flights_under_600= count_flights_under_600_miles(data_list)
    total_AF_airline_flights,delayed_AF_flights= count_Air_France_flights(data_list)
    total_flights_temp= count_flights_under_15_degrees(data_list)
    total_BA_airline_flights= count_airline_flights(data_list)
    least_common_destinations_full_form= count_least_common_destinations(data_list,defined_airport_codes)
    

    average_BA_flights=round(total_BA_airline_flights/12,2)
    percentage_BA_flights=round((total_BA_airline_flights/total_departure_flights)*100,2)
    percentage_delayed_AF_flights=round((delayed_AF_flights/total_AF_airline_flights)*100,2)

    with open ("results.txt","a") as fo:

        #/n used to write in to new lines
        fo.write("*"*len(text)+ "\n")
        fo.write(text+ "\n")
        fo.write("*"*len(text)+ "\n")
    
        lines=[
            
                f"The total number of departure flights from this airport was {total_departure_flights}\n",
                f"The total number of flights departing from Terminal Two was {total_departure_T2}\n",
                f"The total number of departures of flights that are under 600 miles was {total_flights_under_600}\n",
                f"There were {total_AF_airline_flights} Air France flights from this airport\n",
                f"There were {total_flights_temp} flights departing in temperatures below 15 degrees\n",
                f"There was an average of {average_BA_flights} British Airways flights per hour from this airport\n",
                f"British Airways planes made up {percentage_BA_flights}% of all departures\n",
                f"{percentage_delayed_AF_flights}% of Air France departures were delayed\n",
                f"There were {len(rainy_hours)} hours in which rain fell\n",
                f"The least common destination(s) are {least_common_destinations_full_form}\n"
            ]
        for line in lines:
            fo.write(line)
            print(line,end="")
    
    airline_code= input("Enter a two-character Airline code to plot a Histogram: ").upper()
    hour=count_flights_per_airline_by_hour(data_list,airline_code)
    create_histogram(airline_code,city_code,year,flights_per_hour)
    
if __name__=="__main__":
    main()



while True :
        try:

            user_choice=input("Do you want to select a new data file? Y/N:").lower()
            if user_choice== "y":
                main()
            elif user_choice== "n":
                print("Thank you. End of run.")
                break
            else:
                print("Invalid choice.Please enter Y or N only. ")

        except ValueError:
            
            print("Invalid choice.Please enter Y or N only.")
