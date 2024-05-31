#Tools Mengambil Email dari Sebuah File PDF
#Acep Triana
#Sistem Informasi

import fitz  # PyMuPDF
import re

def extract_emails_from_pdf(pdf_path):
    # Membuka file PDF
    pdf_document = fitz.open(pdf_path)
    emails = set()  # Menggunakan set untuk menghindari duplikat

    # Loop melalui setiap halaman dalam PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text()

        # Cari email menggunakan regex
        found_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        emails.update(found_emails)

    return emails

def save_emails_to_file(emails, output_path):
    with open(output_path, 'w') as file:
        for email in emails:
            file.write(email + '\n')

if __name__ == "__main__":
    pdf_path = 'D:\\Tools\\data.pdf'  # Path ke file PDF Anda
    output_path = 'result_email.txt'  # Path untuk menyimpan hasil email

    emails = extract_emails_from_pdf(pdf_path)

    if emails:
        save_emails_to_file(emails, output_path)
        print(f"Ditemukan email berikut dan disimpan di {output_path}:")
        for email in emails:
            print(email)
    else:
        print("Tidak ditemukan email dalam file PDF.")
