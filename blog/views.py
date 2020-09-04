from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, FeatureVideo
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, UserForm, VideoForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .post_perpage import getitemsno, setitemsno, drop_page_no
from django.db.models import Q



def post_list(request):
    try:
        post_page = request.GET.get('op')
        post_page = int(post_page)
    except:
        post_page = getitemsno()
         
    
    try:
        search = request.GET.get('search')
        posts = Post.objects.filter(title__icontains=search).order_by('-title') 
    except:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        search = ''
     
    stuff_for_frontend = paginate_helper(request,posts,post_page)
    post_video = FeatureVideo.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    latest_video = list(post_video)[0]   

    stuff_for_frontend['search'] = search  
    stuff_for_frontend['post_page'] = post_page
    stuff_for_frontend['postv'] = latest_video
    stuff_for_frontend['drop_page_no'] = drop_page_no

    return render(request, 'blog/post_list.html', stuff_for_frontend) 

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    stuff_for_frontend = {'post': post }
    return render(request, 'blog/post_detail.html', stuff_for_frontend)

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        stuff_for_frontend = {'form': form, 'post_edit':'New Post'}
    return render(request, 'blog/post_edit.html', stuff_for_frontend)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':

        # updating an existing form
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        stuff_for_frontend = {'form': form, 'post': post, 'post_edit':'Edit Post'}
    return render(request, 'blog/post_edit.html', stuff_for_frontend)

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    stuff_for_frontend = paginate_helper(request, posts, getitemsno())
    return render(request, 'blog/post_draft_list.html', stuff_for_frontend)
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
       form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form, 'title':post.title, 'comment_new_edit':'New Comment'})


@login_required
def edit_comment_to_post(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm(instance=comment)
        stuff_for_frontend = {'form': form, 'title':post.title ,'comment_new_edit': 'Edit Comment'}
    return render(request, 'blog/add_comment_to_post.html', stuff_for_frontend)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_approve(request, pk):
    # mydjangosite.com/comment/2/approve --> the 2nd comment will get approved
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'blog/signup.html', {'form': form})

def about(request):
    return render(request, 'blog/about.html')   

def contact(request):
    return render(request, 'blog/contact.html') 

@login_required
def videofeature(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.save()
            return redirect('/') 
    else:
        form = VideoForm()
        stuff_for_frontend = {'form': form}
    return render(request, 'blog/add_video.html', stuff_for_frontend) 


def paginate_helper(request, posts, getitemsno):
    paginator = Paginator(posts, getitemsno)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    stuff_for_frontend = {'posts': posts}
    return stuff_for_frontend