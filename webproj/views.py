from django.contrib.auth.decorators import login_required
from django.http.response import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import PostForm, UpdateUserForm, CommentForm
from .models import Forum, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from requests_oauthlib import OAuth1Session
from django.conf import settings
import os
import json


# Create your views here.
def webproj(request):
    posts = Forum.objects.all().order_by('-created_at')

    context = {'posts': posts}
    return render(request, 'index.html', context)


def detail_post(request, id):
    post = Forum.objects.get(id=id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            comment.save()
            return redirect('detail_post', id=post.id)
    else:
        comment_form = CommentForm()

    context = {'post': post, 'comments': comments, 'form': comment_form}
    return render(request, 'detail_post.html', context)


@login_required(login_url='login')
def create_post(request):
    form = PostForm(request.POST or None)
    # check whether it's valid:
    if form.is_valid():
        # save the record into the db
        forum = form.save(commit=False)
        forum.user = request.user
        forum.save()
        messages.success(request, "New Post Created Successfully")
        return redirect('webproj')

    return render(request, 'create-post.html', {'form': form})


@login_required(login_url='login')
def delete_post(request):
    if request.method == "GET":
        post_id = request.GET.get('post_id', None)
        post = get_object_or_404(Forum, id = post_id)
        if post and post.user == request.user:
            post.delete()
            messages.success(request, "Post was deleted successfully!")
            return redirect('webproj')
        else:
            return HttpResponseForbidden()
    raise Http404()


@login_required(login_url='login')
def edit_post(request):
    if request.method == "GET":
        post_id = request.GET.get('post_id', None)
        post = get_object_or_404(Forum, id = post_id)
        if post_id and post.user == request.user:
            form = PostForm(instance=post)
            return render(request, 'edit-post.html', {'form': form, 'post': post})
        else:
            return HttpResponseForbidden()
    elif request.method == "POST":
        form = PostForm(request.POST or None)
        post_id = request.POST.get('post_id', None)

        if post_id and form.is_valid():
            # update the record into the db
            post = get_object_or_404(Forum, id = post_id)
            post.post_title = form.cleaned_data['post_title']
            post.post = form.cleaned_data['post']
            post.save()

            messages.success(request, "Post was updated successfully!")
            return redirect('webproj')
    raise Http404()



def news_view(request):

    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET

    access_token = settings.TWITTER_ACCESS_TOKEN
    access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

    # params = {"ids": "1453760137005518848", "tweet.fields": "created_at"}
    params = {"max_results": "50", "tweet.fields": "created_at"}

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # response = oauth.get(
    #     "https://api.twitter.com/2/users/by/username/NBA"
    # )
    # json_response = response.json()
    # data = json.dumps(json_response, indent=4, sort_keys=True)
    # print(data)

    # response = oauth.get(
    #     "https://api.twitter.com/2/tweets", params=params
    # )
    response = oauth.get(
        "https://api.twitter.com/2/users/19923144/tweets", params=params
    )

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))
    json_response = response.json()
    print(json_response)
    context = {"tweets": json_response['data']}
    return render(request, 'news.html', context)



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('webproj')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def update_profile_view(request):
    if request.method == 'POST':
        form = UpdateUserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('webproj')
    else:
        form = UpdateUserForm()
    return render(request, 'update-profile.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('webproj')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    # logs out user
    logout(request)
    # user redirected to home page after logging out
    return redirect('webproj')

