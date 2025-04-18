#Create graphs to show data 
#What data : ?? 
from FileReader import get_cleaned_data
import matplotlib.pyplot as plt
import seaborn as sns

#grab the data from FileReader.py and import it into graph.py
books, ratings, users, books_years_rational, author_book_count_top50, publisher_top50, ratings_sorted, top20_ratings = get_cleaned_data()

def books_published():
    #Create graph
    plt.figure(figsize=(16, 9))

    #Filter the graph
    filtered_books = books_years_rational[books_years_rational.index >= 1900]

    bars = plt.bar(x=filtered_books.index, height=filtered_books.values)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, '{:.0f}'.format(height), ha='center', va='bottom', rotation=45, fontsize=8)

    plt.xticks(rotation=45, fontsize=10)
    plt.title("Number of Books Published Yer Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.show()
    plt.close()
    
def top_authors():
    cool = sns.color_palette("cool", n_colors=len(author_book_count_top50.values))
    
    plt.figure(figsize=(12,12))
    
    sns_plot = sns.barplot(y=author_book_count_top50.index, 
                           x=author_book_count_top50.values, palette=cool, orient='h', hue=None)
    
    for i, value in enumerate(author_book_count_top50.values):
        sns_plot.text(value, i, int(value), ha="left", va="center", color='black', fontsize=8)
        
    plt.ylabel("Author Names", fontsize=12)
    plt.xlabel("Number of Books Written", fontsize=12)
    plt.title("Top 50 Author With Most Amount of Books Written", fontsize=14)
    
    plt.yticks(rotation=0, fontsize=10)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.05)
    
    plt.tight_layout()
    plt.show()
    plt.close()
    
def top_publisher():
    cool = sns.color_palette("cool", n_colors=len(publisher_top50.values))
    
    plt.figure(figsize=(12,12))
    
    sns_plot = sns.barplot(y=publisher_top50.index,
                           x=publisher_top50.values, palette=cool, hue=publisher_top50.index, dodge=False, legend=False, orient='h' )
    
    for i, values in enumerate(publisher_top50.values):
        sns_plot.text(values, i, int(values), ha="left", va="center", color='black', fontsize=8)
        
    plt.ylabel("Publisher Names")
    plt.xlabel("Number of Books Published")
    plt.title("Top 50 Publisher With Most Amount of Published Books")
    
    plt.yticks(rotation=0, fontsize=10)
    
    plt.tight_layout()
    plt.show()
    plt.close()
   
def average_ratings():
    cool = sns.color_palette("cool", n_colors=len(ratings_sorted.values))
    
    plt.figure(figsize=(24,24))
    ratings_sorted_0_excluded = ratings_sorted.drop(index= 0.0).sort_index(ascending=False)
    sns_plot = sns.barplot(x=ratings_sorted_0_excluded.index,
                           y=ratings_sorted_0_excluded.values,
                           palette=cool, dodge=False, legend=False)
    
    plt.xticks(rotation=90)
    plt.xlabel("Number of Books")
    plt.ylabel("Average Rating")
    plt.title("Average Rating")
    plt.tight_layout()
    plt.show()

def top_rated_books():
    plt.figure(figsize=(12,10))
    plt.pie(top20_ratings, labels=top20_ratings.index, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
    plt.title("Distribution of rated books", pad=20)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.1)
    plt.tight_layout()
    plt.show()
    
#top_authors()
#top_publisher()
#average_ratings()
top_rated_books()