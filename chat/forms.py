# forms.py
from django import forms
from members.models import CustomUser
from chat.models import Thread
from django.db.models import Q 



class CreateThreadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateThreadForm, self).__init__(*args, **kwargs)
        if user:
            # Get the list of users who are not the logged-in user
            users = CustomUser.objects.exclude(id=user.id)
            
            # Get the list of users who are already connected through threads
            connected_users = CustomUser.objects.filter(
                Q(thread_first_person__second_person=user) |
                Q(thread_second_person__first_person=user)
            )
            
            # Exclude connected users from the available users
            self.fields['second_person'].queryset = users.exclude(id__in=connected_users)

    second_person = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(),  # We set an empty initial queryset
        label="Start a new chat with"
    )
