class Book:
    def __init__(self, isbn, title, author="Bilinmiyor",price=0,stock=0,is_borrowed=False,current_holder=None,borrow_date=None  ):
        self.isbn = isbn  # Benzersiz kimlik
        self.__title = title
        self.__author = author
        self.price = price
        self.stock = stock
        self.is_borrowed = is_borrowed
        self.current_holder = current_holder # Kitap şu an kimde?
        self.borrow_date=borrow_date

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
                    durum = "Ödünçte" if book.is_borrowed else "Mevcut"
                    kimde = book.current_holder if book.current_holder else "Kütüphanede"
                    tarih=book.borrow_date if book.borrow_date else "Yok"
                    # book.title yerine get_title() metodunu kullanıyoruz
                    f.write(f"{book.isbn},{book.get_title()},{durum},{kimde},{tarih}\n")
                    print("dosya başarıyla güncellendi!")
            return True
        except Exception as e:
            print(f" Dosya yazma hatası: {e}")
            return False
           

    def load_from_file(self):
        self.books=[]
        try:               
         with open("books.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line =line.strip()
                    if not line: continue

                    parts = line.split(",")
                    if len (parts)>=4:  # Boş satırları atla
                       isbn=parts [0]
                       title=parts[1]
                       durum=parts[2]
                       kimde=parts[3]
                       tarih=parts[4] if len(parts) > 4 else "Yok"
                   
                    yeni_kitap=Book (isbn, title, "Bilinmiyor",0,0)
                    # Dosyadan okunan durumları geri yükle
                    yeni_kitap.is_borrowed=( durum=='Ödünçte')
                    yeni_kitap.current_holder= None if kimde == "Kütüphanede" else kimde
                    yeni_kitap.borrow_date= None if tarih == "Yok" else tarih
                    self.add_book(yeni_kitap)
                    print("dosya başarıyla yüklendi")                   
        except FileNotFoundError:
            print("Henüz veri dosyası yok, yeni oluşturulacak")