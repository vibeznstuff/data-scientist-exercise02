from lxml import etree
import csv
from unidecode import unidecode

#Load Aviation Data XML file
tree = etree.parse("../data/AviationData.xml")
tmp_root = tree.getroot()

#Pull XML text associated with child node ROWS
xml_str = etree.tostring(tmp_root.getchildren()[0])

#Create functional XML instance in etree
root = etree.fromstring(xml_str)

#List of variable names
aviation_vars = ['EventId','InvestigationType','AccidentNumber','EventDate','Location','Country','Latitude','Longitude','AirportCode','AirportName','InjurySeverity','AircraftDamage','AircraftCategory','RegistrationNumber','Make','Model','AmateurBuilt','NumberOfEngines','EngineType','FARDescription','Schedule','PurposeOfFlight','AirCarrier','TotalFatalInjuries','TotalSeriousInjuries','TotalMinorInjuries','TotalUninjured','WeatherCondition','BroadPhaseOfFlight','ReportStatus','PublicationDate']

#Open new csv outfile...
out_file = csv.writer(open('../output/AviationData.csv','w',newline=''))

#Add column headers to csv
out_file.writerow(aviation_vars)

#Start writing rows to CSV file
for row in root.iter():
	tmp_lst = []
	for var in aviation_vars:
		#Convert None value to blank
		if row.get(var) is None:
			val = ""
		else:
			val = unidecode(row.get(var))
		tmp_lst.append(val)
	#Comma separated values from XML file by field
	#Missing values translated as blanks
	out_file.writerow(tmp_lst)