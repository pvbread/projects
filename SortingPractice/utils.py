import csv

# This code loads the current book
# shelf data from the csv file
def load_books(filename):
  bookshelf = []
  with open(filename) as file:
      shelf = csv.DictReader(file)
      for book in shelf:
  
          #prints the values which are in format 'Title', 'First,Last'
          split_book = book['title,author'].split(',')
          book['author_lower'] = split_book[1].lower()
          book['title_lower'] = split_book[0].lower()
          bookshelf.append(book)
          
  return bookshelf