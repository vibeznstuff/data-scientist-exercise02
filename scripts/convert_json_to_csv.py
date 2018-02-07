import json, csv, os
from unidecode import unidecode

#Create new output file for NarrativeData CSV data
f = open("../output/NarrativeData.csv","w")
f.close()

#Function for appending JSON NarrativeData to CSV file
#by file name
def import_narrative_data(filename):
	#Load sample Narrative Data JSON file
	event_ids = json.load(open("../data/"+filename))['data']

	#List of variable names
	narrative_vars = ['EventId','narrative','probable_cause']

	#Open new csv outfile...
	out_file = csv.writer(open('../output/NarrativeData.csv','a',newline=''))

	#Add column headers to csv
	out_file.writerow(narrative_vars)

	#Start writing rows to CSV file
	for event in event_ids:
		tmp_lst = []
		for var in narrative_vars:
			tmp_lst.append(unidecode(event[var]))
			
		#Comma separated values from XML file by field
		#Missing values translated as blanks
		out_file.writerow(tmp_lst)

#Iteratively run import_narrative_data function
#by looping over NarrativeData files
for file in os.listdir("../data/"):
	if "NarrativeData" in file:
		import_narrative_data(file)
	
