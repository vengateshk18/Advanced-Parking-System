import pandas as pd
import datetime

from parking import Vehicle, User, ParkingStage, ParkingSystem

while True:
    print("Welcome to X Parking System")
    print("If you want to park your vehicle press 1")
    print("If you want to get your vehicle press 2")
    print("If you want to exit press 3")
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        # Collect vehicle details
        print("Enter the vehicle details")
        vehicleNumber = input("Enter the vehicle number in proper format (e.g., KA-01-HH-1234): ")
        vehicleName = input("Enter the vehicle name: ")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone: ")
        wheels = int(input("Enter the number of wheels in your vehicle: "))
        vehicle = Vehicle(vehicleNumber, vehicleName, name, email, phone, wheels)
        slot=ParkingSystem.getParkingSlot(ParkingSystem.structure, wheels)
        print(slot)
        if not slot:
            print("No slot available for your vehicle")
            print("Thanks for visiting")
            continue
        else:
            ParkingSystem.placeVehicle(slot[0],slot[4],slot[5],vehicle)
            print(f"Your vehicle is parked at {slot[0].stageName} and slot number is {slot[3]}")

        try:
            parkingdata = pd.read_excel('./data.xlsx')
        except FileNotFoundError:
            parkingdata = pd.DataFrame(columns=["vehicleNumber", "vehicleName", "name", "email", "phone", "wheels","stageId","stageName","slot","datetime"])
        new_data = {
            "vehicleNumber": [vehicle.vehicleNumber],
            "vehicleName": [vehicle.vehicleName],
            "name": [vehicle.user.name],
            "email": [vehicle.user.email],
            "phone": [vehicle.user.phone],
            "wheels": [vehicle.wheels],
            "stageId": [slot[0].stageId],
            "stageName": [slot[0].stageName],
            "slot": [slot[3]],
            "datetime":str(datetime.datetime.now())
        }
        new_data = pd.DataFrame(new_data)
        combined_df = pd.concat([parkingdata, new_data], ignore_index=True)
        combined_df.to_excel('./data.xlsx', index=False, engine='openpyxl')
    elif choice==2:
        print("Enter the vehicle details")
        vehicleNumber = input("Enter the vehicle number in proper format (e.g., KA-01-HH-1234): ")
        vehicleData=ParkingSystem.searchVehicle(vehicleNumber)
        if vehicleData is None:
            print("Vehicle not found or invalid vehicle number")
            continue
        print(vehicleData)
        name=input("Enter the name: ")
        phone=int(input("Enter the phone number: "))
        if name==vehicleData["name"].iloc[0] and phone==vehicleData["phone"].iloc[0]:
            print("Vehicle removed successfully")
            charge=ParkingSystem.chargeVehicle(vehicleData)
            print("Total charge is ",charge)
        else:
            print("Invalid name or phone number")
    elif choice == 3:
        print("Exiting the system.")
        break