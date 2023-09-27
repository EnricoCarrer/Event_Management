import time
from abc import ABC, abstractmethod
import csv
import re

# Global variables
event_filename = 'events.csv'
attendee_filename = 'attendees.csv'


# Trying custom error handling
class MyCustomException(Exception):
    def __init__(self, message):
        super().__init__(message)


# Event is the abstract class that serves as the base class for all events types. It contains common attributes and
# abstract methods that every event should have.
class Event(ABC):

    def __init__(self, event_id, event_type, event_name, event_date, event_time, event_location):
        self.__event_id = event_id
        self.__event_type = event_type
        self.__event_name = event_name
        self.__event_date = event_date
        self.__event_time = event_time
        self.__event_location = event_location
        self.events = []

    # decorators (getters and setters)
    @property
    def event_id(self):
        return self.__event_id

    @event_id.setter
    def event_id(self, event_id):
        self.__event_id = event_id

    @property
    def event_type(self):
        return self.__event_type

    @event_type.setter
    def event_type(self, event_type):
        self.__event_type = event_type

    @property
    def event_name(self):
        return self.__event_name

    @event_name.setter
    def event_name(self, event_name):
        self.__event_name = event_name

    @property
    def event_date(self):
        return self.__event_date

    @event_date.setter
    def event_date(self, event_date):
        self.__event_date = event_date

    @property
    def event_time(self):
        return self.__event_time

    @event_time.setter
    def event_time(self, event_time):
        self.__event_time = event_time

    @property
    def event_location(self):
        return self.__event_location

    @event_location.setter
    def event_location(self, event_location):
        self.__event_location = event_location

    # re-usable methods that are common within different subclasses
    def get_latest_id(self, filename):  # finding the latest id number, so a new unique id number can be created when
        # adding a new event.
        try:
            with open(filename, 'r', newline='') as csvfile:
                event_reader = csv.reader(csvfile)
                rows = list(event_reader)
                if rows:  # Check if there are any rows in the file
                    last_row = rows[-1]  # Read the last row to get the last event ID
                    return int(last_row[0])
                else:
                    return 0  # No events in the file yet, start with ID 1
        except FileNotFoundError:
            # If the file doesn't exist yet, start with ID 1
            return 0

    def get_valid_date_input(self):
        while True:
            event_date = input("Enter event date (DD/MM/YYYY): ")
            date_pattern = r'^\d{2}/\d{2}/\d{4}$'  # expression pattern for the correct format (DD/MM/YYYY)
            if re.match(date_pattern, event_date):
                return event_date
            else:
                print("Invalid date format. Please use DD/MM/YYYY format.")

    def get_valid_time_input(self):
        while True:
            try:
                event_time = input("Enter event time (HH:MM): ")
                time_pattern = r'^\d{2}:\d{2}$'  # expression pattern for the correct format (HH:MM)
                if re.match(time_pattern, event_time):
                    return event_time
                else:
                    raise MyCustomException("Invalid time format. Please use HH:MM format.")
            except MyCustomException as e:
                print(e)

    def list_all_events(self):
        try:
            with open(event_filename, 'r') as file:
                self.events = csv.reader(file, delimiter=",", quotechar='/')
                line_count = 0
                print('\nHeader: ID, type, name, Date, Time, Location, owner\n')
                for row in file:
                    print(row)
                    line_count += 1
                print(f'Total events: {line_count}')
                print('_______________')
        except FileNotFoundError:
            print("File not found.")

    def display_individual_event(self):
        chose_event_to_view = input('Enter the ID of the event you want to see: ')
        try:
            with open(event_filename, 'r') as file:
                self.events = csv.reader(file, delimiter=",", quotechar='/')
                print()
                for row in self.events:
                    if chose_event_to_view == row[0]:
                        if row[1] == 'wedding':
                            print(
                                f'ID: {row[0]} \nType: {row[1]} \nName: {row[2]} \nDate: {row[3]} \nTime: {row[4]} \nLocation: {row[5]} \nBride and Groom: {row[6]}')
                        elif row[1] == 'birthday':
                            print(
                                f'ID: {row[0]} \nType: {row[1]} \nName: {row[2]} \nDate: {row[3]} \nTime: {row[4]} \nLocation: {row[5]} \ncelebrant: {row[6]}')
                        elif row[1] == 'business':
                            print(
                                f'ID: {row[0]} \nType: {row[1]} \nName: {row[2]} \nDate: {row[3]} \nTime: {row[4]} \nLocation: {row[5]} \nhost: {row[6]}')
                        break
                else:
                    print('Event not found. Chose option 2 to view existing events.')
                print('_______________')
        except FileNotFoundError:
            print("File not found.")

    def edit_event(self):
        self.event_id = int(input("Enter the event ID you want to edit: "))

        try:
            with open(event_filename, 'r', newline='') as csvfile:
                self.events_data = list(csv.reader(csvfile))
                found_event = None

                # Find the event with the provided ID
                for i, event in enumerate(self.events_data):
                    if int(event[0]) == self.event_id:
                        found_event = event
                        break

                if found_event:
                    print(f"Event ID: {found_event[0]}")
                    print(f"Event Type: {found_event[1]}")
                    print(f"Event Name: {found_event[2]}")
                    print(f"Event Date: {found_event[3]}")
                    print(f"Event time: {found_event[4]}")
                    print(f"Event location: {found_event[5]}")
                    if found_event[1] == 'wedding':
                        print(f"Bride & groom: {found_event[6]}")
                    if found_event[1] == 'birthday':
                        print(f"celebrant: {found_event[6]}")
                    if found_event[1] == 'business':
                        print(f"host: {found_event[6]}")

                    attribute_to_edit = input("Enter the attribute to edit (Name/Date/Time/Location): ").lower()

                    # Determine the index of the attribute to edit
                    if attribute_to_edit == "name":
                        new_value = input(str("Enter event name/description: "))
                        attr_index = 2
                    elif attribute_to_edit == "date":
                        new_value = Event.get_valid_date_input(self)
                        attr_index = 3
                    elif attribute_to_edit == "time":
                        new_value = Event.get_valid_time_input(self)
                        attr_index = 4
                    elif attribute_to_edit == "location":
                        attr_index = 5
                    else:
                        print("Invalid input. You can only amend Name/Date/Time/Location.")
                        return

                    # Update the selected attribute
                    found_event[attr_index] = new_value

                    # Write the updated data back to the CSV file
                    with open(event_filename, 'w', newline='') as csvfile:
                        event_writer = csv.writer(csvfile)
                        for event in self.events_data:
                            event_writer.writerow(event)

                    print("Event updated successfully!")
                else:
                    print("Event not found with the given ID. Chose option 2 to view all events.")
        except FileNotFoundError:
            print("File not found.")

    def delete_event(self):
        event_id = int(input("Enter the event ID you want to delete: "))
        try:
            with open(event_filename, 'r', newline='') as csvfile:
                events_data = list(csv.reader(csvfile))

                found_event = None

                # Find the event with the provided ID
                for i, event in enumerate(events_data):
                    if int(event[0]) == event_id:
                        found_event = event
                        break

                if found_event:
                    print(f"Event ID: {found_event[0]}")
                    print(f"Event Type: {found_event[1]}")
                    print(f"Event Name: {found_event[2]}")
                    print(f"Event Date: {found_event[3]}")

                    confirmation = input("Do you want to proceed with the deletion? (Yes/No): ").strip().lower()

                    if confirmation == "yes":
                        # Remove the event from the list
                        events_data.pop(i)

                        # Write the updated data back to the CSV file ('w' mode as we need to overwrite everything)
                        with open(event_filename, 'w', newline='') as csv_file:
                            event_writer = csv.writer(csv_file)
                            for event in events_data:
                                event_writer.writerow(event)

                        print("Event deleted successfully!")
                    elif confirmation == "no":
                        print("Deletion canceled.")
                    else:
                        print("Invalid input. Deletion canceled.")
                else:
                    print("Event not found with the given ID.")
        except FileNotFoundError:
            print("File not found.")

    # abstract methods
    @abstractmethod
    def add_event(self):
        pass


