import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QListWidget, QInputDialog,QListWidgetItem,QComboBox,QFileDialog    
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
       # RESMİ KURUMSAL TEMA (OFFICE STYLE)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 2px;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                padding: 6px;
                border-radius: 2px;
                selection-background-color: #34495e;
            }
            QLineEdit:focus {
                border: 1px solid #7f8c8d;
            }
            /* BÜTÜN BUTONLAR İÇİN ORTAK GRİ TASARIM */
            QPushButton {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                color: #2c3e50;
                padding: 8px;
                border-radius: 3px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #dcdde1;
                border: 1px solid #95a5a6;
            }
            QPushButton:pressed {
                background-color: #bdc3c7;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                border-radius: 2px;
                outline: none;
                color: #333333; /* <--- KİTAP İSİMLERİNİ SİYAH/KOYU GRİ YAPAR */
                font-weight: 500;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px dashed #eee;
                color: #333333; /* <--- HER BİR SATIRIN YAZI RENGİNİ GARANTİYE ALIR */
                font-weight: 500;
            }
            QListWidget::item:selected {
                background-color: #34495e;
                color: #ffffff; /* <--- SADECE SEÇİLEN KİTABIN YAZISI BEYAZ KALSIN */
                font-weight: 500;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                padding: 5px;
                border-radius: 2px;
            }
        """)
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
        self.ekle_buton.setStyleSheet("")
        self.ekle_buton.clicked.connect(self.kitap_ekle_fonksiyonu)
        self.ana_layout.addWidget(self.ekle_buton)
        

        self.sil_buton = QPushButton("Seçili Kitabı Sil")
        # Butonun rengini biraz farklı yapalım (Opsiyonel ama şık durur)
        self.sil_buton.setStyleSheet("")
        self.sil_buton.clicked.connect(self.kitap_sil_fonksiyonu)
        self.ana_layout.addWidget(self.sil_buton)
        

        # Bu satırı init_ui içine, diğer butonların olduğu yere ekle
        self.odunc_buton = QPushButton("Kitabı Ödünç Ver / İade Al")
        self.odunc_buton.setStyleSheet("")
        self.odunc_buton.clicked.connect(self.odunc_islem_fonksiyonu)
        self.ana_layout.addWidget(self.odunc_buton)

        # Kitapları listeleyeceğimiz alan (Tablo)
        self.kitap_listesi = QListWidget() 
        self.ana_layout.addWidget(self.kitap_listesi)
        
        self.kaydet_buton = QPushButton("Tüm Listeyi Kaydet")
        self.kaydet_buton.setStyleSheet("")
        self.kaydet_buton.clicked.connect(self.kaydet_fonksiyonu)
        self.ana_layout.addWidget(self.kaydet_buton)

        # İstatistik alanı (Layout'un en başına ekleyebilirsin)
        self.stats_label = QLabel("Toplam Kitap: 0 | Ödünçte: 0 | Geciken: 0")
        self.stats_label.setStyleSheet("")
        self.ana_layout.insertWidget(0, self.stats_label) # En üste yerleştirir
        

        # Filtreleme Etiketi ve Menüsü
        self.filtre_label = QLabel("Listeyi Filtrele:")
        self.ana_layout.addWidget(self.filtre_label)

        self.filtre_menu = QComboBox()
        self.filtre_menu.addItems([
            "Hepsini Göster", 
            "Sadece Kütüphanedekiler", 
            "Sadece Ödünç Verilenler", 
            "Sadece Gecikenler"
        ])
        # Menü her değiştiğinde listeyi otomatik güncelle
        self.filtre_menu.currentIndexChanged.connect(self.arama_fonksiyonu)
        self.ana_layout.addWidget(self.filtre_menu)
        # ARAMA BÖLÜMÜ
        self.arama_label = QLabel("Kitap Ara (ISBN veya İsim):")
        self.ana_layout.addWidget(self.arama_label)
        
        self.arama_input = QLineEdit()
        self.arama_input.setPlaceholderText("Aramak istediğiniz kelimeyi yazın...")
        # Yazı yazıldığı anda arama yapması için:
        self.arama_input.textChanged.connect(self.arama_fonksiyonu) 
        self.ana_layout.addWidget(self.arama_input)
        
        self.kamera_buton = QPushButton("📷 Kamera ile Barkod Tara")
        self.kamera_buton.setStyleSheet("")
        self.kamera_buton.clicked.connect(self.kamera_ile_tara)
        self.ana_layout.addWidget(self.kamera_buton)

        self.excel_buton = QPushButton("📊 Listeyi Excel (CSV) Olarak Kaydet")
        self.excel_buton.setStyleSheet("")
        self.excel_buton.clicked.connect(self.excel_aktar_fonksiyonu)
        self.ana_layout.addWidget(self.excel_buton)


        # Araya küçük bir çizgi (Görsel ayırıcı)
        çizgi = QLabel("------------------------------------------")
        self.ana_layout.addWidget(çizgi)
      
        self.setLayout(self.ana_layout)

    def kitap_ekle_fonksiyonu(self):
        isbn = self.isbn_input.text()
        baslik = self.ad_input.text().strip().title()
        
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
        arama_metni = self.arama_input.text().lower()
        secili_filtre = self.filtre_menu.currentText().strip() # Boşlukları temizle
         
        for i in range(self.kitap_listesi.count()):
            item = self.kitap_listesi.item(i)
            satir_metni = item.text().lower()
            
            # Filtre uygunluğunu her kitap (item) için döngü içinde kontrol etmeliyiz!
            filtre_uygunmu = False
            
            if secili_filtre == "Hepsini Göster":
                filtre_uygunmu = True
            elif secili_filtre == "Sadece Kütüphanedekiler":
                filtre_uygunmu = "[KÜTÜPHANEDE]" in item.text().upper()
            elif secili_filtre == "Sadece Ödünç Verilenler":
                # Senin kodunda "Kimde :" yazıyor, ama listede [KİMDEDE: ...] yazıyor olabilir
                filtre_uygunmu = "KİMDE" in item.text().upper()
            elif secili_filtre == "Sadece Gecikenler":
                filtre_uygunmu = "GECİKTİ" in item.text().upper()

            # Arama metni kontrolü
            metin_uygunmu = arama_metni in satir_metni
            
            # İki şart da sağlanıyorsa göster
            if metin_uygunmu and filtre_uygunmu:
                item.setHidden(False)
            else:
                item.setHidden(True)
    

    def arayuzu_tazele(self):
        from PyQt6.QtGui import QColor
        from PyQt6.QtWidgets import QListWidgetItem # Import eklendi
        import datetime
        
        self.kitap_listesi.clear() # Listeyi temizle
        bugun = datetime.datetime.now()
        
        # Sayaçları en başta sıfırlıyoruz
        toplam_kitap = 0
        odunc_sayisi = 0
        geciken_sayisi = 0

        # Tek bir döngü ile hem listeyi dolduruyoruz hem sayıları topluyoruz
        for b in self.kutuphane.books:
            toplam_kitap += 1
            ek_uyari = ""
            
            if b.is_borrowed:
                odunc_sayisi += 1
                durum = f" [KİMDE: {b.current_holder}]"
                renk = QColor("red")
                
                # GECİKME KONTROLÜ (15 Gün)
                if b.borrow_date and b.borrow_date != "Yok":
                    try:
                        verilis = datetime.datetime.strptime(b.borrow_date, "%d.%m.%Y")
                        fark = (bugun - verilis).days
                        if fark > 15:
                            geciken_sayisi += 1
                            ek_uyari = f" ⚠️ GECİKTİ! ({fark} gün)"
                    except:
                        pass
            else:
                durum = " [KÜTÜPHANEDE]"
                # Resmi tema (beyaz arka plan) kullandığın için siyah yazı daha iyi okunur
                renk = QColor("#333333") 

            # Ekrana basılacak metni oluştur ve listeye ekle
            liste_metni = f"ISBN: {b.isbn} | Kitap: {b.get_title()}{durum}{ek_uyari}"
            item = QListWidgetItem(liste_metni)
            item.setForeground(renk) 
            self.kitap_listesi.addItem(item)

        # İstatistik etiketini döngü BİTTİKTEN sonra (döngüyle aynı hizada) güncelliyoruz
        self.stats_label.setText(
            f"Toplam Kitap: {toplam_kitap} | "
            f"Ödünçte: {odunc_sayisi} | "
            f"Geciken: {geciken_sayisi}"
        )

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
                    if not ok3: return
                    # Telefon zorunlu olmasın diyorsan 'if not ok3: return' yapma
                    
                    # TÜM BİLGİLER TAMAMSA KAYDET
                    tam_isim = f"{ad.strip().capitalize()} {soyad.strip().upper()}"
                    kitap.current_holder=tam_isim
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
        
        # 1. Başlığı al ve baş harflerini büyük yap (.title())
                 raw_title = volume_info.get("title", "Bilinmeyen Kitap")
                 kitap_adi = raw_title.title() 
        
        # 2. Yazarları al ve onları da düzgün formatla
                 authors = volume_info.get("authors", ["Bilinmeyen Yazar"])
                 yazar = ", ".join(authors).title()
        
        # 3. Arayüzdeki kutucuğu güncelle
                 self.ad_input.setText(kitap_adi)
        
        # 4. Kullanıcıya bilgi ver
                 QMessageBox.information(self, "Kitap Bulundu", 
                              f"📚 Kitap: {kitap_adi}\n✍️ Yazar: {yazar}\n\nBilgiler otomatik dolduruldu!")
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

    def excel_aktar_fonksiyonu(self):
        import csv
        from PyQt6.QtWidgets import QFileDialog

    # 1. Bilgisayar sana "Nereye kaydedeyim?" diye soracak
        dosya_yolu, _ = QFileDialog.getSaveFileName(self, "Raporu Kaydet", "", "CSV Dosyası (*.csv)")

        if dosya_yolu:
           try:
            # 2. Seçtiğin dosyayı açıyoruz
            # 'utf-8-sig' kullanıyoruz ki Excel Türkçe karakterleri (ş, İ, ğ) düzgün göstersin
               with open(dosya_yolu, mode='w', newline='', encoding='utf-8-sig') as f:
                    yazar = csv.writer(f, delimiter=';') # Excel noktalı virgülü sever
                
                # 3. En üste başlıkları yazıyoruz
                    yazar.writerow(["ISBN", "Kitap Adı", "Durum", "Kimde", "Tarih", "Telefon"])
                
                # 4. Tüm kitapları tek tek dosyaya satır satır yazıyoruz
                    for kitap in self.kutuphane.books:
                        durum = "Ödünçte" if kitap.is_borrowed else "Kütüphanede"
                        yazar.writerow([
                        kitap.isbn, 
                        kitap.get_title(), 
                        durum, 
                        kitap.current_holder if kitap.current_holder else "-",
                        kitap.borrow_date if kitap.borrow_date else "-",
                        kitap.phone if kitap.phone else "-"
                    ])
            
               QMessageBox.information(self, "Başarılı", "Liste başarıyla Excel (CSV) olarak kaydedildi!")
           except Exception as e:
               QMessageBox.critical(self, "Hata", f"Kaydedilirken bir sorun oluştu: {e}")
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = KutuphaneArayuz()
    pencere.show()
    sys.exit(app.exec()) # Burası PyQt6 için tam olarak böyle olmalı