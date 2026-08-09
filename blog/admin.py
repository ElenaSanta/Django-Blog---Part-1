"""Στο αρχειο admin.py οριζουμε πως θα εμφανιζονται τα αρθρα στο admin panel, δηλαδη ποια πεδια θα εμφανιζονται,
πως θα γινεται η ταξινομηση και η φιλτραρισμα των αρθρων, και ποια πεδια θα ειναι αναζητησιμα.
"""
from django.contrib import admin
from .models import Post

admin.site.register(Post)

class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'author', 'publish', 'status']
	list_filter = ['status', 'created', 'publish', 'author']
	search_fields = ['title', 'body']
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ['author']
	date_hierarchy = 'publish'
	ordering = ['status', 'publish']

