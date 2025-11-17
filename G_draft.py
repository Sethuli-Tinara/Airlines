from datetime import datetime,time as dtime
from graphics import *
import csv

data_list=[]
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

window_start= dtime(0,0)#Start of 12-hour window(midnight)
window_end=dtime(12,0)#End of 12 hour window(noon)


def load_csv_(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)


def count_flights_per_airline_by_hour(data_list,airline_code):
    '''This function counts number of flights from an airport of a selected airline'''
    flights_per_hour={hour: 0 for hour in range(12)}
    
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


load_csv_("C:/Users/H P/OneDrive/Documents/GitHub/Airlines/LHR2025.csv")
flights_per_hour= count_flights_per_airline_by_hour(data_list,"LH")

win=GraphWin("Histogram",1920,1080)
win.setCoords(0,0,100,100)
win.setBackground("white")

#Heading
topic=f"Departures by hour for {defined_airlines['LH']} from {defined_airport_codes['CDG']} 2025"

topic=Text(Point(40,95),topic)
topic.setStyle("bold")
topic.setTextColor("black")
topic.setSize(15)
topic.draw(win)


#Drawing x and y axis
x_axis=Line(Point(10,35),Point(75,35))
x_axis.setWidth(1)
x_axis.draw(win)

y_axis=Line(Point(10,35),Point(10,90))
y_axis.setWidth(1)           
y_axis.draw(win)


#Bar scaling calculation
maximum_flights_per_hour= max(flights_per_hour.values())
#Avoiding division by zero 
if maximum_flights_per_hour == 0:
    maximum_flights_per_hour == 1


#Bar length,width etc..
bar_width=4
bar_space=6

first_x=15
scale=500/maximum_flights_per_hour
maximum_bar_height=55

for hour in range(12):
    count=flights_per_hour[hour]
    center=first_x+hour*bar_space

    height=(count/maximum_flights_per_hour)*maximum_bar_height
    bar=Rectangle(Point(center-bar_width/2,35), Point(center,+ bar_width/2,35 + height))
    #Drawing bars
    bar.setFill("lightcoral")
    bar.setOutline("black")
    bar.draw(win)

    if count>0:
        label_y = 35 + height + 3
        if height < 10 :
            label_y = 35 + height /2
            label=Text(Point(center,label_y),str(count))
            label.setTextColor("white")
        else:
            label=Text(Point(center, label_y),str(count))
            label.setTextColor("black")

        
            

        #Hour label below
        hour_label= f"{hour:02d}:00"
        Text(Point(center,16).hour_label.setSize(10).draw(win))
    
        #Printing numbers infront of bar
    Text(Point(left_margin + bar_length + 10, y + bar_height/2),str(count)).draw(win)

    

win.getMouse()
win.close()





