from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import stripe
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import time
from django.http import HttpResponse



class UserCreateView(CreateView):
    form_class = UserCreate
    template_name = "main/user_create.html"
    context_object_name = "register"

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]

        user = authenticate(username=username, password=password)
        login(self.request, user)

        if user:
            return redirect('user_select')

        return super().form_valid(form)
    

    

class EndUserSignUpView(LoginRequiredMixin, CreateView):
    model = EndUser
    form_class = EndUserForm
    template_name = 'main/enduser_signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        end_user = form.save(commit=False)
        end_user.user = self.request.user
        end_user.save()
        return super().form_valid(form)

class CreatorSignUpView(LoginRequiredMixin, CreateView):
    model = Creator
    form_class = CreatorForm
    template_name = 'main/creator_signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        creator = form.save(commit=False)
        creator.user = self.request.user
        creator.save()
        return super().form_valid(form)
    
class CreatorProfileView(ListView):
    model = Creator  
    context_object_name = 'creatorprofile'
    template_name = 'main/creatorprofile.html'

    def get_queryset(self):
        pk = self.kwargs.get('pk')  # Retrieve the 'pk' parameter from the URL
        return Creator.objects.get(user_id=pk)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        creator = Creator.objects.get(user=user)
        posts = Post.objects.filter(creator=user.id)
        last_10_bids = Bid.highest_bids()  # Get the last 10 bids
        context['creator'] = creator
        context['posts'] = posts
        context['last_10_bids'] = last_10_bids  # Pass the last 10 bids to the template
        return context
    
#class EndUserProfileView(ListView):
    #model = EndUser
    #context_object_name = 'enduserprofile'
    #template_name = 'main/enduserprofile.html'
    #def get_queryset(self):
        #pk = self.kwargs.get('pk')
        #return EndUser.objects.get(user_id = pk) 

class HomeView(LoginRequiredMixin,ListView):
    model = Creator
    template_name = 'main/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_role = self.get_user_role(self.request.user)
        context['user_role'] = user_role
        return context

    def get_user_role(self, user):
        if hasattr(user, 'creator'):
            return 'creator'
        elif hasattr(user, 'enduser'):
            return 'enduser'
        else:
            return None


        
class LoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    context_object_name = "login"

    def get_success_url(self):
        return reverse_lazy('home')
    
class UserSelect(LoginRequiredMixin,View):
    def get(self, request):
        form = UserTypeForm()
        return render(request, 'main/user_type.html', {'form': form})


    def post(self, request):
            form = UserTypeForm(request.POST)
            if form.is_valid():
                user_type = form.cleaned_data['user_type']
                if user_type == 'creator':
                    return redirect('creator_signup')
                elif user_type == 'end_user':
                    return redirect('end_user_signup')
            return render(request, 'main/user_type.html', {'form': form})
        
        

class CreatorPostView(CreateView):
    form_class = CreatorPostForm
    template_name  = 'main/creatorpost.html'
    context_object_name = 'creatorpostform'

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        creator = Creator.objects.get(user=user)
        post.creator = creator
        post.save()
        return redirect('home')  



class EndUserHomePage(ListView):
    model = Post
    template_name = 'main/filtered_posts.html'
    context_object_name = 'feed'

    def get_queryset(self):
        end_user = get_object_or_404(EndUser, user=self.request.user)
        required_field = end_user.required
        queryset = super().get_queryset()
        filtered_posts = queryset.filter(creator__profession=required_field)
        return filtered_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        end_user = get_object_or_404(EndUser, user=self.request.user)
        feed = []
        for post in context['feed']:
            bid = Bid.objects.filter(project=post).first()
            feed.append({
                'post': post,
                'bid': bid,
            })
        context['feed'] = feed
        return context
@login_required
def booth(request, booth_name):
    bid = Bid.objects.filter(project__title=booth_name, accepted=True).first()
    post = Post.objects.filter(title=booth_name).first()

    if post.closed:
        message = "This Creator did not accept your bid, and this project has been closed."
    else:
        message = "This Creator has not accepted a bid yet."

    return render(request, "main/booth.html", {
        'booth_name': booth_name,
        'username': request.user.email,
        'accepted_bid': bid,
        'message': message,
    })


class EditCreatorProfile(LoginRequiredMixin, UpdateView):
    model = Creator
    form_class = CreatorForm
    template_name = 'main/edit_creator_profile.html'
    success_url = reverse_lazy('home')


class EditEndUserProfile(LoginRequiredMixin, UpdateView):
    model = EndUser
    form_class = EndUserForm
    template_name = 'main/edit_enduser_profile.html'
    success_url = reverse_lazy('home')

class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CreatorPostForm
    template_name  = 'main/creatorpost_edit.html'
    def get_success_url(self):

        return reverse_lazy('creator_profile', kwargs={'pk': self.object.creator.pk})
    


class CreateBid(LoginRequiredMixin, CreateView):
    form_class = CreateBid
    template_name = 'main/createbid.html'
    context_object_name = 'creatorbidform'

    def form_valid(self, form):
        bidder = self.request.user.enduser
        project_id = self.kwargs['pk']
        project = get_object_or_404(Post, pk=project_id)

        try:
            # Check if a bid by the same bidder already exists for the project
            bid = Bid.objects.get(project=project, bidder=bidder)
            bid.bid_price = form.cleaned_data['bid_price']
            bid.custom_option = form.cleaned_data['custom_option']
            bid.comments = form.cleaned_data['comments']
            bid.save()
        except Bid.DoesNotExist:
            bid = form.save(commit=False)
            bid.bidder = bidder
            bid.project = project
            bid.save()
        
        return redirect('home')
class EditBid(LoginRequiredMixin, UpdateView):
    model = Bid
    template_name = 'main/edit_bid.html'
    success_url = reverse_lazy('home')
    fields = ['bid_price', 'custom_option', 'comments']


class AcceptBidView(View):
    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id)
        project = bid.project

        has_accepted_bid = Bid.objects.filter(project=project, accepted=True).exists()
        if has_accepted_bid:
            return redirect('creator_profile', pk=request.user.id, error='A bid is already accepted for this project.')

        bid.accepted = True
        bid.save()

        return redirect('creator_profile', pk=request.user.id)
    
class CloseProject(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        if post.closed:
            return redirect('creator_profile', pk=request.user.id, error='A bid is already accepted for this project.')
        

        post.closed = True
        post.save()

        return redirect('creator_profile', pk=request.user.id)
    

class ProductPageView(View):
    template_name = 'main/product_page.html'

    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
        return render(request, self.template_name)

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)


class PaymentSuccessfulView(View):
    template_name = 'main/payment_successful.html'

    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
        checkout_session_id = request.GET.get('session_id', None)
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer = stripe.Customer.retrieve(session.customer)
        
        return render(request, self.template_name, {'customer': customer})


class PaymentCancelledView(View):
    template_name = 'main/payment_cancelled.html'

    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
        return render(request, self.template_name)


class StripeWebhookView(View):
    @csrf_exempt
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
        time.sleep(10)
        payload = request.body
        signature_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            session_id = session.get('id', None)
            time.sleep(15)
            
        return HttpResponse(status=200)
    
class Landing(ListView):
    model = User
    context_object_name = 'landing'
    template_name = 'main/index.html'

class CreatorLanding(ListView):
    model = Creator
    context_object_name = 'creatorlanding'
    template_name = 'main/creatorlanding.html'

class EndUserLanding(ListView):
    model = EndUser
    context_object_name = 'enduserlanding'
    template_name = 'main/enduserlanding.html'