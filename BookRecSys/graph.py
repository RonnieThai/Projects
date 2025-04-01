#Create graphs to show data 
#What data : ?? 
from FileReader import get_cleaned_data
import matplotlib.pyplot as plt

#grab the data from FileReader.py and import it into graph.py
books, ratings, users, books_year_rational = get_cleaned_data()

#Create graph
plt.figure(figsize=(16, 9))

#Filter the graph
filtered_books = books_year_rational[books_year_rational.index >= 1900]

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
