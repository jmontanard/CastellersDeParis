from tastypie.resources import ModelResource
from fortalesa.models import Casteller, Event, EventType
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization

class CastellerResource(ModelResource):
    class Meta:
        queryset = Casteller.objects.all()
        resource_name = 'casteller'
        #allowed_methods = ['get']
        authorization = DjangoAuthorization()

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']
        # Add it here.
        authentication = ApiKeyAuthentication()