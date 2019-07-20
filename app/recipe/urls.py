from django.urls import path, include 
from rest_framework.routers import DefaultRouter

# import our view to render the viewset
from recipe import views 

# create our default router - will auto. create URLs for our viewset
    # you may have multiple URLs associated to a viewset
    # auto. registers the appropriate URLs for all the actions in our viewset
router = DefaultRouter()
# register our view - when working with a viewset register the view:
    # give it a name - we'll call it 'tags'
    # assign views.TagViewSet
# Registers our viewSet with our Router
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

# identify the app_name
    # so when using the reverse() it can lookup the right URLs
app_name = 'recipe' # add to main urls.py

# any path that matches our recipe app will pass in our router url
    # so all the urls created by the router will be included in the urlpatterns
    # and if we add more view sets we can register them here too & they'll auto. have the URLs created
urlpatterns = [
    path('', include(router.urls))
]