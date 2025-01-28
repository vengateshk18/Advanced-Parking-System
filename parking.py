import pandas as pd
import datetime

class ParkingStage:
    def __init__(self, stageId: int, stageName: str):
        self.left = None
        self.right = None
        self.stageId = stageId
        self.stageName = stageName

        # Initialize slots with a continuous numbering system
        slot_number = 1
        self.slots = []
        for __ in range(2):  # 2 rows
            row_slots = []
            for _ in range(3):  # 3 columns per row
                row_slots.append(f"Slot {slot_number}")
                slot_number += 1
            self.slots.append(row_slots)

    def __str__(self):
        return f'''  
        StageId: {self.stageId} StageName: {self.stageName}
        Slots:
          1. {self.slots[0][0]}
          2. {self.slots[0][1]}
          3. {self.slots[0][2]}
          4. {self.slots[1][0]}
          5. {self.slots[1][1]}
          6. {self.slots[1][2]}'''



class User:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
    def __str__(self):
        return f"Name: {self.name} Email: {self.email} Phone: {self.phone}"

class Vehicle:
    def __init__(self, vehicleNumber: str, vehicleName: str, name: str, email: str, phone: str, wheels: int):
        self.vehicleNumber = vehicleNumber
        self.vehicleName = vehicleName
        self.user = User(name, email, phone)
        self.entryTime = datetime.datetime.now()
        self.wheels=wheels
    def __str__(self):
        return f"Name: {self.vehicleName} Number: {self.vehicleNumber} User: {self.user} datetime: {self.entryTime} wheels: {self.wheels}"


class ParkingSystem:
    structure = None

    @staticmethod
    def createStages(stageIds,stageNames, start, end):
        if start > end:
            return None
        mid = (start + end) // 2
        root = ParkingStage(stageIds[mid], stageNames[mid])
        root.left = ParkingSystem.createStages(stageIds,stageNames, start, mid - 1)  
        root.right = ParkingSystem.createStages(stageIds,stageNames, mid + 1, end)  
        return root

    @staticmethod
    def loadData():
        df = pd.read_csv('./current.csv')
        ParkingSystem.structure = ParkingSystem.createStages(df['stageId'].values,df['stageName'].values ,0, len(df) - 1)
        print("Data Loaded Successfully")
    @staticmethod
    def printStructure(root):
        if not root:
            return
        ParkingSystem.printStructure(root.left)
        print(root)
        ParkingSystem.printStructure(root.right)
    
    @staticmethod
    def getParkingSlot(slot: ParkingStage, wheels: int):
        if not slot:
            return None
        
        # Check the left subtree
        data = ParkingSystem.getParkingSlot(slot.left, wheels)
        if data is not None:  # If a valid slot is found, stop and return
            return data

        # Check the current slot
        data = ParkingSystem.searchVehicle(slot, wheels)
        if data is not None:  # If the current slot matches, return it
            return data

        # Check the right subtree
        return ParkingSystem.getParkingSlot(slot.right, wheels)

    @staticmethod
    def searchVehicle(slot : ParkingStage, wheels : int):
        if wheels==2:
            for i in range(2):
                for j in range(3):
                    if slot.slots[i][j].startswith('Slot'):
                        return [slot,slot.stageId,slot.stageName,slot.slots[i][j]]
        elif wheels==4:
            for i in range(2):
                for j in range(2):
                    if slot.slots[i][j].startswith('Slot') and slot.slots[i][j+1].startswith('Slot'):
                        return [slot,slot.stageId,slot.stageName,slot.slots[i][j],slot.slots[i][j+1]]

        return None
                        
# Example Usage
ParkingSystem.loadData()



while True:
    print("Welcome to X Parking System")
    print("If you want to park your vehicle press 1")
    print("If you want to exit press 2")
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
        try:
            parkingdata = pd.read_excel('./data.xlsx')
        except FileNotFoundError:
            parkingdata = pd.DataFrame(columns=["vehicleNumber", "vehicleName", "name", "email", "phone", "wheels"])
        new_data = {
            "vehicleNumber": [vehicle.vehicleNumber],
            "vehicleName": [vehicle.vehicleName],
            "name": [vehicle.user.name],
            "email": [vehicle.user.email],
            "phone": [vehicle.user.phone],
            "wheels": [vehicle.wheels]
        }
        new_data = pd.DataFrame(new_data)
        combined_df = pd.concat([parkingdata, new_data], ignore_index=True)
        combined_df.to_excel('./data.xlsx', index=False, engine='openpyxl')
    elif choice == 2:
        print("Exiting the system.")
        break