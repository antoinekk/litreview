from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . import forms
from .models import Review, Ticket, UserFollows
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from itertools import chain
from django.db import IntegrityError

User = get_user_model()

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('feed')
        message = 'Identifiants invalides.'
    return render(request, 'login.html', context={'form': form, 'message': message})

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    return render(request, 'signup.html', context={'form': form})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    else:
        form = forms.TicketForm()
    return render(request, 'create_ticket.html', context={'form': form})

@login_required
def create_review(request):
    if request.method == 'POST':
        ticketform = forms.TicketForm(request.POST, request.FILES)
        reviewform = forms.ReviewForm(request.POST)
        if ticketform.is_valid() and reviewform.is_valid():
            ticket = ticketform.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = reviewform.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    else:
        ticketform = forms.TicketForm()
        reviewform = forms.ReviewForm()
    return render(request, 'create_review.html', context={'ticketform': ticketform, 'reviewform': reviewform})

@login_required
def user_posts(request):
    tickets_review = Ticket.objects.filter(user=request.user, review__isnull=False)
    tickets_no_review = Ticket.objects.filter(user=request.user, review__isnull=True)
    reviews = Review.objects.filter(user=request.user)
    posts_list_user = sorted(chain(tickets_review, tickets_no_review, reviews), key=lambda post: post.time_created, reverse=True)
    return render(request, 'posts.html', context = {'posts_list_user': posts_list_user, 'tickets_no_review': tickets_no_review})

@login_required
def feed(request):
    users_followed = UserFollows.objects.filter(user=request.user).order_by('followed_user').values_list('followed_user_id')
    tickets_user_no_review = Ticket.objects.filter(user=request.user, review__isnull=True)
    tickets_followed_no_review = Ticket.objects.filter(user__in=users_followed, review__isnull=True)
    tickets_no_review = list(chain(tickets_user_no_review, tickets_followed_no_review))
    reviews_user = Review.objects.filter(user=request.user)
    reviews_followed = Review.objects.filter(user__in=users_followed)
    reviews = list(chain(reviews_user, reviews_followed))
    posts_list = sorted(chain(tickets_no_review, reviews), key=lambda post: post.time_created, reverse=True)
    return render(request, 'feed.html', context = {'posts_list': posts_list})

@login_required
def follow_user(request):
    message = ''
    if request.method == 'POST':
        form = forms.SubscriptionForm(request.POST)
        if form.is_valid():
            try:
                followed_user = User.objects.get(username=form['subscribe'].value())
                if request.user == followed_user:
                    message = 'Vous ne pouvez pas vous suivre vous-même'
                else:
                    try:
                        UserFollows.objects.create(user=request.user, followed_user=followed_user)
                        message = 'Vous suivez maintenant cet utilisateur'
                    except IntegrityError:
                        message = 'Vous suivez déjà cet utilisateur'

            except User.DoesNotExist:
                message = 'Utilisateur inconnu'
    else:
        form = forms.SubscriptionForm()
    user_followed = UserFollows.objects.filter(user=request.user).order_by('followed_user')
    followed_by = UserFollows.objects.filter(followed_user=request.user).order_by('user')
    return render(request, 'subscribe.html', context = {'form': form, 'message': message, 'user_followed': user_followed, 'followed_by': followed_by, 'title': 'Subscriptions'})

@login_required
def unfollow_user(request, pk):
    user_to_unfollow = UserFollows.objects.get(pk=pk)
    user_to_unfollow.delete()
    return redirect('subscribe')

@login_required
def response_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        reviewform = forms.ReviewForm(request.POST)
        if reviewform.is_valid():
            review = reviewform.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('posts')
    else:
        reviewform = forms.ReviewForm()
    return render(request, 'response_ticket.html', context = {'ticket': ticket, 'reviewform': reviewform})

@login_required
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.delete()
    return redirect('posts')

@login_required
def delete_review(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect('posts')

@login_required
def modify_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        ticketform = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if ticketform.is_valid():
            ticketform.save()
            return redirect('posts')
    else:
        ticketform = forms.TicketForm(instance=ticket)
    return render(request, 'modify_ticket.html', context = {'ticketform': ticketform})

@login_required
def modify_review(request, pk):
    review = Review.objects.get(pk=pk)
    ticket = review.ticket
    if request.method == 'POST':
        reviewform = forms.ReviewForm(request.POST, instance=review)
        if reviewform.is_valid():
            reviewform.save()
            return redirect('posts')
    else:
        reviewform = forms.ReviewForm(instance=review)
    return render(request, 'modify_review.html', context = {'reviewform': reviewform, 'ticket': ticket})
