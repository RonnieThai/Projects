#Read the data from the csv files of User, Rating, and Book
#Fix any missing or incorrect data 
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
books.loc[118033, 'Book-Title']
books.loc[187689, 'Book-Title']

#Add the missing author to those books
books.loc[118033, 'Book-Author'] = 'Downes, Larissa Anne'

#Get rid of index 187689 due to no author 
books = books.drop(index=187689).reset_index(drop=True)

#recheck If there are any missing values 
print(books.isna().sum())

#Get the user data
print("\nUsers Data:")
print(users.isna().sum())

#get the users age column 
users.drop(columns=['Age'], inplace=True)
print("\n", ratings.isnull().sum())

#check for duplicate values 
print(books.duplicated().sum())
print(users.duplicated().sum())
print(ratings.duplicated().sum())

#Perform EDA
print(books.head)
print(books.dtypes)

#>> FIX 67 - 74 IF ANY PROBLEM OCCURS 
#Fix incorrect year of publication
#books.loc[209538]
#print(books.loc[209538, 'Book-Title'])
#books.loc[209538, 'Year-Of-Publication']

#books.loc[220731]

#books.loc[221678]

invalid_years = books[pd.to_numeric(books['Year-Of-Publication'], errors='coerce').isna()]
print("Invalid Year-Of-Publication entries:")
print(invalid_years[['Book-Title', 'Year-Of-Publication']])

books['Year-Of-Publication'] = pd.to_numeric(books['Year-Of-Publication'], errors='coerce').fillna(0).astype('int64')

print("\nAfter fixing, unique years are:")
print(books['Year-Of-Publication'].unique())

books['Year-Of-Publication'].value_counts().sort_index(ascending=False).loc[:20]

#Check to see if any publish dates are incorrect
print(books[books['Year-Of-Publication']>2021][['Book-Title', 'Year-Of-Publication', 'Publisher', 'Book-Author']])

print(books.loc[37487, 'Book-Title'])
print(books.loc[55676, 'Book-Title'])
print(books.loc[80264, 'Book-Title'])
print(books.loc[118294, 'Book-Title'])
print(books.loc[192992, 'Book-Title'])

books.loc[[37487, 55676, 78168, 80264, 97826, 116053, 118294, 192992, 228172, 240168, 246841, 255408, 260973]
          , 'Year-Of-Publication'] = [1991, 2005, 2003, 2003, 2001, 1981, 1995, 2023, 1987, 1996, 1925, 1937, 1991]
books.loc[37487, 'Book-Author'] = 'Bruce Coville'