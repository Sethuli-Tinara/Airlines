from graphics import *
import csv

data_list = []   # data_list An empty list to load and hold data from csv file

def load_csv(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)

#************************************************************************************************************

#Creating a dictionary with airport code and it's respective airport name
defined_airport_codes= {
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
defined_airlines= {
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

def count_departure_flights(data_list):
    '''This function counts the total number of flights departing '''
    
    total_departure_flights = 0
    
    for row in data_list:
        try: #Counting total numer of departure flights
            total_departure_flights += 1
        
        except Exception as e:           
            print(f"Error processing row: {e}")
            continue
    
    return total_departure_flights                                 

def count_two_terminal_flights(data_list):
    '''This function counts the total number of flights departing from Terminal 2 '''
    
    total_departure_T2 = 0
    for row in data_list:
        try: #Converting terminal field to integer
            if int(row[8])== 2:
                total_departure_T2 += 1
        
        except Exception as e:           
            print(f"Error processing row: {e}")
            continue

    return total_departure_T2

def count_flights_under_600_miles(data_list):
    '''This function counts the total number of departures of flights that are under 600 miles '''
    
    total_flights_under_600 = 0
    for row in data_list:
        try:#Converting distance field to integr
            if int(row[5])< 600:
                total_flights_under_600 += 1
        
        except Exception as e:     
            print(f"Error processing row: {e}")
            continue
    
    return total_flights_under_600

def count_Air_France_flights(data_list):
    '''This function counts the total number of Air France flights '''
 
    total_AF_airline_flights = 0
    delayed_AF_flights = 0
    for row in data_list:
        try:
            airline = row[1][:2]
            if airline == "AF":
                total_AF_airline_flights += 1
                if row[2] != row[3]: #Checking if scheduled time equal to departure time
                    delayed_AF_flights += 1
        
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
    
    return total_AF_airline_flights,delayed_AF_flights

def count_flights_under_15_degrees(data_list):
    '''This function counts the total number of departures of flights that are under 15 Celsius degrees'''
    
    total_flights_temp = 0
    for row in data_list:
        try:
            temperature = int(row[10].split("Â")[0])#Splits temprature field and convert to integer
            if temperature < 15:# Checking if temperature is below 15 degrees
                total_flights_temp += 1
        
        except Exception as e:
            print(f"Error processing row: {e}:")
            continue

    return total_flights_temp

def count_BA_airline_flights(data_list):
    '''This function counts the total number of flights for British Airways'''
    total_BA_airline_flights = 0
    for row in data_list:
        try:
            airline = row[1][:2]
            #Checking airline 
            if airline == "BA":
                total_BA_airline_flights += 1
        
        except Exception as e:
            print(f"Error processing row: {e}:")
            continue


    return total_BA_airline_flights

def count_rainy_hours(data_list):
    ''' This function counts the number of flights departing below 15 degrees'''

    #Creating a set to not repeat values
    rainy_hours = set()
    for row in data_list:
        try:
            hour = row[2].split(":")[0]#Extracting hour
            hour = int(hour) #Converting to integer
            if "rain" in row[10].lower(): #Checking if "rain" in the field
                rainy_hours.add(hour)

        except Exception as e:
            print(f"Error processing row: {e}:")
            continue

    return rainy_hours

def count_least_common_destinations(data_list,defined_airport_codes):
    '''This functions finds the least common destination(s) from the data list '''

    count_of_destinations = {} #Creating a dictionary to find the least common destinations
    least_common_destinations = [] #List to hold least common destinations
    least_common_destinations_full_form = []#List to hold the full form of least common destinations  
    for row in data_list:
        try:
            #Finding the destinations with the least number of flights
            destination=row[4]
            if destination in defined_airport_codes:
                #Add 1 to the destination if it already exists else start at 1
                if destination in count_of_destinations:
                    count_of_destinations[destination] += 1
                else:
                    count_of_destinations[destination] = 1

        except Exception as e:
            print(f"Error processing row: {e}:")
            continue 
    
    if not count_of_destinations:
        return [] #Return an empty list if there are no destinations found                     
    
    least_common_destination_count = min(count_of_destinations.values()) #Finding the minimum value in the dictionary of count of destinations
    for destination,count in count_of_destinations.items():#Appending items to the list after iterating over the dictionary checking if the destination has the least count
        if count == least_common_destination_count :
            least_common_destinations.append(destination)  
    for destination in least_common_destinations:
        least_common_destinations_full_form.append(defined_airport_codes[destination])

    return least_common_destinations_full_form

def count_flights_per_airline_by_hour(data_list,airline_code):
    '''This function counts number of flights from an airport of a selected airline'''

    #Creating a dictionary to count flights for each hour(From 00.00am - 11.00 am) 
    flights_per_hour= {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}
    
    for row in data_list:
        try:
            #Count flights of the selected airline by splitting through colon and converting hour to integer
            hour = row[2].split(":")[0] #Extracting hour
            hour = int(hour) # Converting to integer
            if airline_code== row[1][:2]:
               flights_per_hour[hour]+= 1 #if conditions match adding 1 to the respective hour
        
        except Exception as e:
             print(f"Error processing row: {e}:")
             continue


    return flights_per_hour

def create_histogram(airline_code,city_code,year,flights_per_hour):
    '''Creating histogram based on the user's input of airline code to output flights each hour of the respective airline '''

    try:
        #Create window
        window= GraphWin("Histogram",1200,700)
        window.setCoords(0,0,100,100)
        window.setBackground("white")

        left_margin= 25
        bottom_margin= 5
        bar_height= 5
        spacing = 2
        total_height = (bar_height + spacing) * 12
        n_hours= 12
       
        #Title
        title=f"Departures by hour for {defined_airlines.get(airline_code)} from {defined_airport_codes.get(city_code)} {year}"
        title_style=Text(Point(50,95),title)
        title_style.setSize(14)
        title_style.draw(window)
        
        #Checking if the dictionary is empty and outputing an error message
        if flights_per_hour:
            max_count = max(flights_per_hour.values())
        else:
            max_count=0
            
        if max_count == 0 :
            message = Text(Point(50,50),"No flights for this airline during this period")
            message.setSize(12)
            message.draw(window)
            window.getMouse()
            window.close()

            return

        #Y axis label
        y_axis_line = Text(Point(left_margin - 10, bottom_margin + 40), "Hours\n00:00\nto\n12:00")
        y_axis_line.setSize(12)
        y_axis_line.draw(window)

        #Individually looping to draw each bar
        for i in range (n_hours):
            hour= i
            count = flights_per_hour.get(hour,0)

            #Vertical stacking of bars
            y_bottom = bottom_margin + hour * (bar_height + spacing)
            y_top = y_bottom+ bar_height

            #Scaling bar width and handling zero division error
            if max_count > 0:
                bar_width = (count/max_count) * 60
            else:
                bar_width = 0
           
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

            #Count label (infront of bar)
            text_x = left_margin + bar_width + 3
            text_y = (y_bottom + y_top) / 2
            text = Text(Point(text_x, text_y), str(count))
            text.setSize(9)
            text.draw(window)
               
        #Y axis line
        y_axis = Line(Point(left_margin, bottom_margin), Point(left_margin, bottom_margin + total_height + 0.9))
        y_axis.setWidth(1)
        y_axis.draw(window)

        #X axis line
        x_axis =Line(Point(left_margin, bottom_margin), Point(left_margin + 65, bottom_margin))
        x_axis.setWidth(1)
        x_axis.draw(window)

        #Arrowhead for Y axis
        y_up = Point(left_margin, bottom_margin + total_height + 1)
        y_left = Point(left_margin - 0.5, bottom_margin + total_height - 1) 
        y_right = Point(left_margin + 0.5, bottom_margin + total_height - 1)
        y_arrow = Polygon(y_up, y_left, y_right)
        y_arrow.setFill("black")
        y_arrow.draw(window)

        #Arrowhead for X axis
        x_tip = Point(left_margin + 65, bottom_margin)
        x_up = Point(left_margin + 64, bottom_margin - 0.8)
        x_down = Point(left_margin + 64, bottom_margin + 0.8)
        x_arrow = Polygon(x_tip,x_up,x_down)
        x_arrow.setFill("black")
        x_arrow.draw(window)

        #Label
        departure_label = Rectangle(Point(45,bottom_margin - 4),Point(46.2,bottom_margin - 2))
        departure_label.setFill("purple")
        departure_label.setOutline("black")
        departure_label.draw(window)

        departure_label_text = Text(Point(53, bottom_margin - 3),"Departures per hour")
        departure_label_text.setSize(12)
        departure_label_text.draw(window)
        
        try:
            window.getMouse()

        except GraphicsError:
            pass

        finally:
            window.close()

    except Exception as e:
        print("Error creating histogram:",e)
        
     
#---------------------------------------------------------------------Main Program-------------------------------------------------------------------------------------
def main():
    #Validation of city code
    city_code = input("Please enter a three-letter city code: ").upper().strip()#Allowing lower case and remove whitespace
    
    while True:       
        if len(city_code)!= 3:#Validating length
            city_code = input ("Wrong code length-please enter a three-letter city code: ").upper().strip()
            continue

        if city_code not in defined_airport_codes:
            city_code = input("Unavailable city code-please enter a valid city code: ").upper().strip()
            continue

        break #Loop breaks after city code is valid

    #Validation of year
    year = (input("Please enter the year required in the format YYYY: "))

    while True:
        try:
            year = int(year)
            if 2000 <= year <= 2025:
                year = str(year)
                break
            
            else:
                year = input("Out of range - please enter a value from 2000 to 2025: ")

        except ValueError:
            year = input("Wrong data type - please enter a four-digit year value: ")
            
    selected_data_file = f"{city_code}{year}.csv"
    #Passing argument(File) and clearing previous data
    data_list.clear() 
    
    try:
        #Loading selected data file
        load_csv(selected_data_file)

    except FileNotFoundError:
        #If file not found output and error message and returning to main program
        print(f"Error: File {selected_data_file} not found.")
        return
    
    text=f"File {selected_data_file} selected-Planes departing {defined_airport_codes[city_code]} {year}"
    print("*"*len(text))
    print(f"File {selected_data_file} selected-Planes departing {defined_airport_codes[city_code]} {year}")
    print("*"*len(text))

    #Calling functions and Calculating required values
    total_departure_flights = count_departure_flights(data_list)
    total_departure_T2 = count_two_terminal_flights(data_list)
    total_flights_under_600 = count_flights_under_600_miles(data_list)
    total_AF_airline_flights,delayed_AF_flights = count_Air_France_flights(data_list)
    total_flights_temp = count_flights_under_15_degrees(data_list)
    total_BA_airline_flights = count_BA_airline_flights(data_list)
    total_rain_hours = count_rainy_hours(data_list)
    least_common_destinations_full_form = count_least_common_destinations(data_list,defined_airport_codes)
    
    #round function to round off values to decimal values
    average_BA_flights = round(total_BA_airline_flights/12,2)

    if total_departure_flights > 0:
        percentage_BA_flights = round((total_BA_airline_flights/total_departure_flights)*100,2)

    else:
        percentage_BA_flights = 0.00

    if total_AF_airline_flights > 0:
        percentage_delayed_AF_flights = round((delayed_AF_flights/total_AF_airline_flights)*100,2)

    else:
        percentage_delayed_AF_flights = 0.00
              
    #Opening a text file as "results.txt" to write the results using "with open" for safe file handling
    
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
                f"There were {len(total_rain_hours)} hours in which rain fell\n",
                f"The least common destination(s) are {least_common_destinations_full_form}\n"
            ]
        for line in lines:
            fo.write(line)
            print(line,end="")
        
        fo.write("\n")#Writes blank line for readability

    #Get airline code from user
    airline_code = input("Enter a two-character Airline code to plot a Histogram: ").upper().strip()
    while airline_code not in defined_airlines: #Output Error message if airline code not available and ask for input again allowing upper and lower case removing whitesapce
        airline_code= input("Unavailable Airline code please try again: ").upper().strip() 
    hour = count_flights_per_airline_by_hour(data_list,airline_code)
    create_histogram(airline_code,city_code,year,hour)
    
if __name__ == "__main__":
    main()

while True:
    try:
        print()  # Prints new line for readability
        #Ask from user whether they need to read for a new file
        user_choice = input("Do you want to select a new data file? Y/N: ").lower().strip()#Converting lower case and remove whitespace

        if user_choice == "y":
            print()
            main()

        elif user_choice == "n":
            print("Thank you. End of run.")
            break

        else:
            print("Invalid choice. Please enter Y or N only.")

    except ValueError:
        print("Invalid choice. Please enter Y or N only.")
