import numpy as np
import networkx as nx
import matplotlib.py as plt  
from PopularityRecSys import pt, similarites

def recommend(book_name):
    if book_name in pt.index:
        index = np.where(pt.index == book_name)[0][0]
        similar_books_list = sorted(
            list(enumerate(similarites[index])), key=lambda x: x[1], reverse=True)[1:11]
        
        recommended_books = [pt.index[book[0]] for book in similar_books_list]
        similarity_scores = [book[1] for book in similar_books_list]
        
        print(f'Recommendations for the book {book_name}:')
        print('-'*5)
        for book in recommended_books:
            print(book)
        
        #create graph
        G = nx.Graph()
        
        #add the nodes to the graph
        G.add_node(book_name)
        for book, score in zip(recommended_books, similarity_scores):
            G.add_node(book)
            G.add_edge(book_name, book, weight=score)
        
        #Draw the graph out
        pos = nx.spring_layout(G, k=0.5, iterations=20)
        plt.figure(figsize=(12,8))
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=3000, font_size=10, font_weight='bold', edge_color='black')
        
        #Labels
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        plt.title(f'Book Recommendation Network for: {book_name}')
        plt.show()
        print('\n')
        
    else:
        print('Book Not Found')
        print('\n')
       