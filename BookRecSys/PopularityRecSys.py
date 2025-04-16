from FileReader import get_cleaned_data
import pandas as pd
import seaborn as sns
import numpy as np
import warnings
import matplotlib.pyplot as plt
import os
import nltk
from sklearn.metrics.pairwise import cosine_similarity

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
    
    def calc_weighted_rating(row, avgRating, numOfRatings, minThres, defRating):
        weighted_rating = ((row[avgRating] * row[numOfRatings]) + (minThres * defRating)) / (row[numOfRatings] + minThres)
        return weighted_rating
        
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
    
    top_popular_books = filter_by_rating_threshold(popularity_df, 100, sort=True, top_n=5)
    print(top_popular_books)
    
    #Number of Ratings above 100
    popularity_df_above_100 = filter_by_rating_threshold(popularity_df, 100)
    popularity_df_above_100['Weighted-Rating'] = popularity_df_above_100.apply(
        lambda x: calc_weighted_rating(x, 'Average-Rating', 'Number-of-Ratings', 100, 5),
        axis=1
    )
    
    top_weighted_books = popularity_df_above_100.sort_values('Weighted-Rating', ascending=False).head(20)
    #print(top_weighted_books)
    
    # Number of Rating above 50
    popularity_df_above_50 = filter_by_rating_threshold(popularity_df, 50)
    popularity_df_above_50['Weighted-Rating'] = popularity_df_above_50.apply(
        lambda x: calc_weighted_rating(x, 'Average-Rating', 'Number-of-Ratings', 50, 5),
        axis=1
    )
    
    popularity_df_above_50.sort_values('Weighted-Rating', ascending=False).head(20)
    
    #Number of Rating above 250
    popularity_df_above_250 = filter_by_rating_threshold(popularity_df, 250)
    popularity_df_above_250['Weighted-Rating'] = popularity_df_above_250.apply(
        lambda x: calc_weighted_rating(x, 'Average-Rating', 'Number-of-Ratings', 250, 5),
        axis=1
    )
    
    popularity_df_above_250.sort_values('Weighted-Rating', ascending=False).head(20)
    
    #merge any rating above 250 with the data frame
    popularity_df_merge = pd.merge(popularity_df_above_100, books, on='Book-Title').drop_duplicates('Book-Title', keep='first')
    popularity_df_merge = popularity_df_merge.drop(columns=['Image-URL-S', 'Image-URL-L'])
    print(popularity_df_merge.shape)
    popularity_df_merge.sort_values('Weighted-Rating', ascending=False).head(10)
    
    #Show the top rated books
    ratings_books_merged.head()
    
    #Filter the users with 200 votes
    users_rating_count = ratings_books_merged.groupby('User-ID').count()['ISBN']
    users_rating_count = users_rating_count.sort_values(ascending=False).reset_index()
    users_rating_count.rename(columns={'ISBN':'No-of-Books-Rated'}, inplace=True)
    print(users_rating_count.shape)
    users_rating_count.head()
    
    users_200 = users_rating_count[users_rating_count['No-of-Books-Rated']>=200]
    print(users_200.shape)
    
    books_with_users_200 = pd.merge(users_200, ratings_books_merged, on='User-ID')
    print(books_with_users_200.shape)
    books_with_users_200.head()    
    
    #Filter books with more than 50 ratings 
    print(ratings_books_merged.shape)
    ratings_books_merged.head()
    
    books_rating_count = ratings_books_merged.groupby('Book-Title').count()['ISBN'].sort_values(ascending=False).reset_index()
    books_rating_count.rename(columns={'ISBN' : 'Number-of-Rated-Books'}, inplace=True) #If doesnt work change 'Number-of-Rated-Books' to 'Number-of-Book-Ratings'
    books_rating_count.head()
    
    books_ratings_50 = books_rating_count[books_rating_count['Number-of-Rated-Books']>=50] #If doesnt work change 'Number-of-Rated-Books' to 'Number-of-Book-Ratings'
    print(books_ratings_50)
    books_ratings_50.head()
    
    #Filter
    filtered_books = pd.merge(books_ratings_50, books_with_users_200, on="Book-Title")
    print(filtered_books.columns)
    filtered_books.head()
    
    popular_books = filtered_books.groupby('Book-Title').count().reset_index()
    popular_books = popular_books['Book-Title']
    popular_books = books[books['Book-Title'].isin(popular_books)]
    popular_books = popular_books.copy()
    popular_books.drop_duplicates(subset=['Book-Title'], inplace=True, keep='first')
    print(popular_books)
    
    pt = filtered_books.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
    pt.fillna(0, inplace=True)
    print(pt)
    
    #Model Creation
    #Turn the books to vectors
    similarites = cosine_similarity(pt)
    similarites
    similarites.shape
    
    #Retrieve index
    np.where(pt.index=='1984')
    np.where(pt.index=='stardust')[0][0]
    
    #Index to find array
    #First movie in the index table
    print(similarites[0])
    similarites[np.where(pt.index=='stardust')[0][0]]
    
    #sort the array recieved
    list(enumerate(similarites[0]))
    
    #Sort without index
    sorted(list(enumerate(similarites[0])), key=lambda x: x[1], reverse=True)
    
    #Remove the first item we selected from top5
    sorted(list(enumerate(similarites[0])), key=lambda x: x[1], reverse=True)[1:6]
    
    #display the top 5
    for book in sorted(list(enumerate(similarites[0])), key=lambda x: x[1], reverse=True)[1:6]:
        print(book[0])
        
    for book in sorted(list(enumerate(similarites[0])), key=lambda x: x[1], reverse=True)[1:6]:
        print(pt.index[book[0]])
        
    if 'hamkmfa' in pt.index:
        np.where(pt.index=='hamkda')[0][0]
    else:
        print('Book Not Found')
          
        
popularity_based_system()