class Wedding(Event):
    def __init__(self, event_id, event_name, event_date, event_time, event_location, bride_and_groom):
        super().__init__(event_id, 'Wedding', event_name, event_date, event_time, event_location)
        self.bride_and_groom = bride_and_groom

    def add_event(self):
        self.event_id = Event.get_latest_id(self, event_filename) + 1  # Generate a unique event ID
        self.event_date = Event.get_valid_date_input(self)
        self.event_time = Event.get_valid_time_input(self)
        self.event_location = input("Enter event location: ").lower()
        self.event_location = self.event_location.replace(',', '')
        self.bride_and_groom = input(str('Enter the names of the bride and the groom: '))
        self.bride_and_groom = self.bride_and_groom.replace(',', '')
        self.event_name = f'wedding of {self.bride_and_groom}'

        try:
            with open(event_filename, 'a', newline='') as csvfile:  # Save the event to the CSV file
                event_writer = csv.writer(csvfile)
                event_writer.writerow(
                    [self.event_id, self.event_type, self.event_name, self.event_date, self.event_time,
                     self.event_location, self.bride_and_groom])
                print("Event added successfully!")
        except Exception as e:
            print(f"An error occurred while saving the event: {str(e)}")


class Birthday(Event):
    def __init__(self, event_id, event_name, event_date, event_time, event_location, celebrant):
        super().__init__(event_id, 'Birthday', event_name, event_date, event_time, event_location)
        self.celebrant = celebrant

    def add_event(self):
        self.event_id = Event.get_latest_id(self, event_filename) + 1  # Generate a unique event ID
        self.event_date = Event.get_valid_date_input(self)
        self.event_time = Event.get_valid_time_input(self)
        self.event_location = input("Enter event location: ").lower()
        self.event_location = self.event_location.replace(',', '')
        self.celebrant = input(str('Enter the name of the celebrant: '))
        self.event_name = f'birthday of {self.celebrant}'

        try:
            with open(event_filename, 'a', newline='') as csvfile:  # Save the event to the CSV file
                event_writer = csv.writer(csvfile)
                event_writer.writerow(
                    [self.event_id, self.event_type, self.event_name, self.event_date, self.event_time,
                     self.event_location, self.celebrant])
                print("Event added successfully!")
        except Exception as e:
            print(f"An error occurred while saving the event: {str(e)}")


