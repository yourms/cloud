from django_request_mapping import UrlPattern

from helpweb.views import MyView

urlpatterns = UrlPattern()
urlpatterns.register(MyView)