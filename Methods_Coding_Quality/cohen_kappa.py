from sklearn.metrics import cohen_kappa_score
import pandas as pd

df = pd.read_excel(r"..\..\DataSources\kappa_reviewed.xlsx")
x=df["Reviewer2"].apply(str) 
y=df["Reviewer1"].apply(str) 


print(cohen_kappa_score(x,y))