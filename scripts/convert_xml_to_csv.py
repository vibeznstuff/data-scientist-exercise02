from lxml import etree

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
with open('../output/AviationData.csv','w+') as out_file:
	#Add column headers to csv
	out_file.write('event_id,investigation_type,accident_number,event_date,location,country,latitude,longitude,airport_code,airport_name,injury_severity,aircraft_damage,aircraft_category,registration_number,make,model,amateur_built,number_of_engines,engine_type,far_desc,schedule,purpose_of_flight,air_carrier,total_fatal_injuries,total_serious_injuries,total_minor_injuries,total_uninjured,weather_condition,broad_phase_of_flight,report_status,publication_date\n')
	#Execute SQL script and begin writing to out_file
	for row in root.iter():
		tmp_lst = []
		for var in aviation_vars:
			#Convert None value to blank
			if row.get(var) is None:
				val = ''
			else:
				val = row.get(var)
			tmp_lst.append(val.replace(","," -"))
		#Comma separated values from XML file by field
		#Missing values translated as blanks
		row_text = str(tmp_lst)[1:-1].replace("'","")
		out_file.write(row_text + '\n')
out_file.close()