# *Author - Ilya Kharkovets*
# 20.02.2024

import flet as ft
import os
import pathlib
import PyPDF2
from PIL import Image
from flet import ElevatedButton, Row
from gtts import gTTS
from pdf2docx import parse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def main(page: ft.Page):
    page.window_height = 600
    page.window_width = 720
    page.window_full_screen = False
    page.window_opacity = 0.95
    page.window_resizable = False


    def pick_files_result(e: ft.FilePickerResultEvent):
        global output_file
        global selected_file

        if e.files:
            selected_file = e.files[0].path

            # Check file extension to determine file type
            file_extension = selected_file.lower().split('.')[-1]

            if file_extension == 'pdf':
                output_file = os.path.splitext(selected_file)[0] + "_ready.pdf"
            elif file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                output_file = os.path.splitext(selected_file)[0] + "_ready.jpg"
            else:
                selected_files.update()
    
    def text_to_speech(file_path, language='ru', output_file='output.mp3'):
        try:
            # Открываем текстовый файл и читаем его содержимое
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            # Создаем объект gTTS
            tts = gTTS(text=text, lang=language, slow=False)

            # Сохраняем аудиофайл
            tts.save(output_file)

            print(f"Аудиофайл успешно создан: {output_file}")

            # Воспроизводим аудиофайл
            os.system(f"start {output_file}")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def pdf_to_txt(pdf_path):
    # Extracting the base filename and directory from the provided PDF path
        pdf_dir, pdf_filename = os.path.split(pdf_path)
        # Removing the ".pdf" extension from the filename
        txt_filename = os.path.splitext(pdf_filename)[0] + ".txt"
        # Constructing the full path for the text file
        txt_path = os.path.join(pdf_dir, txt_filename)

        # Opening the PDF file in binary mode
        with open(pdf_path, 'rb') as pdf_file:
            # Creating a PdfReader object
            reader = PyPDF2.PdfReader(pdf_file)
            # Opening the text file in write mode
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                # Iterating through pages of the PDF file
                for page_number in range(len(reader.pages)):
                    # Accessing the page by the current index (page_number)
                    page = reader.pages[page_number]
                    # Extracting text content from the page using the extract_text() method
                    text = page.extract_text()
                    # Writing the extracted text to the text file
                    txt_file.write(text)
    
    def convert_jpg_to_pdf(jpg_file):
        # Ensure the provided file is a JPG
        if not jpg_file.lower().endswith(('.jpg', '.jpeg')):
            print("Error: Input file is not a JPG.")
            return

        # Create a PDF file with the same name as the JPG file
        pdf_file = os.path.splitext(jpg_file)[0] + '.pdf'

        # Open the JPG image using Pillow
        img = Image.open(jpg_file)

        # Create a PDF canvas
        pdf = canvas.Canvas(pdf_file, pagesize=img.size)

        # Draw the JPG image on the PDF canvas
        pdf.drawInlineImage(jpg_file, 0, 0, width=img.width, height=img.height)

        # Save and close the PDF file
        pdf.save()

        print(f"Conversion successful. PDF file created at: {pdf_file}")

    def compress_pdf(input_file, output_file):
        # Открываем исходный PDF-файл
        input_pdf = PyPDF2.PdfReader(open(input_file, 'rb'))
        # Создаем новый PDF-файл для хранения сжатых данных
        output_pdf = PyPDF2.PdfWriter()
        # Сжимаем каждую страницу исходного PDF-файла и добавляем ее в новый файл
        for page in input_pdf.pages:
            page.compress_content_streams()  # Сжатие содержимого страниц
            output_pdf.add_page(page)
        # Сохраняем сжатый PDF-файл
        output_pdf.write(open(output_file, 'wb'))
    
    def convert_to_word(pdf_file):
        word_file = pathlib.Path(pdf_file)
        word_file = word_file.stem + '.docx'
        parse(pdf_file, word_file)

    def change(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()
    def open_url(url):
        page.launch_url("https://github.com/paladinxb")

    def bs_dismissed(e):
        print("Dismissed!")

    def show_bs(e):
        bs.open = True
        bs.update()

    def close_bs(e):
        bs.open = False
        bs.update()

    bs = ft.BottomSheet(
        ft.Container(
            ft.Row(
                [
                    #ft.ElevatedButton("Close", on_click=close_bs),
                    ft.OutlinedButton("GitHub",on_click=open_url),
                    ft.IconButton(ft.icons.SUNNY, on_click=change),
                ],
                tight=True,
            ),
            padding=10,
        ),
        open=False,
        on_dismiss=bs_dismissed,
    )

    # Создание выпадающего меню для выбора темы
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    selected_files = ft.Text()


    page.overlay.append(bs)
    page.title = "Conventor by paladinxb"
    page.add(
                ft.Row(
                [
                    ft.IconButton(ft.icons.SETTINGS, on_click=show_bs),
                ]
                ), 
                ft.Row(
                    [
                       
                        ft.Text("Conventor by paladinxb", size=50, weight=ft.FontWeight.W_900, selectable=True, text_align="CENTER"),
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment = ft.MainAxisAlignment.CENTER
                ),
                Row([
                    ft.Text(" ", size=10, weight=ft.FontWeight.W_900, selectable=True, text_align="CENTER")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment = ft.MainAxisAlignment.CENTER
                ),
                Row([
                    ElevatedButton(text="Выберите файл для работы", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: pick_files_dialog.pick_files(
                                    allow_multiple=True
                                )), 
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment = ft.MainAxisAlignment.CENTER
                ),
                Row([
                    ft.Text(" ", size=10, weight=ft.FontWeight.W_900, selectable=True, text_align="CENTER")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                Row([selected_files], alignment=ft.MainAxisAlignment.CENTER),
                Row(
                    [
                        ElevatedButton(text="Перевод PDF в Word", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: convert_to_word(selected_file)
                                ),
                        ElevatedButton(text="Перевод PDF в TXT", icon=ft.icons.UPLOAD_FILE,
                                    on_click=lambda _: pdf_to_txt(selected_file)(allow_multiple=True)),
                        ElevatedButton(text="Перевод JPG в PDF", icon=ft.icons.UPLOAD_FILE,on_click=lambda _: convert_jpg_to_pdf(selected_file)(
                                    allow_multiple=True
                                )),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment = ft.MainAxisAlignment.CENTER
                ),
                Row([
                    ft.Text(" ", size=20, weight=ft.FontWeight.W_900, selectable=True, text_align="CENTER")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                Row(
                    [
                        ElevatedButton(text="Сжатие PDF", icon=ft.icons.UPLOAD_FILE,on_click=lambda _: compress_pdf(selected_file, output_file)(
                                    allow_multiple=True
                                )),
                        ElevatedButton(text="TXT в Аудио", icon=ft.icons.UPLOAD_FILE,on_click=lambda _: text_to_speech(selected_file, language='ru', output_file='output.mp3')(
                                    allow_multiple=True
                                )),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ), 
        ),

ft.app(target=main)
