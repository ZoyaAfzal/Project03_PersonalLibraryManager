import json
from colorama import Fore, Style, init

# Initialize colorama (for Windows support)
init(autoreset=True)

db_file = "library.json"

def load_library():
    try:
        with open(db_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library():
    with open(db_file, "w") as file:
        json.dump(library, file, indent=4)

library = load_library()

def add_book():
    title = input(Fore.CYAN + "Enter the book title: " + Style.RESET_ALL).strip()
    author = input(Fore.CYAN + "Enter the author: " + Style.RESET_ALL).strip()
    
    while True:
        try:
            year = int(input(Fore.CYAN + "Enter the publication year: " + Style.RESET_ALL).strip())
            break
        except ValueError:
            print(Fore.RED + "Invalid year! Please enter a valid number." + Style.RESET_ALL)
    
    genre = input(Fore.CYAN + "Enter the genre: " + Style.RESET_ALL).strip()
    read_status = input(Fore.CYAN + "Have you read this book? (yes/no): " + Style.RESET_ALL).strip().lower() == "yes"
    
    rating = 0
    if read_status:
        while True:
            try:
                rating = int(input(Fore.YELLOW + "Rate the book (1-5): " + Style.RESET_ALL).strip())
                if 1 <= rating <= 5:
                    break
                else:
                    print(Fore.RED + "Please enter a rating between 1 and 5." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Invalid rating! Please enter a number between 1 and 5." + Style.RESET_ALL)
    
    library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status, "rating": rating})
    print(Fore.GREEN + "Book added successfully!" + Style.RESET_ALL)
    save_library()

def remove_book():
    title = input(Fore.RED + "Enter the title of the book to remove: " + Style.RESET_ALL)
    global library
    library = [book for book in library if book["title"].lower() != title.lower()]
    print(Fore.GREEN + "Book removed successfully!" + Style.RESET_ALL)
    save_library()

def search_books():
    print(Fore.MAGENTA + "Search by:\n1. Title\n2. Author\n3. Genre" + Style.RESET_ALL)
    choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)
    keyword = input(Fore.YELLOW + "Enter the search keyword: " + Style.RESET_ALL)
    
    if choice == "1":
        results = [book for book in library if keyword.lower() in book["title"].lower()]
    elif choice == "2":
        results = [book for book in library if keyword.lower() in book["author"].lower()]
    elif choice == "3":
        results = [book for book in library if keyword.lower() in book["genre"].lower()]
    else:
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
        return
    
    if results:
        for book in results:
            print(Fore.BLUE + f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'} - Rating: {book['rating']}/5" + Style.RESET_ALL)
    else:
        print(Fore.RED + "No books found." + Style.RESET_ALL)

def display_books():
    if not library:
        print(Fore.RED + "Library is empty." + Style.RESET_ALL)
        return
    
    print(Fore.MAGENTA + "Sort by:\n1. Title\n2. Author\n3. Year" + Style.RESET_ALL)
    sort_choice = input(Fore.YELLOW + "Enter sorting choice: " + Style.RESET_ALL)
    
    if sort_choice == "1":
        sorted_library = sorted(library, key=lambda x: x["title"].lower())
    elif sort_choice == "2":
        sorted_library = sorted(library, key=lambda x: x["author"].lower())
    elif sort_choice == "3":
        sorted_library = sorted(library, key=lambda x: x["year"], reverse=True)
    else:
        print(Fore.RED + "Invalid choice. Showing unsorted list." + Style.RESET_ALL)
        sorted_library = library
    
    for book in sorted_library:
        print(Fore.BLUE + f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'} - Rating: {book['rating']}/5" + Style.RESET_ALL)

def display_statistics():
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books else 0
    print(Fore.CYAN + f"Total books: {total_books}\nPercentage read: {read_percentage:.2f}%" + Style.RESET_ALL)

def update_book():
    title = input(Fore.YELLOW + "Enter the title of the book to update: " + Style.RESET_ALL)
    for book in library:
        if book["title"].lower() == title.lower():
            book["read"] = input(Fore.CYAN + "Have you read this book? (yes/no): " + Style.RESET_ALL).strip().lower() == "yes"
            if book["read"]:
                book["rating"] = int(input(Fore.YELLOW + "Rate the book (1-5): " + Style.RESET_ALL))
            print(Fore.GREEN + "Book updated successfully!" + Style.RESET_ALL)
            save_library()
            return
    print(Fore.RED + "Book not found." + Style.RESET_ALL)

def menu():
    while True:
        print(Fore.CYAN + "\nWelcome to your Personal Library Manager!" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Add a book\n2. Remove a book\n3. Search for a book\n4. Display all books\n5. Display statistics\n6. Update a book\n7. Exit" + Style.RESET_ALL)
        
        choice = input(Fore.GREEN + "Enter your choice: " + Style.RESET_ALL)
        
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_books()
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            update_book()
        elif choice == "7":
            print(Fore.GREEN + "Library saved to file. Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Try again." + Style.RESET_ALL)

if __name__ == "__main__":
    menu()
