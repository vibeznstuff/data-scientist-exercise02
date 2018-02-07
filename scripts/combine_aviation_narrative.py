import pandas as pd, numpy as np

#Import Aviation Data
aviation = pd.read_csv('../output/AviationData.csv')

#Import Narrative Data
narrative = pd.read_csv('../output/NarrativeData.csv')

full_data = aviation.merge(right=narrative,how='left',left_on=["EventId"],right_on=["EventId"],sort=True)

print(len(aviation))
print(len(narrative))
print(len(full_data))
print(full_data.head())

#Write full aviation data frame output to csv for storage
full_data.to_csv("../output/Full_Aviation_Data.csv")