import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import websockets
from datetime import datetime
from keep_alive import keep_alive  # keep_alive.py dosyasını içe aktar

# Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

def run_flask():
    app.run(debug=True)
# URL ve Telegram bilgileri
url = "https://rustypot.com/coinflip"
telegram_token = '7725393384:AAHooYoNdX9cSLYmhYvqa1_mOBJJ51UFOs4'
chat_id = '1073946048'

# Web tarayıcısını başlat (örneğin Chrome)
driver = webdriver.Chrome()  # chromedriver dosyasının PATH'ini belirtmen gerekebilir
driver.get(url)

# Telegram’a mesaj gönderme fonksiyonu
def telegram_mesaj_gonder(mesaj):
    telegram_url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': mesaj
    }
    requests.post(telegram_url, params=params)

# Giveaway'ı kontrol eden fonksiyon
def kontrol_et():
    while True:
        try:
            # Flash giveaway başlangıcını kontrol et
            flash_giveaway = driver.find_element(By.ID, "fgStartingSoon")

            # Eğer div görünür hale geldiyse, giveaway başlamıştır
            if flash_giveaway.is_displayed():
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                mesaj = f"Flash giveaway başladı! Zaman: {now}"
                telegram_mesaj_gonder(mesaj)
                print(mesaj)

                # Giveaway başladıktan sonra 1.5 dakika bekle ve tekrar kontrol et
                time.sleep(90)  # 1.5 dakika bekle
                continue  # Ana döngüye dön

        except Exception as e:
            print("Henüz başlamadı veya bir hata oluştu:", e)

        time.sleep(2)  # 2 saniye bekle

# Ana program
if __name__ == "__main__":
    keep_alive()  # Flask sunucusunu başlat
    kontrol_et()  # Giveaway kontrol fonksiyonunu başlat
