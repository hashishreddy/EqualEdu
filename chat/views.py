# views.py
from chat.models import Thread
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from members.models import CustomUser
from .forms import CreateThreadForm

@login_required
def messages_page(request):
    # Get the list of users (excluding the logged-in user and users with existing threads)
    users = CustomUser.objects.exclude(pk=request.user.id).exclude(
        thread_first_person__second_person=request.user
    ).exclude(
        thread_second_person__first_person=request.user
    )

    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')

    if request.method == 'POST':
        form = CreateThreadForm(request.POST, user=request.user)
        if form.is_valid():
            second_person = form.cleaned_data['second_person']

            # Create a new thread with the logged-in user and the selected second person
            new_thread = Thread.objects.create(first_person=request.user, second_person=second_person)

            # Redirect to the chat view for the newly created thread (replace 'view_name' with your actual chat view name)
            return redirect('chat:messages_page')

    else:
        # Initialize the form with the logged-in user
        form = CreateThreadForm(user=request.user)

    context = {
        'Threads': threads,
        'users': users,
        'form': form,
    }

    return render(request, 'messages.html', context)
