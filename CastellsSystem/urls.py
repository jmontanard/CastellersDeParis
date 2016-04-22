"""CastellersDeParis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from tastypie.api import Api
from fortalesa.api import resources
from django.conf import settings
from django.conf.urls.static import static

v1_api = Api(api_name='v1')
v1_api.register(resources.CastellerResource())
v1_api.register(resources.CastellerAuthResource())
v1_api.register(resources.UserResource())
v1_api.register(resources.GroupResource())
v1_api.register(resources.EventResource())
v1_api.register(resources.EventTypeResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/v1/doc/',
        include('tastypie_swagger.urls', namespace='Fortalesa'),
        kwargs={
            "tastypie_api_module": v1_api,
            "namespace": "Fortalesa",
            "version": "0.1"}
        ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
