import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QListWidget
from logic import Book, Library 

class KutuphaneArayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.kutuphane = Library()
        
        # 1. Eski verileri dosyadan Library sınıfına yükle
        self.kutuphane.load_from_file() 
        
        # 2. Arayüzü (butonları ve liste kutusunu) oluştur
        self.init_ui() 
        
        # 3. Yüklenen verileri ekrandaki listeye (QListWidget) tek tek bas
        for b in self.kutuphane.books:
            # Buradaki formatın kitap_ekle_fonksiyonu ile aynı olmalı!
            self.kitap_listesi.addItem(f"ISBN: {b.isbn} | Kitap: {b.get_title()}")
        
    def init_ui(self):
        self.setWindowTitle("Kütüphane Yönetim Paneli")
        self.setGeometry(100, 100, 350, 450)

        self.layout = QVBoxLayout()

        self.bilgi_label = QLabel("Kitap Eklemek İçin Bilgileri Girin:")
        self.layout.addWidget(self.bilgi_label)

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("ISBN Numarası")
        self.layout.addWidget(self.isbn_input)

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Kitap Adı")
        self.layout.addWidget(self.ad_input)

        self.ekle_buton = QPushButton("Kütüphaneye Ekle")
        self.ekle_buton.clicked.connect(self.kitap_ekle_fonksiyonu)
        self.layout.addWidget(self.ekle_buton)

        self.sil_buton = QPushButton("Seçili Kitabı Sil")
        # Butonun rengini biraz farklı yapalım (Opsiyonel ama şık durur)
        self.sil_buton.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        self.sil_buton.clicked.connect(self.kitap_sil_fonksiyonu)
        self.layout.addWidget(self.sil_buton)

        # Kitapları listeleyeceğimiz alan (Tablo)
        self.kitap_listesi = QListWidget() 
        self.layout.addWidget(self.kitap_listesi)
        
        self.kaydet_buton = QPushButton("Tüm Listeyi Kaydet")
        self.kaydet_buton.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.kaydet_buton.clicked.connect(self.kaydet_fonksiyonu)
        self.layout.addWidget(self.kaydet_buton)
        
        # ARAMA BÖLÜMÜ
        self.arama_label = QLabel("Kitap Ara (ISBN veya İsim):")
        self.layout.addWidget(self.arama_label)
        
        self.arama_input = QLineEdit()
        self.arama_input.setPlaceholderText("Aramak istediğiniz kelimeyi yazın...")
        # Yazı yazıldığı anda arama yapması için:
        self.arama_input.textChanged.connect(self.arama_fonksiyonu) 
        self.layout.addWidget(self.arama_input)

        # Araya küçük bir çizgi (Görsel ayırıcı)
        çizgi = QLabel("------------------------------------------")
        self.layout.addWidget(çizgi)
      
        self.setLayout(self.layout)

    def kitap_ekle_fonksiyonu(self):
        isbn = self.isbn_input.text()
        ad = self.ad_input.text()
        if isbn and ad:
            yeni_kitap = Book(isbn, ad, "Bilinmiyor", 0, 0)
            durum, mesaj = self.kutuphane.add_book(yeni_kitap)
            if durum:
                QMessageBox.information(self, "Başarılı", mesaj)
                # Kitabı ekrandaki listeye (QListWidget) ekleyen satır:
                self.kitap_listesi.addItem(f"ISBN: {isbn} | Kitap: {ad}")
                self.isbn_input.clear()
                self.ad_input.clear()
            else:
                QMessageBox.warning(self, "Hata", mesaj)
        else:
            QMessageBox.critical(self, "Hata", "Lütfen boş alan bırakmayın!")

            self.isbn_input.setFocus() # İmleci otomatik ISBN kutusuna atar

        
    def kitap_sil_fonksiyonu(self):
        # 1. Listeden seçili olan satırı bul
        secili_item = self.kitap_listesi.currentItem()
        
        if secili_item:
            # 2. Satırdaki metinden ISBN'yi ayıkla (Formatımız -> ISBN: 101 | ...)
            metin = secili_item.text()
            # "ISBN: " kısmından sonrasını alıp boşluğa kadar bölüyoruz
            isbn = metin.split("ISBN: ")[1].split(" |")[0]
            
            # 3. logic.py'deki remove_book fonksiyonunu çağır
            silindi_mi = self.kutuphane.remove_book(isbn)
            
            if silindi_mi:
                # 4. Eğer arkada silindiyse, ekrandaki listeden de görsel olarak kaldır
                row = self.kitap_listesi.row(secili_item)
                self.kitap_listesi.takeItem(row)
                QMessageBox.information(self, "Başarılı", f"{isbn} ISBN'li kitap silindi.")
            else:
                QMessageBox.warning(self, "Hata", "Kitap sistemden silinemedi!")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen silmek için listeden bir kitap seçin!")
    
    def kaydet_fonksiyonu(self):
        self.kutuphane.save_to_file()
        QMessageBox.information(self, "Başarılı", "Kitap listesi books.txt dosyasına kaydedildi!")

    def arama_fonksiyonu(self):
        arama_metni = self.arama_input.text().lower() # Küçük harfe çevirerek ara
        
        # Listedeki tüm satırları tek tek kontrol et
        for i in range(self.kitap_listesi.count()):
            item = self.kitap_listesi.item(i)
            # Eğer satırdaki metin arama kelimesini içeriyorsa göster, içermiyorsa gizle
            if arama_metni in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = KutuphaneArayuz()
    pencere.show()
    sys.exit(app.exec()) # Burası PyQt6 için tam olarak böyle olmalı