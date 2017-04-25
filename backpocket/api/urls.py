from django.conf.urls import url, include
from rest_framework import routers
from backpocket.users.views import UserViewSet

router = routers.DefaultRouter()
# router.register(r'links', UserViewSet)
# router.register(r'lists', UserViewSet)
# router.register(r'pages', UserViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
