"""Εδω οριζουμε την εφαρμογη blog. Οταν δημιουργουμε μια εφαρμογη στο Django, πρεπει να ορισουμε την κλαση
AppConfig για να μπορει το Django να την αναγνωρισει. Η κλαση AppConfig περιεχει πληροφοριες για την εφαρμογη 
"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
