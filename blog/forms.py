"""Στο αρχειο forms.py οριζουμε φορμες που θα χρησιμοποιηθουν στην εφαρμογη μας. Οι φορμες χρησιμοποιούνται 
για να λαβουμε, να επεξεργαστουμε και να τα αποθηκευσουμε στη βαση μας δεδομενα του χρηστη
"""
from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label="Your name")
    email = forms.EmailField(label="Your email")
    to = forms.EmailField(label="Recipient's email")
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Comments"
    )

class CommentForm(forms.ModelForm):
    #Βαζω τη Meta class για να περάσω τις πληροφορίες που θέλω μέσω του μοντελού χρησιμοποιώντας τα πεδια του
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


