# import pandas as pd
# import datetime
# # New data to append
# data = {
#     "vehicleNumber": ["KA-01-HH-1234"],  # Wrap scalar value in a list
#     "vehicleName": ["Suzuki"],
#     "name": ["Rahul"],
#     "email": ["data@gmail.com"],
#     "phone": ["1234567890"],
#     "wheels": [4],
#     "stageId": [1],
#     "stageName": ["A"],
#     "slot": ["Slot 1"],
#     "datetime":[str(datetime.datetime.now())]
# }

# # Create DataFrame
# dt = pd.DataFrame(data)

# # Save to Excel
# dt.to_excel('./data.xlsx', index=False, engine='openpyxl')

# print("Data saved successfully!")

import pandas as pd

df=pd.read_json('./charge.json')
print(df["Car"]['baseCharge'])