class Business(Event):
    def __init__(self, event_id, event_name, event_date, event_time, event_location, business_host):
        super().__init__(event_id, 'Business', event_name, event_date, event_time, event_location)
        self.business_host = business_host

    def add_event(self):
        self.event_id = Event.get_latest_id(self, event_filename) + 1  # Generate a unique event ID
        self.event_name = input(str("Enter event name/title: "))
        self.event_date = Event.get_valid_date_input(self)
        self.event_time = Event.get_valid_time_input(self)
        self.event_location = input("Enter event location: ").lower()
        self.event_location = self.event_location.replace(',', '')
        self.business_host = input(str('Enter the name of the business host: '))

        try:
            with open(event_filename, 'a', newline='') as csvfile:  # Save the event to the CSV file
                event_writer = csv.writer(csvfile)
                event_writer.writerow(
                    [self.event_id, self.event_type, self.event_name, self.event_date, self.event_time,
                     self.event_location, self.business_host])
                print("Event added successfully!")
        except Exception as e:
            print(f"An error occurred while saving the event: {str(e)}")


class Attendee:  # IS-relationship (every attendee IS going to an event)
    def __init__(self, attendee_id, name, surname, email, phone, event_id_input):
        self.attendee_id = attendee_id
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.event_id_input = event_id_input

    def add_attendee(self):
        self.attendee_id = Event.get_latest_id(self, attendee_filename) + 1  # Generate a unique event ID
        self.name = input("Enter the attendee's first name: ")
        self.surname = input("Enter the attendee's surname: ")
        self.email = input("Enter the attendee's email: ")
        self.phone = input("Enter the attendee's phone: ")
        self.event_id_input = input("Enter the event ID they are attending: ")
        event_id_list = []
        # open the file and create a list with the event IDs.
        with open(event_filename, 'r', newline='') as csvfile:
            events_data = list(csv.reader(csvfile))
            for row in events_data:
                event_id_list.append(row[0])
        # validate the event id before adding the new attendee.
        while True:
            if self.event_id_input in event_id_list:
                # Create the attendee object
                new_attendee = Attendee(self.attendee_id, self.name, self.surname, self.email, self.phone,
                                        self.event_id_input)
                # Add the attendee to the CSV file
                with open('attendees.csv', 'a', newline='') as csvfile:
                    attendee_writer = csv.writer(csvfile)
                    attendee_writer.writerow(
                        [new_attendee.attendee_id, new_attendee.name, new_attendee.surname, new_attendee.email,
                         new_attendee.phone, new_attendee.event_id_input])
                break
            else:
                print('Event not found. Enter an existing event id')
                self.event_id_input = input("Enter the event ID they are attending: ")

        print("Attendee added to the event successfully!")

    def list_attendees_to_an_event(self):
        event_id = int(input("Enter the event ID to list attendees: "))

        try:
            with open('attendees.csv', 'r', newline='') as csvfile:
                attendees_data = list(csv.reader(csvfile))
                # Create a list with all the attendees going to that event
                event_attendees = [attendee for attendee in attendees_data if int(attendee[5]) == event_id]
                # if the ID is found, print the attendees.
                if event_attendees:
                    print(f"Attendees of Event ID {event_id}:\n")
                    for attendee in event_attendees:
                        print(f"Person ID: {attendee[0]}")
                        print(f"Name: {attendee[1]}")
                        print(f"Surname: {attendee[2]}")
                        print(f"Email: {attendee[3]}")
                        print(f"Phone: {attendee[4]}")
                        print("______________________")
                else:
                    print("No attendees found with the given event ID.")
        except FileNotFoundError:
            print("File not found.")

    def delete_attendee_from_event(self):
        attendee_id = int(input("Enter the personal ID of the attendee you want to delete: "))
        event_id = int(input("Enter the event ID from which you want to delete the attendee: "))

        try:
            with open('attendees.csv', 'r', newline='') as csvfile:
                attendees_data = list(csv.reader(csvfile))

                found_attendee = None

                # Find the attendee with the provided personal ID and event ID
                for i, attendee in enumerate(attendees_data):
                    if int(attendee[0]) == attendee_id and int(attendee[5]) == event_id:
                        found_attendee = attendee
                        break

                if found_attendee:
                    print(f"Personal ID: {found_attendee[0]}")
                    print(f"Name: {found_attendee[1]}")
                    print(f"Surname: {found_attendee[2]}")
                    print(f"Email: {found_attendee[3]}")
                    print(f"Phone: {found_attendee[4]}")
                    print("______________________")

                    confirmation = input("Do you want to proceed with the deletion? (Yes/No): ").strip().lower()

                    if confirmation == "yes":
                        # Remove the attendee from the list
                        attendees_data.pop(i)

                        # Write the updated data back to the CSV file ('w' mode as we need to overwrite everything)
                        with open('attendees.csv', 'w', newline='') as csvfile:
                            attendee_writer = csv.writer(csvfile)
                            attendee_writer.writerows(attendees_data)

                        print("Attendee deleted from the event successfully!")
                    elif confirmation == "no":
                        print("Deletion canceled.")
                    else:
                        print("Invalid input. Deletion canceled.")
                else:
                    print("Attendee not found with the given IDs.")
        except FileNotFoundError:
            print("File not found.")


