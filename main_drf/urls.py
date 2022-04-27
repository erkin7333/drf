from django.urls import path
from .views import (AktiyorListView, AktiyorDetailtView)
from .genericviews import (KinoListView, KinoDetailetView, ReviewCreateView,
                           AddStarReytingView)
from rest_framework.urlpatterns import format_suffix_patterns
from .api_viewset import AktyroViewSet, KinoViewSet, ReviewCreateViewSet, AddStarReytingViewSet
app_name = "main_drf"


urlpatterns = format_suffix_patterns([
    path('kino/', KinoViewSet.as_view({'get': 'list'})),
    path('kino/<int:pk>/', KinoViewSet.as_view({'get': 'retrieve'})),
    path('review/', ReviewCreateViewSet.as_view({'post': 'create'})),
    path('reting/', AddStarReytingViewSet.as_view({'post': 'create'})),
    path('aktyor/', AktyroViewSet.as_view({'get': 'list'})),
    path('aktyor/<int:pk>/', AktyroViewSet.as_view({'get': 'retrieve'})),
])



# urlpatterns = [
#     path('kino/', KinoListView.as_view(), name='kino'),
#     path('kino/<int:pk>/', KinoDetailetView.as_view(), name='kinolar'),
#     path('review/', ReviewCreateView.as_view(), name='review'),
#     path('reting/', AddStarReytingView.as_view(), name='reting'),
#     path('aktyor/', AktiyorListView.as_view(), name="aktyor"),
#     path('aktyor/<int:pk>/', AktiyorDetailtView.as_view(), name="aktyor"),
# ]