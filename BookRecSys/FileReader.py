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

# Checks for missing values
print("\nMissing values in books DataFrame:")
print(books.isna().sum())

# Checks for rows where the author is missing 
print("\nRows with missing Book-Author:")
missing_authors = books[books['Book-Author'].isna()]
print(missing_authors)

#Locate the missing values of books
books.iloc[118033]['Book-Title']
books.iloc[187689]['Book-Title']

#Add the missing author to those books
books.iloc[118033]['Book-Title'] = 'Downes, Larissa Anne'

#Get rid of index 187689 due to no author 
books = books.drop(index=187689)
books = books.reset_index(drop=True)