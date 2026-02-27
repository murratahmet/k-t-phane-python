class Book:
    def __init__(self, isbn, title, author, pages, year):
        self.isbn = isbn  # Benzersiz kimlik
        self.__title = title
        self.__author = author
        self.__pages = int(pages) # Sayıyı sağlama alalım
        self.__year = year
        self.is_borrowed = False
        self.current_holder = None # Kitap şu an kimde?

    def get_title(self): return self.__title
    def get_author(self): return self.__author
    def get_pages(self): return self.__pages
    def get_year(self): return self.__year

    def display_info(self):
        status = f"Ödünçte ({self.current_holder})" if self.is_borrowed else "Mevcut"
        return f"[{self.isbn}] 📖 {self.__title} - {self.__author} | {status}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        # Aynı ISBN'li kitap var mı kontrolü (Mühendislik kuralı!)
        if any(b.isbn == book.isbn for b in self.books):
            return False, "Bu ISBN zaten kayıtlı!"
        self.books.append(book)
        return True, "Kitap başarıyla eklendi."

    def remove_book(self, isbn):
        # İsim yerine ISBN ile silmek çok daha güvenli
        for b in self.books:
            if b.isbn == isbn:
                self.books.remove(b)
                return True
        return False

    def borrow_book(self, isbn, user_name):
        for b in self.books:
            if b.isbn == isbn and not b.is_borrowed:
                b.is_borrowed = True
                b.current_holder = user_name
                return True
        return False

    def return_book(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                b.is_borrowed = False
                b.current_holder = None
                return True
        return False

    def list_books(self):
        return self.books
    
    def save_to_file(self):
        try:
            with open("books.txt", "w", encoding="utf-8") as f:
                for book in self.books:
                    # book.title yerine get_title() metodunu kullanıyoruz
                    f.write(f"{book.isbn},{book.get_title()}\n")
            return True
        except Exception as e:
            print(f"Kaydetme hatası: {e}")
            return False

    def load_from_file(self):
        try:
            import os
            if not os.path.exists("books.txt"):
                return
                
            with open("books.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line: continue # Boş satırları atla
                    
                    parts = line.split(",")
                    if len(parts) == 2:
                        isbn, title = parts
                        # Yeni kitap nesnesi oluşturup listeye ekle
                        self.add_book(Book(isbn, title, "Bilinmiyor", 0, 0))
        except Exception as e:
            print(f"Yükleme hatası: {e}")