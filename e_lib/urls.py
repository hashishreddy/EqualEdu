from django.urls import path
from.import views
urlpatterns = [
    path('',views.home,name="home"),
    path('summary/',views.summary,name="summary"),  
    path('add_book/',views.add_book, name="add_book"),
    path('subjects/', views.subject_list, name='subject_list'), 
    path('books/<int:subject_id>/', views.books_by_subject, name='books_by_subject'),
    path('book/<int:books_id>/', views.book_detail, name='book_detail'),
    path('search_book/', views.search_book, name='search_book'), 
    path('view-pdf/<int:book_id>/', views.view_pdf, name='view_pdf'),
    path('profile/', views.profile, name='profile'), 
    path('add_video/',views.add_video, name="add_video"),
    path('video/',views.video, name="video"),
    path('my_activity/', views.my_activity, name='my_activity'), 
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    path('translate/', views.translate_text, name='translate-text'),
    path('summarize-pdf/<int:book_id>/', views.summarize_pdf_view, name='summarize_pdf'),
    path('search', views.search_project_gutenberg, name='search'),


]