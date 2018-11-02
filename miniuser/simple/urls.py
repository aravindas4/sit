from django.urls import path, include
from simple import views as simple_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', simple_views.UserViewSet)
router.register(r'issues', simple_views.IssuesViewSet)

urlpatterns = [
    path('create/', simple_views.CreateUser.as_view()),
    path('login/', simple_views.Login.as_view()),
    path('', include(router.urls))
]