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
        
        
    def init_ui(self):
        

        self.setWindowTitle("Kütüphane Yönetim Paneli")
        self.setGeometry(100, 100, 350, 550)

        self.ana_layout = QVBoxLayout()

        self.stats_label = QLabel ("Kütüphane Kitapları Hazırlıyor...")
        self.stats_label.setStyleSheet("""
            background-color: #34495e; 
            color: white; 
            padding: 10px; 
            border-radius: 5px; 
            font-weight: bold;
            font-size: 13px;
        """)
        self.ana_layout.insertWidget(0, self.stats_label)

        self.bilgi_label = QLabel("Kitap Eklemek İçin Bilgileri Girin:")
        self.ana_layout.addWidget(self.bilgi_label)

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("ISBN Numarası (veya Barkod Okutun)")
        self.isbn_input.returnPressed.connect(self.kitap_ekle_fonksiyonu)
        self.ana_layout.addWidget(self.isbn_input)

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Kitap Adı")
        self.ana_layout.addWidget(self.ad_input)

        self.ekle_buton = QPushButton("Kütüphaneye Ekle")
        self.ekle_buton.clicked.connect(self.kitap_ekle_fonksiyonu)
        self.ana_layout.addWidget(self.ekle_buton)

        self.sil_buton = QPushButton("Seçili Kitabı Sil")
        # Butonun rengini biraz farklı yapalım (Opsiyonel ama şık durur)
        self.sil_buton.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        self.sil_buton.clicked.connect(self.kitap_sil_fonksiyonu)
        self.ana_layout.addWidget(self.sil_buton)

        # Bu satırı init_ui içine, diğer butonların olduğu yere ekle
        self.odunc_buton = QPushButton("Kitabı Ödünç Ver / İade Al")
        self.odunc_buton.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold;")
        self.odunc_buton.clicked.connect(self.odunc_islem_fonksiyonu)
        self.ana_layout.addWidget(self.odunc_buton)

        # Kitapları listeleyeceğimiz alan (Tablo)
        self.kitap_listesi = QListWidget() 
        self.ana_layout.addWidget(self.kitap_listesi)
        
        self.kaydet_buton = QPushButton("Tüm Listeyi Kaydet")
        self.kaydet_buton.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.kaydet_buton.clicked.connect(self.kaydet_fonksiyonu)
        self.ana_layout.addWidget(self.kaydet_buton)

        # İstatistik alanı (Layout'un en başına ekleyebilirsin)
        self.stats_label = QLabel("Toplam Kitap: 0 | Ödünçte: 0 | Geciken: 0")
        self.stats_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px; margin-bottom: 10px;")
        self.ana_layout.insertWidget(0, self.stats_label) # En üste yerleştirir
        
        # ARAMA BÖLÜMÜ
        self.arama_label = QLabel("Kitap Ara (ISBN veya İsim):")
        self.ana_layout.addWidget(self.arama_label)
        
        self.arama_input = QLineEdit()
        self.arama_input.setPlaceholderText("Aramak istediğiniz kelimeyi yazın...")
        # Yazı yazıldığı anda arama yapması için:
        self.arama_input.textChanged.connect(self.arama_fonksiyonu) 
        self.ana_layout.addWidget(self.arama_input)
        
        self.kamera_buton = QPushButton("📷 Kamera ile Barkod Tara")
        self.kamera_buton.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        self.kamera_buton.clicked.connect(self.kamera_ile_tara)
        self.ana_layout.addWidget(self.kamera_buton)


        # Araya küçük bir çizgi (Görsel ayırıcı)
        çizgi = QLabel("------------------------------------------")
        self.ana_layout.addWidget(çizgi)
      
        self.setLayout(self.ana_layout)

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
        import datetime
        
        self.kitap_listesi.clear() # Listeyi temizle
        bugun = datetime.datetime.now()
        toplam_kitap=len(self.kutuphane.books)
        odunc_sayisi=0
        geciken_sayisi=0

        for b in self.kutuphane.books:
            ek_uyari = ""
            if b.is_borrowed:
                odunc_sayisi+=1
                durum = f" [KİMDEDE: {b.current_holder}]"
                renk = QColor("red")
                
                # GECİKME KONTROLÜ (15 Gün)
                if b.borrow_date and b.borrow_date != "Yok":
                    try:
                        verilis = datetime.datetime.strptime(b.borrow_date, "%d.%m.%Y")
                        fark = (bugun - verilis).days
                        if fark > 15:
                            geciken_sayisi+=1
                            ek_uyari = f" ⚠️ GECİKTİ! ({fark} gün)"
                    except:pass
            else:
                durum = " [KÜTÜPHANEDE]"
                renk = QColor("white")

            # Ekrana basılacak metin
            liste_metni = f"ISBN: {b.isbn} | Kitap: {b.get_title()}{durum}{ek_uyari}"
            item = QListWidgetItem(liste_metni)
            item.setForeground(renk) 
            self.kitap_listesi.addItem(item)

            self.stats_label.setText(
                f" Toplam : {toplam_kitap} | "
                f" Ödünç : {odunc_sayisi} | "
                f" Geciken : {geciken_sayisi}"
            )

            toplam = len(self.kutuphane.books)
        oduncte = sum(1 for b in self.kutuphane.books if b.is_borrowed)
        gecikme_sayisi = 0
        
        # Gecikme sayısını hesapla (daha önceki tarih mantığıyla aynı)
        import datetime
        bugun = datetime.datetime.now()
        for b in self.kutuphane.books:
            if b.is_borrowed and b.borrow_date and b.borrow_date != "Yok":
                try:
                    verilis = datetime.datetime.strptime(b.borrow_date, "%d.%m.%Y")
                    if (bugun - verilis).days > 15:
                        gecikme_sayisi += 1
                except: pass

        self.stats_label.setText(f"Toplam Kitap: {toplam} | Ödünçte: {oduncte} | Geciken: {gecikme_sayisi}")

    def odunc_islem_fonksiyonu(self):
        import datetime
        secili_item = self.kitap_listesi.currentItem()
        if not secili_item:
            QMessageBox.warning(self, "Hata", "Lütfen bir kitap seçin!")
            return

        metin = secili_item.text()
        try:
            # ISBN'yi güvenli alalım
            parts = metin.split("ISBN: ")
            if len(parts) < 2: return
            isbn = parts[1].split(" |")[0]
            
            kitap = next((b for b in self.kutuphane.books if b.isbn == isbn), None)

            if kitap:
                if not kitap.is_borrowed:
                    # 1. ADI AL
                    ad, ok1 = QInputDialog.getText(self, "Ödünç Ver", "Okuyucunun Adı:")
                    if not ok1 or not ad.strip(): return # İptal edilirse çık

                    # 2. SOYADI AL
                    soyad, ok2 = QInputDialog.getText(self, "Ödünç Ver", f"{ad} kişisinin Soyadı:")
                    if not ok2 or not soyad.strip(): return # İptal edilirse çık

                    # 3. TELEFONU AL
                    tel, ok3 = QInputDialog.getText(self, "İletişim", f"{ad} {soyad} için telefon:")
                    # Telefon zorunlu olmasın diyorsan 'if not ok3: return' yapma
                    
                    # TÜM BİLGİLER TAMAMSA KAYDET
                    tam_isim = f"{ad.strip().capitalize()} {soyad.strip().upper()}"
                    kitap.is_borrowed = True
                    kitap.current_holder = tam_isim
                    kitap.phone = tel if (ok3 and tel.strip()) else "Yok"
                    kitap.borrow_date = datetime.datetime.now().strftime("%d.%m.%Y")
                    
                    QMessageBox.information(self, "Başarılı", f"Kitap {tam_isim} kişisine verildi.")
                    self.kutuphane.save_to_file()
                    self.arayuzu_tazele()
                else:
                    # İADE ALMA (Burası aynı kalabilir)
                    cevap = QMessageBox.question(self, "İade", f"Bu kitap {kitap.current_holder} kişisinde. İade alalım mı?",
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if cevap == QMessageBox.StandardButton.Yes:
                        kitap.is_borrowed = False
                        kitap.current_holder = None
                        kitap.phone = None
                        kitap.borrow_date = None
                        self.kutuphane.save_to_file()
                        self.arayuzu_tazele()
        except Exception as e:
            # Görseldeki o hatayı burası yakalıyor
            QMessageBox.critical(self, "Hata", f"İşlem sırasında bir hata oluştu: {e}")
    
            
    def kamera_ile_tara(self):
        import cv2
        from pyzbar import pyzbar
        import requests

        cap = cv2.VideoCapture(0) # Kamerayı aç
        if not cap.isOpened():
            QMessageBox.critical(self, "Hata", "Kamera açılmadı!")
            return

        QMessageBox.information(self, "Bilgi", "Barkodu kameraya gösterin. Kapatmak için penceredeyken 'q'ya basın.")

        while True:
            ret, frame = cap.read()
            if not ret: break

            # Barkodları tara
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                isbn = barcode.data.decode("utf-8")
                self.isbn_input.setText(isbn) # ISBN'yi kutuya yaz
                
                # Sesi andıran bir görsel geri bildirim için çerçeve çizelim
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                cap.release()
                cv2.destroyAllWindows()
                
                # OTOMATİK BİLGİ ÇEKME
                self.google_dan_bilgi_cek(isbn)
                return

            cv2.imshow("Barkod Taraniyor...", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        cap.release()
        cv2.destroyAllWindows()

    def google_dan_bilgi_cek(self, isbn):
        import requests
        # ISBN içindeki tireleri veya boşlukları temizleyelim (API temiz veri sever)
        temiz_isbn = isbn.replace("-", "").replace(" ", "").strip()
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{temiz_isbn}"
        
        try:
            res = requests.get(url, timeout=5)
            data = res.json()
            
            if "items" in data:
                volume_info = data["items"][0]["volumeInfo"]
                kitap_adi = volume_info.get("title", "")
                yazar = ", ".join(volume_info.get("authors", ["Bilinmeyen Yazar"]))
                
                if kitap_adi:
                    self.ad_input.setText(kitap_adi)
                    QMessageBox.information(self, "Kitap Bulundu", 
                                          f"📚 Kitap: {kitap_adi}\n✍️ Yazar: {yazar}\n\nBilgiler otomatik dolduruldu!")
                    # İmleci direkt ekle butonuna odakla ki hızlıca kaydedebil
                    self.ekle_buton.setFocus()
            else:
                # EĞER BULUNAMAZSA: Kullanıcıyı bilgilendir ama kutuyu temizleme, 
                # belki ISBN doğrudur ama isim yoktur.
                QMessageBox.warning(self, "Bilgi", 
                                  f"Barkod okundu ({temiz_isbn}), ancak Google veritabanında bu kitabın detayları bulunamadı.\n\nLütfen kitap adını elle giriniz.")
                self.ad_input.setFocus() # Kitap adı kutusuna zıpla
        except Exception as e:
            print(f"Hata detayı: {e}")
            QMessageBox.warning(self, "Bağlantı Hatası", "İnternet bağlantısı kurulamadı. Lütfen bilgileri manuel giriniz.")        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = KutuphaneArayuz()
    pencere.show()
    sys.exit(app.exec()) # Burası PyQt6 için tam olarak böyle olmalı