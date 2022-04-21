from django.urls import path

from .views import ProfileDetailView, ProfileListView


app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='profile-list'), 
    path('<slug:username>/', ProfileDetailView.as_view(), name='profiledetail'),
]