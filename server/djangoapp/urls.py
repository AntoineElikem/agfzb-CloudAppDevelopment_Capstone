from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [

    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

 path('', views.get_dealerships, name='index'),

    # path for about view
   path('about/', views.about, name='about'),

    # path for contact us view
    path('contact/', views.contact, name='contact'),

    # path for registration

    # path for login
    path('login/', views.login_request, name='login'),

    # path for logout
    path('logout/', views.logout_request, name='logout'),

    # path for signup
    path('signup/', views.registration_request, name='signup'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for get dealer details
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for adding reviews
    path('review/add/', views.add_review, name='add_review'),

    # [atj fpr add review]
    path('add_review/<int:dealer_id>/', views.add_review, name='add_review'),


    # path for dealer reviews view
    

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)