# importing nesscessary data to 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.patches import Patch

# Allows the function to read the EXCEL sheet
# Data gathered from "https://www.iqair.com/ca/canada/ontario/toronto"
df = pd.read_excel("C:\\Users\\ronni\\OneDrive\\Desktop\\Data\\TorontoAQI.xlsx",'Data')

# Convert datetime to date only 
df['Dates'] = pd.to_datetime(df['Dates']).dt.strftime('%Y-%m-%d')

# Prints out the Data of the excel file 
print(df)

# Stores values of excel column 
aqi = df
date=df['Dates']
print(date)
aqi=df['AQI']
print(aqi)
daytemp=df['Day Temp']
print(daytemp)
nighttemp=df['Night Temp']
print(nighttemp)
windspd=df['Wind speed (km/h)']
print(windspd)

# Shows the number of rows in an array
x=np.arange(len(date))
print(x)
# Bar chart width
w=0.5

plt.figure(figsize=(12,6))

# Set the colors of the AQI Level
colors = ['green' if aqi_values <= 50 else 
'yellow' if aqi_values <= 100 else
'orange' if aqi_values <=150 else
'red' if aqi_values <=200 else
'purple' if aqi_values <=250 else
'maroon' for aqi_values in aqi]

plt.bar(x,aqi,w,label='Air Quality Index',color=colors)

# Add labels to the x and y axis 
plt.xlabel('Dates')
plt.ylabel('AQI level')
plt.title('Toronto AQI Over Time')

# Changes the X axis name to the date index in excel sheet 
plt.xticks(x,date, rotation=45, ha='right')

# Add a legend indicting what the color of the bar means 
legend_elements = [
    Patch(facecolor='green', edgecolor='black', label='good (0-50)'),
    Patch(facecolor='yellow', edgecolor='black', label='moderate (51-100)'),
    Patch(facecolor='orange', edgecolor='black', label='unhealthy to targeted groups (101-150)'),
    Patch(facecolor='red', edgecolor='black', label='unhealthy (151-200)'),
    Patch(facecolor='purple', edgecolor='black', label='very unhealthy (201-300)'),
    Patch(facecolor='maroon', edgecolor='black', label='hazardous (301+)')
]

# Box that adds the level of pollutants 
pollutionlevel_text = "Pollution Levels: \nPM2.5: 22.1µg/m3\nPM10: 52.8µg/m3\nO3: 7.0 µg/m3\nNO2: 37.6µg/m3\nSO2: 0.1 µg/m3"
plt.gca().add_patch(plt.Rectangle((.75, 0.5), .2, .15, color='white', edgecolor='black', lw=1)) #BOX
plt.text(0.76, 0.2, pollutionlevel_text, fontsize = 11, verticalalignment='top', horizontalalignment='left', color='black', fontweight='bold')

# Add a custom legends to indicate the AQI
# Make room outside the graph for the legend 
plt.legend(handles=legend_elements, title="AQI Levels", loc='upper left', bbox_to_anchor=(1,1))
plt.tight_layout()

plt.show()