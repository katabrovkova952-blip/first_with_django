from django.urls import path

from .views import AssistantAskView

app_name = 'assistant'

urlpatterns = [path('ask/', AssistantAskView.as_view())]
