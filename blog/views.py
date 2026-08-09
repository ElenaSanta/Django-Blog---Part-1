"""Εδω ορίζονται οι προβολές (views) για την εφαρμογή blog. Κάθε προβολή είναι μια συνάρτηση που χειρίζεται 
τα αιτήματα HTTP και κάνει τις κατάλληλες ανακατευθύνσεις.
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag

def post_list(request, tag_slug=None):
    post_list = Post.objects.filter(status=Post.Status.PUBLISHED)
    tag = None

    if tag_slug:
        # Βρίσκουμε το tag από το URL και φιλτράρουμε τα posts
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'blog/post/list.html', {
        'posts': posts,
        'page_obj': posts,
        'tag': tag
    })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    #Σχόλια(Λίστα και φόρμα)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })




def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"New mail: {post.title} from: {cd['name']}"
            message = f"Read \"{post.title}\" at {post_url}\n\n" \
                      f"Comments by {cd['name']}: {cd['comments']}"
            
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'sent': sent
    })


@require_POST      
#Προσθέτουμε το @require_POST decorator για να επιτρέψουμε μόνο POST αιτήματα σε αυτή τη view και οχι άλλα HTTP requests.
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    
    if form.is_valid():
        # Δημιουργούμε το αντικείμενο Comment χωρίς όμως να το σώσουμε ακόμα στη βάση (commit=False)
        comment = form.save(commit=False)
        # Συνδέουμε το σχόλιο με το συγκεκριμένο άρθρο
        comment.post = post
        comment.active = True
        comment.save()
    else:
        print("--- ΣΦΑΛΜΑΤΑ ΦΟΡΜΑΣ: ---", form.errors)

    return render(request, 'blog/post/comment.html', {
        'post': post,
        'form': form,
        'comment': comment
    })