from django.urls import path

from result.views import PrivacyView, TermsView, receive_message

urlpatterns = [
    path('privacy/', PrivacyView.as_view()),
    path('terms/', TermsView.as_view()),
    path('', receive_message),
]
