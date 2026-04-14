from django.urls import path
from .views import ClassifyNameView, HomeView

urlpatterns = [
    path('', HomeView.as_view()),
    path('classify', ClassifyNameView.as_view(), name='classify'),
]