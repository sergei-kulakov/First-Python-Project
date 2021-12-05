import pandas as pd, numpy as np
import math
import matplotlib.pyplot as plt
import sklearn
from sklearn import linear_model


data_raw = pd.read_csv("train.csv")
data = data_raw.drop(["PassengerId", "Name", "Ticket"], axis=1) #At this moment we do not need these columns
data['Sex'] = np.where(data['Sex'] == 'male', 1, 0)
colnames = data.columns #variable with names of the columns


#In this part I separate room and floor of people
current_floor = []
current_room = []
for i in data['Cabin']:
    current_string = str(i)
    if ' ' in current_string: #if an item has more than one element
        current_string = current_string[(current_string.index(" ") + 1):(current_string.index(" ") + 4)]
    elif (current_string == "nan"):
        current_floor.append("")
        current_room.append("")
        continue
    current_floor.append(ord(current_string[0]) % 32) #display floor as number
    current_room.append(current_string[1:3])

data = data.drop('Cabin', axis=1) #remove Cabin column
data = data.assign(Floor=current_floor, Room=current_room) #add modified data

#converting Port letter into number
embarked_ports = data['Embarked'].unique()
ports_matrix = np.zeros((len(data['Embarked']),3))
for j in range(len(data['Embarked'])):
    if str(data['Embarked'][j]) != "nan":
        current_index = int(np.where(embarked_ports == data['Embarked'][j])[0])
        ports_matrix[j, current_index] = 1
    else:
        ports_matrix[j,] = "nan"

#adding data back 
data = data.drop('Embarked', axis=1)
ports_matrix_reformed = pd.DataFrame(ports_matrix, columns=['Port 1', 'Port 2', 'Port 3'])
data_cleaned = pd.concat([data.reset_index(drop=True), ports_matrix_reformed], axis=1)

print(data_cleaned.Sex.unique())

#clf.fit(data_cleaned.drop('Survived', axis=1),data_cleaned['Survived'])

# filmat = np.zeros((len(colnames)-1,len(colnames)-1))
# for i in range(len(colnames[1:])):
#   for j in range(len(colnames[1:])):
#      print(np.corrcoef(data[colnames[i]],data[colnames[j]])[0,1])
