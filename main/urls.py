from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('enduser/', EndUserSignUpView.as_view(), name='end_user_signup'),
    path('user_select/', UserSelect.as_view(), name='user_select'),
    path('creator/', CreatorSignUpView.as_view(), name ='creator_signup'),
    path('home/', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('creatorprofile/<int:pk>', CreatorProfileView.as_view(), name='creator_profile'),
    path('creatorpost/', CreatorPostView.as_view(), name='creatorpost'),
    path('enduserfeed/', EndUserHomePage.as_view(), name='home_page_user'),
    path('creator_chat/<str:booth_name>/', views.booth, name='booth'),
    path('enduseredit/<int:pk>', EditEndUserProfile.as_view(), name='edit_enduser'),
    path('creatoredit/<int:pk>', EditCreatorProfile.as_view(), name='edit_creator'),
    path('creatorpostedit/<int:pk>', EditPost.as_view(), name='edit_creator_post'),
    path('createbid/<int:pk>', CreateBid.as_view(), name='create_bid'),
    path('editbid/<int:pk>', EditBid.as_view(), name='update_bid'),
    path('accept_bid/<int:bid_id>/', AcceptBidView.as_view(), name='accept_bid'),
    path('close_project/<int:pk>/', CloseProject.as_view(), name='close_project'),
    path('payment_successful/', PaymentSuccessfulView.as_view(), name='payment_successful'),
    path('payment_cancelled/', PaymentCancelledView.as_view(), name='payment_cancelled'),
    path('product_page', ProductPageView.as_view(), name='product_page'),
    path('stripe_webhook', StripeWebhookView.as_view(), name='stripe_webhook'),
    path('', Landing.as_view(), name='landing'),
    path('creatorlanding', CreatorLanding.as_view(), name='creatorlanding'),
    path('enduserlanding', EndUserLanding.as_view(), name='enduserlanding'),

  

    
    
]
