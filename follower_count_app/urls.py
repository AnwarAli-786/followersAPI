from django.urls import path, include
from follower_count_app.views import FollowerCountView

urlpatterns = [
    path('getFollowerCount/', FollowerCountView.as_view()),
]

