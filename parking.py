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
    def getParkingSlot(stage: ParkingStage, wheels: int):
        if not stage:
            return None
        
        # Check the left subtree
        data = ParkingSystem.getParkingSlot(stage.left, wheels)
        if data is not None:  # If a valid slot is found, stop and return
            return data

        # Check the current slot
        data = ParkingSystem.findBestSlot(stage, wheels)
        if data is not None:  # If the current slot matches, return it
            return data

        # Check the right subtree
        return ParkingSystem.getParkingSlot(stage.right, wheels)

    @staticmethod
    def findBestSlot(stage : ParkingStage, wheels : int):
        if wheels==2:
            for i in range(2):
                for j in range(3):
                    if type(stage.slots[i][j])==str and stage.slots[i][j].startswith('Slot'):
                        return [stage,int(stage.stageId),stage.stageName,stage.slots[i][j],i,j]
        elif wheels==4:
            for i in range(2):
                for j in range(2):
                    if type(stage.slots[i][j])==str and type(stage.slots[i][j+1])==str and stage.slots[i][j].startswith('Slot') and stage.slots[i][j+1].startswith('Slot'):
                        return [stage,stage.stageId,stage.stageName,stage.slots[i][j],stage.slots[i][j+1],i,j,j+1]
        return None
    @staticmethod
    def placeVehicle(stage: ParkingStage, stageRow : int, stageColumn : int, vehicle: Vehicle):
        stage.slots[stageRow][stageColumn] = vehicle

    @staticmethod
    def searchVehicle(vehicleNumber: str):
        parkedData=pd.read_excel('./data.xlsx')
        if vehicleNumber in parkedData['vehicleNumber'].values:
            return parkedData[parkedData['vehicleNumber']==vehicleNumber]
        else:
            return None
    @staticmethod
    def chargeVehicle(vehicleData: pd.DataFrame):
        vehicleData['exit']=str(datetime.datetime.now())
        vehicleData['exit']=pd.to_datetime(vehicleData['exit'])
        vehicleData['datetime']=pd.to_datetime(vehicleData['datetime'])
        vehicleData['duration']=(vehicleData['exit']-vehicleData['datetime']).dt.total_seconds()/3600
        charge=pd.read_json('./charge.json')
        if vehicleData['wheels'].values==2:
            return charge['Bike']['baseCharge']+charge['Bike']['chargePerHour']*vehicleData['duration']
        else:
            return charge['Car']['baseCharge']+charge['Car']['chargePerHour']*vehicleData['duration']
        return None
            
        
                        
# Example Usage
ParkingSystem.loadData()