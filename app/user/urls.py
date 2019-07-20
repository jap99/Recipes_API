# path - lets us define different paths in our app
from django.urls import path, include

# import our view
from user import views 




# define our app name - lets us identify which app we're creating the URL from when using reverse()
app_name = 'user'

urlpatterns = [
    # first: our api will be user/create, 
    # second: the view we wire the URL to, 
    # third: give it a name we can use when using django's reverse() lookup function
        # give the same name that we use in our tests
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
] 
 # if path matches create/, we go to that view which will handle/render our API request
