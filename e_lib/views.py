from django.shortcuts import render,redirect,get_object_or_404
from .forms import BookForm
from .models import Subject, Book

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Video
from .forms import VideoForm
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
from django.core.files import File

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import ViewedBook
from django.utils import timezone


from translate import Translator
from pytube import YouTube
import os
import tensorflow as tf
import whisper
from django.conf import settings




import PyPDF2  # Import PyPDF2 and any other necessary libraries
import openai
from django.http import JsonResponse


# Replace "YOUR_API_KEY" with your actual OpenAI API key
openai.api_key = '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'
def home(request):
    
    if request.method == 'POST':
        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('subject_list')
        else:
            messages.success(request,("Incorrect username or password,try again"))
            return redirect('home')

    else:   
        return render(request, 'home.html', {})
    

def search_book(request):
    if request.method == "POST":
        searched = request.POST['searched']
        Books = Book.objects.filter(books_name__contains=searched)
        return render(request,'search_book.html', {'searched':searched,'Books':Books})
    else:
        return render(request,'search_book.html',{})

def summary(request):
    
    
    return render(request,'summary.html',{})
# def books(request):
    

#     return render(request,'books.html',{})
# def books(request):
    
#     book_list = Book.objects.all()
#     return render(request,'books.html',{'book_list':book_list})


@login_required

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.added_by = request.user

            if form_instance.book_pdf:
                pdf_data = form_instance.book_pdf.read()
                pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
                pdf_page = pdf_document[0]

                page_width = int(pdf_page.rect.width)
                page_height = int(pdf_page.rect.height)

                # Convert the PDF page to an RGB image
                pixmap = pdf_page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

                img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

                # Resize the image to the desired dimensions
                desired_width = 400  # Change this to your desired width
                desired_height = 600  # Change this to your desired height

                img = img.resize((desired_width, desired_height))

                img_io = BytesIO()
                img.save(img_io, format='PNG')

                img_file = File(img_io, name='image.png')
                form_instance.book_img = img_file

            form_instance.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})





def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

def books_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, subject_id=subject_id)
    books = Book.objects.filter(subject=subject)
    return render(request, 'books_by_subject.html', {'subject': subject, 'books': books})

def book_detail(request, books_id):
    book = get_object_or_404(Book, books_id=books_id)
    print(book)  # Check if the book object is populated
    context = {'book': book}
    return render(request, 'book_detail.html', context)

def view_pdf(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    viewed_book, created = ViewedBook.objects.get_or_create(user=request.user, book=book)
    if created:
        viewed_book.viewed_at = timezone.now()
        viewed_book.save()
    
    pdf_file_url = book.book_pdf.url
    return redirect(pdf_file_url)

def profile(request):
    return render(request, 'profile.html', {'user': request.user})


def my_activity(request):
    books = Book.objects.all()
    return render(request, 'my_activity.html',{'books': books})




@login_required
def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('home')
    else:
        form = VideoForm()

    return render(request, 'add_video.html', {'form': form})

def video(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'video_detail.html', {'video': video})


def translate_text(request):
    if request.method == 'POST':
        selected_language = request.POST.get('language')
        in_language = selected_language


        final = settings.MODEL.transcribe('Covaxinshort.mp4', task = 'translate')
        defa = final['text']
        limited = final['text'][0:487]

    # Translate the text
        translator = Translator(to_lang=in_language)
        translated_text = translator.translate(limited)

    return render(request, 'translated_text.html', {'defa': defa,'translated_text': translated_text})
from django.views.decorators.csrf import csrf_protect

from django.shortcuts import render

# import os
# import PyPDF2
# import re 
# import openai

# # Replace "YOUR_API_KEY" with your actual OpenAI API key
# openai.api_key = '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'




# def summarize_pdf(pdf_file_path):

#     pdf_summary_text = ""

#     pdf_file = open(pdf_file_path, 'rb')
#     pdf_reader = PyPDF2.PdfReader(pdf_file)

#     for page_num in range(len(pdf_reader.pages)):
#         page_text = pdf_reader.pages[page_num].extract_text().lower()
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful research assistant."},
#                 {"role": "user", "content": f"summarize this: {page_text}"},
#             ],
#             headers={"Authorization": f"Bearer {openai.api_key}"}
#         )
#         page_summary = response["choices"][0]["message"]["content"]
#         pdf_summary_text += page_summary + "\n"

#     pdf_file.close()

#     return pdf_summary_text

import os
import PyPDF2
from transformers import pipeline
def summarize_pdf(pdf_file_path):

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    pdf_text = ""
    pdf_file = open(pdf_file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    pdf_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text().lower()
        pdf_text += page_text.replace('\n', ' ') 

    pdf_file.close()
    final_text = ""
    chunk_size = 1024

    for i in range(0, len(pdf_text), chunk_size):
        chunk = pdf_text[i:i + chunk_size]
        
        response = summarizer(chunk, max_length=150, min_length=60, do_sample=False)
        final_text = final_text +" " + response[0]['summary_text']
        
        print(f"{response[0]['summary_text']}")

    return final_text

def summarize_pdf_view(request,book_id):
    book = get_object_or_404(Book, books_id=book_id)

    pdf_file_path = book.book_pdf.path
    if not pdf_file_path:
        return render(request, 'summarize_pdf.html', {'error': 'No PDF file specified.'})

    pdf_summary_text = summarize_pdf(pdf_file_path)

    return render(request, 'summarized_pdf.html', {'summary_text': pdf_summary_text})

import requests
from bs4 import BeautifulSoup

def search_project_gutenberg(request):
    if request.method == 'POST':
        book_title = request.POST['book_title']
        base_url = "http://www.gutenberg.org/ebooks/search/?query="

        # Replace spaces in the book title with "+" for the URL
        book_title = book_title.replace(" ", "+")
        search_url = base_url + book_title

        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find and collect the search results
            results = soup.find_all('li', class_='booklink')
            if results:
                search_results = []
                for result in results:
                    title = result.find('span', class_='title').get_text()
                    link = result.find('a')['href']
                    search_results.append({'title': title, 'link': f"http://www.gutenberg.org{link}"})
                return render(request, 'search_results.html', {'search_results': search_results})
            else:
                no_results = True
        else:
            no_results = True
    else:
        no_results = False

    return render(request, 'search.html', {'no_results': no_results})



# import os
# import PyPDF2
# from transformers import pipeline







# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# pdf_file_path = "/Users/hashishreddy/Desktop/MannSocialPhilos09.pdf"

# pdf_file = open(pdf_file_path, 'rb')
# pdf_reader = PyPDF2.PdfReader(pdf_file)

# pdf_text = ""
# for page_num in range(len(pdf_reader.pages)):
#     page_text = pdf_reader.pages[page_num].extract_text().lower()
#     pdf_text += page_text.replace('\n', ' ') 

# pdf_file.close()
# final_text = ""
# chunk_size = 1024

# for i in range(0, len(pdf_text), chunk_size):
#     chunk = pdf_text[i:i + chunk_size]
    
#     response = summarizer(chunk, max_length=150, min_length=60, do_sample=False)
    
#     print(f"{response[0]['summary_text']}")
