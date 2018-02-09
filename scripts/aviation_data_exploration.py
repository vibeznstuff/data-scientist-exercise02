import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Import flattened CSV census data into dataframe
df = pd.read_csv('../output/Full_Aviation_Data.csv')

print(df.head())

#Sort out numeric and categorical fields for processing
exclude_vars = ['EventId','AccidentNumber','EventDate','RegistrationNumber','Unnamed: 0','narrative','probable_cause','AirportName','AirportCode','Location','Model','Make','PublicationDate','AirCarrier','Country','Latitude','Longitude']
numeric_vars = list(df._get_numeric_data().columns)
numeric_vars = [field for field in numeric_vars if field not in exclude_vars]
cat_vars = [col for col in df.columns if col not in numeric_vars and col not in exclude_vars]

print("Numeric Vars:  ")
print(numeric_vars)
print("\n")
print("Categorical Vars:  ")
print(cat_vars)

sns.set_style("whitegrid")

#Create one-way frequencies for categorical vars
for cat_var in cat_vars:
	f, ax = plt.subplots(figsize=(12,12))
	plt.title(cat_var+' frequencies')
	sns.countplot(y=cat_var, data=df, color="c")
	plt.savefig('../output/figs/freqs/'+cat_var+'_freqs.png', bbox_inches='tight')
	plt.close()
	print(cat_var + " number of factors: " + str(len(df[cat_var].value_counts())))
	
#Display by category the relative frequencies by Aircraft Damage
for cat_var in cat_vars:
	f, ax = plt.subplots(figsize=(12,12))
	plt.title(cat_var+' frequencies')
	sns.countplot(y=cat_var, hue="AircraftDamage", data=df)
	plt.savefig('../output/figs/by_aircraft_damage/'+cat_var+'_by_aircraftdamage.png', bbox_inches='tight')
	plt.close()
	
#Create histograms for numeric vars
for numeric_var in numeric_vars:
	print(numeric_var)
	f, ax = plt.subplots(figsize=(12,12),nrows=3)
	minor=df[df.AircraftDamage == 'Minor']
	substantial=df[df.AircraftDamage == 'Substantial']
	destroyed=df[df.AircraftDamage == 'Destroyed']
	ax[0].title.set_text('Minor: ' + numeric_var+' histogram')
	sns.distplot(minor[numeric_var].dropna(),norm_hist=True,ax=ax[0])
	ax[1].title.set_text('Substantial: ' + numeric_var+' histogram')
	sns.distplot(substantial[numeric_var].dropna(),norm_hist=True,ax=ax[1])
	ax[2].title.set_text('Destroyed: ' + numeric_var+' histogram')
	sns.distplot(minor[numeric_var].dropna(),norm_hist=True,ax=ax[2])
	plt.savefig('../output/figs/histograms/'+numeric_var+'_hist.png', bbox_inches='tight')
	plt.close()