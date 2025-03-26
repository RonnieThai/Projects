import pandas as pd
import seaborn as sns
import numpy as np
import warnings
import matplotlib.pyplot as plt
import os
import nltk

#Changes the directory path 
os.chdir(r'C:\Users\ronni\Python Project\BookRecSys')

#Allows panda to read the data from the csv Files
books = pd.read_csv('DataSets/Books.csv')
ratings = pd.read_csv('DataSets/Ratings.csv')
users = pd.read_csv('DataSets/Users.csv')

print(books.head())
print(ratings.head())
print(users.head())

print(books.shape)
print(ratings.shape)
print(users.shape)

#isna function detects missing value 
books.isna().sum()
