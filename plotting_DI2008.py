import csv
import matplotlib.pyplot as plt 
import sys 
from collections import Counter

doc = sys.argv[1:]

if len(doc) > 1:
	print("Too long! Exiting program. Plot one at a time please.")
	sys.exit()

print("Plotting this file: {}".format(doc))

file = doc[0]

with open(file,'rb') as csvfile:

	csvreader = csv.reader(csvfile)

	all_data = []

	for line in csvreader:

		all_data.append(line) #take everything 

channel_annotations = all_data[3][1:] #Slice of "Time" heading, get channel annotations

all_EUs = all_data[4][1:-2] #slice off timestamps, etc, get just EU titles 

timestamps = [i[-1] for i in all_data[5:]] # get all time stamps 

all_data = [i[1:-2] for i in all_data[5:]] # slice off all headers, timestamps


EUs_counter = Counter(all_EUs)
EUs = []

print("Found these units to plot:")

for EU in EUs_counter:
	print EU
	EUs.append(EU)

#Plot one EU at a time 


indices = []

for EU in EUs: 
	indices.append([i for i in range(len(all_EUs)) if all_EUs[i] == EU]) #gets channel numbers for each EU in a list 

for index_list in indices: #loops as many times as there are discrete index lists 

	labels = [channel_annotations[i] for i in index_list]

	data = [] # make a new empty list each time 

	for data_point in all_data:

		data.append([data_point[i] for i in index_list]) #gets only the data points which have a column index of the current iteration of index_lists. Is lists of lists

	for i in range(len(data[0])): #loop as many times as there are data entry
		plt.plot([float(data[j][i]) for j in range(len(data))],label = labels[i]) #if there are 5 PSI channels, i goes from 0 to 5, and then plots through j in length of all data 

	plt.grid()
	plt.legend()
	plt.show()


