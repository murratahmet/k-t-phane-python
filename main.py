import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QListWidget, QInputDialog,QListWidgetItem
from logic import Book, Library 

class KutuphaneArayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.kutuphane = Library()
        
        # 1. Eski verileri dosyadan Library sınıfına yükle
        self.kutuphane.load_from_file() 
        
        # 2. Arayüzü (butonları ve liste kutusunu) oluştur
        self.init_ui() 
        self.arayuzu_tazele()
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

        # Bu satırı init_ui içine, diğer butonların olduğu yere ekle
        self.odunc_buton = QPushButton("Kitabı Ödünç Ver / İade Al")
        self.odunc_buton.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold;")
        self.odunc_buton.clicked.connect(self.odunc_islem_fonksiyonu)
        self.layout.addWidget(self.odunc_buton)

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
        baslik = self.ad_input.text()
        
        if isbn and baslik:
            from logic import Book
            yeni_kitap = Book(isbn, baslik, "Bilinmiyor", 0, 0)
            basarili, mesaj = self.kutuphane.add_book(yeni_kitap)
            
            if basarili:
                # Sadece düz yazı değil, durum bilgisini de ekliyoruz
                self.kutuphane.save_to_file()
                self.arayuzu_tazele()
                self.isbn_input.clear()
                self.ad_input.clear()
               
            else:
                QMessageBox.warning(self, "Hata", mesaj) 

        
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

                from PyQt6.QtWidgets import QInputDialog # Bunu en üste eklemeyi unutma

    def arayuzu_tazele(self):
        from PyQt6.QtGui import QColor
        self.kitap_listesi.clear() 
        for b in self.kutuphane.books:
            if b.is_borrowed:
                durum = f" [KİMDEDE: {b.current_holder}]"  
                renk = QColor("red")
            else : 
                durum = " [KÜTÜPHANEDE]"
                renk = QColor("darkgreen")

            # DÜZELTME: Nesneyi oluştur ve rengi üzerine uygula, değişkene tekrar atama yapma!
            item = QListWidgetItem(f"ISBN: {b.isbn} | Kitap: {b.get_title()}{durum}")
            item.setForeground(renk) 
            self.kitap_listesi.addItem(item)

    def odunc_islem_fonksiyonu(self):
        import datetime
        secili_item = self.kitap_listesi.currentItem()
        if not secili_item:
            QMessageBox.warning(self, "Hata", "Lütfen bir kitap seçin!")
            return

        metin = secili_item.text()
        try:
            isbn = metin.split("ISBN: ")[1].split(" |")[0]
            kitap = next((b for b in self.kutuphane.books if b.isbn == isbn), None)

            if kitap:
                if not kitap.is_borrowed:
                    isim, onay = QInputDialog.getText(self, "Ödünç Ver", "Kitabı kim alıyor?")
                    if onay and isim.strip():
                        kitap.is_borrowed = True
                        kitap.current_holder = isim
                        # DÜZELTME: Tarih atamasını onay alındıktan sonra yapıyoruz
                        kitap.borrow_date = datetime.datetime.now().strftime("%d.%m.%Y")
                        QMessageBox.information(self, "Başarılı", f"Kitap {isim} kişisine verildi.")
                else:
                    cevap = QMessageBox.question(self, "İade", f"Bu kitap {kitap.current_holder} kişisinde. İade alalım mı?",
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if cevap == QMessageBox.StandardButton.Yes:
                        kitap.is_borrowed = False
                        kitap.current_holder = None
                        kitap.borrow_date = None # İade edilince tarihi temizle
                        QMessageBox.information(self, "Başarılı", "Kitap iade alındı.")
                
                self.kutuphane.save_to_file()
                self.arayuzu_tazele()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İşlem sırasında bir hata oluştu: {e}")
    
            
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = KutuphaneArayuz()
    pencere.show()
    sys.exit(app.exec()) # Burası PyQt6 için tam olarak böyle olmalı