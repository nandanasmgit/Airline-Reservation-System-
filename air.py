
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("airline_reservation_1.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS AIRLINE (
                    AIRLINE_ID INTEGER PRIMARY KEY,
                    NAME TEXT,
                    ADDRESS TEXT,
                    FLIGHT_ID INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS AIRPORT (
                    AIRPORT_ID INTEGER PRIMARY KEY,
                    NAME TEXT,
                    CITY TEXT,
                    COUNTRY TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS FLIGHT (
                    FLIGHT_ID INTEGER PRIMARY KEY,
                    AIRLINE_ID INTEGER,
                    DEPARTUREAIRPORT_ID INTEGER,
                    ARRIVALAIRPORT_ID INTEGER,
                    DEPARTURE_DATE TEXT,
                    ARRIVAL_DATE TEXT,
                    FLIGHTNUMBER INTEGER,
                    FOREIGN KEY (AIRLINE_ID) REFERENCES AIRLINE(AIRLINE_ID),
                    FOREIGN KEY (DEPARTUREAIRPORT_ID) REFERENCES AIRPORT(AIRPORT_ID),
                    FOREIGN KEY (ARRIVALAIRPORT_ID) REFERENCES AIRPORT(AIRPORT_ID))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS SEAT (
                    SEAT_ID INTEGER PRIMARY KEY,
                    FLIGHT_ID INTEGER,
                    SEAT_NO TEXT,
                    CLASS TEXT,
                    FOREIGN KEY (FLIGHT_ID) REFERENCES FLIGHT(FLIGHT_ID))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS PASSENGER (
                    PASSENGER_ID INTEGER PRIMARY KEY,
                    NAME TEXT,
                    DOB TEXT,
                    EMAIL TEXT,
                    PHONE_NO TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS RESERVATION (
                    RESERVATION_ID INTEGER PRIMARY KEY,
                    RESERVATION_DATE TEXT,
                    STATUS TEXT,
                    PASSENGER_ID INTEGER,
                    FLIGHT_ID INTEGER,
                    FOREIGN KEY (PASSENGER_ID) REFERENCES PASSENGER(PASSENGER_ID),
                    FOREIGN KEY (FLIGHT_ID) REFERENCES FLIGHT(FLIGHT_ID))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS PAYMENT (
                    PAYMENT_ID INTEGER PRIMARY KEY,
                    AMOUNT REAL,
                    PAYMENT_DATE TEXT,
                    PAYMENT_METHOD TEXT,
                    RESERVATION_ID INTEGER,
                    FOREIGN KEY (RESERVATION_ID) REFERENCES RESERVATION(RESERVATION_ID))''')

conn.commit()

# Close the connection
conn.close()

# Function to add a passenger
def add_passenger():
    name = name_entry.get()
    dob = dob_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    conn = sqlite3.connect("airline_reservation_1.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PASSENGER (NAME, DOB, EMAIL, PHONE_NO) VALUES (?, ?, ?, ?)", 
                   (name, dob, email, phone))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"Passenger {name} added successfully!")
    add_passenger_form.reset()

# Function to make a reservation
def make_reservation():
    passenger_id = passenger_id_entry.get()
    flight_id = flight_id_entry.get()
    reservation_date = reservation_date_entry.get()
    status = status_var.get()

    conn = sqlite3.connect("airline_reservation_1.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO RESERVATION (RESERVATION_DATE, STATUS, PASSENGER_ID, FLIGHT_ID) VALUES (?, ?, ?, ?)", 
                   (reservation_date, status, passenger_id, flight_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Reservation made successfully!")
    make_reservation_form.reset()

# Function to search for flights
def search_flights():
    departure = departure_entry.get()
    arrival = arrival_entry.get()

    conn = sqlite3.connect("airline_reservation_1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM FLIGHT WHERE DEPARTUREAIRPORT_ID=? AND ARRIVALAIRPORT_ID=?", 
                   (departure, arrival))
    results = cursor.fetchall()
    conn.close()

    search_results_text.delete("1.0", tk.END)
    if results:
        for row in results:
            search_results_text.insert(tk.END, f"Flight ID: {row[0]}, Flight Number: {row[6]}\n")
    else:
        search_results_text.insert(tk.END, "No flights found.")

# Create the main tkinter window
root = tk.Tk()
root.title("Airline Reservation System")

# Add Passenger Form
add_passenger_frame = tk.LabelFrame(root, text="Add Passenger")
add_passenger_frame.pack(fill="both", expand="yes", padx=10, pady=5)

tk.Label(add_passenger_frame, text="Name:").pack()
name_entry = tk.Entry(add_passenger_frame)
name_entry.pack()

tk.Label(add_passenger_frame, text="Date of Birth (YYYY-MM-DD):").pack()
dob_entry = tk.Entry(add_passenger_frame)
dob_entry.pack()

tk.Label(add_passenger_frame, text="Email:").pack()
email_entry = tk.Entry(add_passenger_frame)
email_entry.pack()

tk.Label(add_passenger_frame, text="Phone Number:").pack()
phone_entry = tk.Entry(add_passenger_frame)
phone_entry.pack()

tk.Button(add_passenger_frame, text="Add Passenger", command=add_passenger).pack()

# Make Reservation Form
make_reservation_frame = tk.LabelFrame(root, text="Make Reservation")
make_reservation_frame.pack(fill="both", expand="yes", padx=10, pady=5)

tk.Label(make_reservation_frame, text="Passenger ID:").pack()
passenger_id_entry = tk.Entry(make_reservation_frame)
passenger_id_entry.pack()

tk.Label(make_reservation_frame, text="Flight ID:").pack()
flight_id_entry = tk.Entry(make_reservation_frame)
flight_id_entry.pack()

tk.Label(make_reservation_frame, text="Reservation Date (YYYY-MM-DD):").pack()
reservation_date_entry = tk.Entry(make_reservation_frame)
reservation_date_entry.pack()

status_var = tk.StringVar(value="Confirmed")
tk.Label(make_reservation_frame, text="Status:").pack()
tk.OptionMenu(make_reservation_frame, status_var, "Confirmed", "Pending", "Cancelled").pack()

tk.Button(make_reservation_frame, text="Make Reservation", command=make_reservation).pack()

# Search Flights Form
search_flights_frame = tk.LabelFrame(root, text="Search Flights")
search_flights_frame.pack(fill="both", expand="yes", padx=10, pady=5)

tk.Label(search_flights_frame, text="Departure Airport ID:").pack()
departure_entry = tk.Entry(search_flights_frame)
departure_entry.pack()

tk.Label(search_flights_frame, text="Arrival Airport ID:").pack()
arrival_entry = tk.Entry(search_flights_frame)
arrival_entry.pack()

tk.Button(search_flights_frame, text="Search Flights", command=search_flights).pack()

search_results_text = tk.Text(search_flights_frame, height=5, width=40)
search_results_text.pack()

# Run the main loop
root.mainloop()
