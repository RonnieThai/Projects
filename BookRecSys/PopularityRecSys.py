from FileReader import get_cleaned_data
import pandas as pd
import seaborn as sns
import numpy as np
import warnings
import matplotlib.pyplot as plt
import os
import nltk

#grab the data from FileReader.py and import it into PopularityRecSys.py
books, ratings, users, books_years_rational, author_book_count_top50, publisher_top50, ratings_sorted, top20_ratings = get_cleaned_data()

def popularity_based_system():
    
    def filter_by_rating_threshold(df, min_ratings, sort=False, top_n=None):
        filtered = df[df['Number-of-Ratings'] >= min_ratings]
        if sort:
            filtered = filtered.sort_values(by='Average-Rating', ascending=False)
        if top_n:
            return filtered.head(top_n)
        return filtered
    
    ratings_books_merged = ratings.merge(books, on='ISBN')
    print(ratings_books_merged.head())
    ratings_books_merged.shape
    
    #Get the number of votes for each books
    ratings_books_nonzero = ratings_books_merged[ratings_books_merged['Book-Rating']!=0]
    num_rating_df = ratings_books_nonzero.groupby('Book-Title').count()['Book-Rating'].sort_values(ascending=False).reset_index()
    num_rating_df.rename(columns={'Book-Rating':'Number-of-Ratings'}, inplace=True)
    print(num_rating_df)
    
    #Average Rating
    avg_rating_df = ratings_books_nonzero.groupby('Book-Title').mean(numeric_only=True)['Book-Rating'].reset_index()
    avg_rating_df.rename(columns={'Book-Rating':'Average-Rating'}, inplace=True)
    avg_rating_df.head()
    
    #Merging the avg rating with most amount
    popularity_df = pd.merge(num_rating_df, avg_rating_df, on='Book-Title')
    popularity_df
    
    #Taking the books with ratings above 100
    popularity_df_above_50 = filter_by_rating_threshold(popularity_df, 50)
    popularity_df_above_100 = filter_by_rating_threshold(popularity_df, 100)
    popularity_df_above_250 = filter_by_rating_threshold(popularity_df, 250)
    