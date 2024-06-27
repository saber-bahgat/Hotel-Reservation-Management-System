import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("hotel_reservation_management_system.db")
cur = conn.cursor()

cur.execute("DROP TABLE rooms")
cur.execute("""CREATE TABLE IF NOT EXISTS rooms(
            
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            price INTEGER NOT NULL,
            status TEXT NOT NULL,
            reservation_start DATE,
            reservation_end DATE
            )""")
conn.commit()
conn.close()

def add_room(type_room, price):
    conn = sqlite3.connect("hotel_reservation_management_system.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO rooms(type, price, status) VALUES(?, ?, ?)", (type_room, price, 'No Reservation'))
    conn.commit()
    conn.close()

def edit_room(room_id, new_type, new_price):
    conn = sqlite3.connect("hotel_reservation_management_system.db")
    cur = conn.cursor()
    cur.execute("UPDATE rooms SET type = ?, price = ? WHERE id = ?", (new_type, new_price, room_id))
    conn.commit()
    conn.close()

def reservation_rooms(room_id, days):
    conn = sqlite3.connect("hotel_reservation_management_system.db")
    cur = conn.cursor()

    # Calculate current date and reservation end date
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=days)

    # Use parameter substitution to safely insert values into SQL statement
    cur.execute("UPDATE rooms SET status = ?, reservation_start = ?, reservation_end = ? WHERE id = ?",
                ("Reserved", str(current_date), str(end_date), room_id))
    conn.commit()
    conn.close()

def cancel_reservation(room_id):
    conn = sqlite3.connect("hotel_reservation_management_system.db")
    cur = conn.cursor()
    cur.execute("UPDATE rooms SET status = ?, reservation_start = NULL, reservation_end = NULL WHERE id = ?", ('No Reservation', room_id))
    conn.commit()
    conn.close()

def display_rooms():
    conn = sqlite3.connect("hotel_reservation_management_system.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM rooms")
    result = cur.fetchall()
    conn.close()
    return result

def search_rooms(search):
    conn = sqlite3.connect("hotel_reservation_management_system.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM rooms WHERE type LIKE ?", ('%' + search + '%',))
    result = cur.fetchall()
    conn.close()
    return result

def delete_room(room_id):
    conn = sqlite3.connect("hotel_reservation_management_system.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
    conn.commit()
    conn.close()

def main():
    print("Welcome to the Hotel Reservation Management System!")
    while True:
        print("1. Add Room")
        print("2. Edit Room Data")
        print("3. Display Rooms")
        print("4. Reservation Room")
        print("5. Search For Rooms")
        print("6. Cancel Room Reservation")
        print("7. Delete Room")
        print("8. Exit")
        choice = input("Enter your choice from 1 to 8: ")
        
        if choice == '1':
            print("# Add Room!")
            type_room = input("Enter the room type (Single, Family, Double): ").title()
            price = int(input("Enter a price: "))
            add_room(type_room, price)
            print("Room added successfully!")
            print("-"*10)
        
        elif choice == '2':
            print("# Edit Room Data!")
            room_id = input("Enter the room ID you want to edit: ")
            new_type = input("Enter the new room type: ").title()
            new_price = int(input("Enter the new price: "))
            edit_room(room_id, new_type, new_price)
            print(f"Room {room_id} data updated successfully!")
            print("-"*10)
        elif choice == '3':
            print("# Display Rooms!")
            rooms = display_rooms()
            for room in rooms:
                print(f"ID: {room[0]} | Type: {room[1]} | Price: {room[2]} | Status: {room[3]}")
                if room[3] == 'Reserved':
                    print(f"Reservation Start: {room[4]} | Reservation End: {room[5]}")
            print("-"*10)
        
        elif choice == '4':
            print("# Reservation Room!")
            room_id = input("Enter the room ID you want to reserve: ")
            days = int(input("Enter the number of days for the reservation: "))
            reservation_rooms(room_id, days)
            print(f"Room {room_id} reserved successfully for {days} days!")
            print("-"*10)

        elif choice == '5':
            print("# Search For Rooms!")
            search_term = input("Enter a room type (Single, Family, Double) to search for: ").title()
            results = search_rooms(search_term)
            print("Search results:")
            for room in results:
                print(f"ID: {room[0]} | Type: {room[1]} | Price: {room[2]} | Status: {room[3]}")
                if room[3] == 'Reserved':
                    print(f"Reservation Start: {room[4]} | Reservation End: {room[5]}")
            print("-"*10)
        
        elif choice == '6':
            print("# Cancel Room Reservation!")
            room_id = input("Enter the room ID to cancel reservation: ")
            cancel_reservation(room_id)
            print(f"Reservation for room {room_id} canceled successfully!")
            print("-"*10)
        
        elif choice == '7':
            print("# Delete Room!")
            room_id = input("Enter the room ID you want to delete: ")
            delete_room(room_id)
            print(f"Room {room_id} deleted successfully!")
            print("-"*10)
        
        elif choice == '8':
            print("Exiting program...  Goodbye!")
            break
        
        else:
            print("Invalid choice! Please enter a number from 1 to 8.")

if __name__ == '__main__':
    main()
