# Import tabulate module & SQLite Module
from tabulate import tabulate
import sqlite3

# Create a Database and determine where it will be stored
db = sqlite3.connect('Data/ebookstore_db')

# Get a cursor object
cursor = db.cursor()

# Create a table and add the columns to include plus there Data types and establish a Primary Key
cursor.execute('''
        CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER) 
        ''')
db.commit()  # Commit these changes to the database

# Create a list to store book data you want to put in the table
book_info = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
             (3002, 'Harry Potter and the Philosopher\'s\' Stone', 'J.K.Rowling', 40),
             (3003, 'The Lion the Witch and the Wardrobe', 'C.S. Lewis', 25),
             (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
             (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

# Use the executemany module to add multiple rows to the table
cursor.executemany(''' INSERT OR IGNORE INTO books(id, Title, Author, Qty) VALUES(?, ?, ?, ?)''',
                   book_info)
db.commit()     # Commit these changes to the database


# ========The beginning of the Book class==========
class Book:
    """
    This Class is for all the books in the database to be able to retrieve certain information
    about each book easily.
    """

    def __init__(self, book_id, title, author, qty):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.qty = qty

    def get_id(self):
        return int(self.book_id)

    def get_quantity(self):
        return int(self.qty)

    def __str__(self):
        return f"{self.book_id}, {self.title}, {self.author}, {self.qty}"


# ========Functions outside the Class==========
def list_of_books():
    """
    This function creates a list of all the books in the database
    and assigns them to the Book class
    """
    book_list = []
    cursor.execute('''SELECT * FROM books''')       # this takes all the information from the table for each row
    for book in cursor:
        book_list_item = Book(book[0], book[1], book[2], book[3])   # iterate through each book and assign to Book class
        book_list.append(book_list_item)     # append all these books to the empty list

    return book_list    # This function returns the full list of books from the database


def view_database():
    """
    This Function Creates a table of all the books in the database and displays them to the user
    """
    table = []  # create an empty table to append list of lists to use tabulate module
    for i in range(len(list_of_books())):  # Iterate through each element in list of books
        table_element = [list_of_books()[i].book_id, list_of_books()[i].title,
                         list_of_books()[i].author, list_of_books()[i].qty]
        table.append(table_element)  # append the list to have list of lists
    headers = ["id", "Title", "Author", "qty"]  # Create headers for the table
    print(tabulate(table, headers, tablefmt="rounded_grid"))  # Create the table in an easy-to-read manner


def add_book():
    """
    This Function adds a new book to the database and also
    adds this book to the table of books imported into this program
    """
    new_book_id = list_of_books()[-1].book_id + 1     # Create new id for this book that is 1 higher than the last book
    new_book_title = input("What is the Book Title? ")   # Get the book info from the user
    new_book_author = input("Who is the Author of this book? ")
    while True:
        try:
            new_book_qty = int(input("How many copies of the book do you have? "))  # Gather the quantity of this book

            cursor.execute('''INSERT INTO books(id, Title, Author, qty) VALUES(?, ?, ?, ?)''',
                           (new_book_id, new_book_title, new_book_author, new_book_qty))   # Add row into the database

            db.commit()   # commit these changes

            print(f"\n{new_book_title} has been added to the Database.")    # Let the user know this has been added.
            break

        except ValueError:
            print("\nOops! That was not a valid number, try again!")   # displays error if the user enters invalid no.


def update_book_info():
    """
    This function can update the Author, Title and Quantity values in the book database
    and in turn appends these changes into the list of books.
    """
    view_database()   # This Displays the table of the list of books
    while True:
        try:
            # Find out what book the user wants to update
            determine_which_book = int(input("\nWhat is the id of the book would you like to update? "))
            list_of_book_id = []   # Crete an empty list to store all the book ids
            for book_ in list_of_books():
                list_of_book_id.append(book_.book_id)   # loop through and append the book ids to the empty list
            if determine_which_book not in list_of_book_id:   # if book id isn't in list display error message and loop
                print("\nThis book is not in the database. please try again.")
            else:
                while True:   # If the id is in the list present user with menu of choices
                    what_to_change = input('''\nWhat do you want to update?
            Please Select one of the following options:  
            T  - The book Title
            A  - The books Author
            Q  - The Quantity of the book 
                    : ''').lower()

                    if what_to_change == "t":  # This if statement will update the Title of selected book
                        update_book_title = input("\nWhat is the book's updated Title? ")

                        cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''',
                                       (update_book_title, determine_which_book))

                        db.commit()

                        print("\nThe book Title has been updated.\n")
                        break

                    elif what_to_change == "a":  # This if statement will update the Author of selected book
                        update_book_author = input("\nWhat is the book's updated Author? ")

                        cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''',
                                       (update_book_author, determine_which_book))

                        db.commit()

                        print("\nThe book Author has been updated.\n")
                        break

                    elif what_to_change == "q":  # This if statement will update the Quantity of selected book
                        update_book_title = int(input("\nWhat is the book's updated Quantity? "))

                        cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''',
                                       (update_book_title, determine_which_book))

                        db.commit()

                        print("\nThe book quantity has been updated.\n")
                        break

                    else:   # if option the user selects is not valid they will get this error message
                        print("\nPlease enter a valid option.\n")
                break
        except ValueError:  # if the id the user selects isn't valid the program will present this error message
            print("\nOops! That was not a valid id number, try again!")


def delete_book():
    """
    This Function deletes a book from the database
    """
    view_database()   # This Displays the table of the list of books
    while True:
        try:
            #  Determine which book the user would like to delete
            which_book_to_delete = int(input("\nWhat is the id of the book would you like to delete? "))
            list_of_book_id = []  # Crete an empty list to store all the book ids
            for book_ in list_of_books():
                list_of_book_id.append(book_.book_id)  # loop through and append the book ids to the empty list
            if which_book_to_delete not in list_of_book_id:  # if id not in the database the user will get this error
                print("\nThis book is not in the database. please try again.")
            else:
                # This will delete this row from the database using the id as the key
                cursor.execute('''DELETE FROM books WHERE id = ?''', (which_book_to_delete,))

                db.commit()

                print("\nThis book has been deleted from the database.")
                break
        except ValueError:  # if the id the user enters is not valid the user will get this error message, then loop
            print("\nOops! That was not a valid id number, try again!")


def search_for_book():
    """
    This function will search the database for a certain title of book and display all the information
    about this book to the user
    """
    while True:
        # determine which book the user would like to search for, this is unfortunately case and space sensitive
        book_to_find = input("What is the title of the book you would like to find? (This is Case & Space Sensitive): ")
        list_of_book_titles = []   # Crete an empty list to store all the book titles
        for book_titles in list_of_books():
            list_of_book_titles.append(book_titles.title)  # loop through and append the book titles to the empty list
        if book_to_find not in list_of_book_titles:   # if title is not in the database the user will get this error
            print("This book doesnt exist in the database, please try again.")
        else:
            # this will gather the row of data from the database by the book title
            cursor.execute('''SELECT * FROM books WHERE Title = ?''', (book_to_find,))
            bring_book_to_python = cursor.fetchone()  # assign it a variable in the program
            located_book = Book(bring_book_to_python[0], bring_book_to_python[1],
                                bring_book_to_python[2], bring_book_to_python[3])   # assign to Book class

            located_book_table = [["id", "Title", "Author", "qty"],
                                  [located_book.book_id, located_book.title,
                                   located_book.author, located_book.qty]]

            print(tabulate(located_book_table, tablefmt="rounded_grid"))  # print all the book info into a table

            break


def main():
    """
    This function presents the user with a menu option of the eBook Store,
    where the options are chosen by the number they input into the console
    """
    while True:
        user_choice = int(input('''\nBook DataBase Menu , please enter the number of the option you'd like:  
                              1 - Enter Book
                              2 - Update Book
                              3 - Delete Book
                              4 - Search Book
                              5 - View All Books
                              0 - Exit
                              : '''))

        # Depending on the users choice the function will call on a different function to execute.

        if user_choice == 1:
            add_book()

        elif user_choice == 2:
            update_book_info()

        elif user_choice == 3:
            delete_book()

        elif user_choice == 4:
            search_for_book()

        elif user_choice == 5:
            view_database()

        elif user_choice == 0:   # This option exits the whole program
            print("\nThanks for using my eBookStore! Have a Great one!")
            exit()

        else:   # if their option is not valid they will get this error message.
            print("\nPlease enter a valid option.\n")


main()