class Menu:

    def display_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Add an event")
            print("2. Display all events")
            print("3. Display details of an event")
            print("4. Edit an event")
            print("5. Delete an event")
            print("6. Add an attendee to an event")
            print("7. List attendees of an event")
            print("8. Delete an attendee from an event")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                print('\nYou chose option 1: Add an event.')
                while True:
                    self.event_type = input("Enter event type (choose from wedding, birthday, business): ").lower()
                    if self.event_type == 'wedding':
                        Event.get_latest_id(self, event_filename)
                        Wedding.add_event(self)
                        break
                    elif self.event_type == 'birthday':
                        Event.get_latest_id(self, event_filename)
                        Birthday.add_event(self)
                        break
                    elif self.event_type == 'business':
                        Event.get_latest_id(self, event_filename)
                        Business.add_event(self)
                        break
                    else:
                        print("Unrecognized event_type. Please choose from the valid options.")

            elif choice == "2":
                print('\nYou chose option 2: List all events')
                Event.list_all_events(self)
                time.sleep(3)

            elif choice == "3":
                print('\nYou chose option 3: List an individual event')
                Event.display_individual_event(self)

            elif choice == "4":
                print('You chose option 4: Edit an event')
                Event.edit_event(self)

            elif choice == "5":
                print('You chose option 5: delete an event')
                Event.delete_event(self)

            elif choice == "6":
                print('You chose option 6: Add an attendee to an event')
                Attendee.add_attendee(self)

            elif choice == "7":
                print('You chose option 7: List attendees of an event')
                Attendee.list_attendees_to_an_event(self)

            elif choice == "8":
                print('You chose option 8: Delete an attendee from an event')
                Attendee.delete_attendee_from_event(self)

            elif choice == "0":
                print("Exiting the program. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")


# calling the Menu to start the program:
if __name__ == "__main__":  # checks if the script is being run directly as the main program or if it's being
    # imported as a module into another script
    menu = Menu()  # instantiation of the Menu class
    menu.display_menu()
