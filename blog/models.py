""" Εδώ ορίζονται τα μοντέλα για την εφαρμογή blog. Τα μοντέλα αντιπροσωπεύουν τις δομές δεδομένων που 
χρησιμοποιούνται στην εφαρμογή και καθορίζουν τον τρόπο αποθήκευσης και ανάκτησης των δεδομένων από τη βάση
"""
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'P', 'Published'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )



class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:             # Σαν τα Annotations στη Java (@OrderBy() για ταξινομηση)
        ordering = ['created']
        #Σαν τα περιεχομενα σε βιβλιο
        indexes = [
            models.Index(fields=['created']),
        ]  

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'