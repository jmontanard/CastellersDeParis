from tastypie.resources import ModelResource
from fortalesa.models import Casteller, Event, EventType

class CastellerResource(ModelResource):
    class Meta:
        queryset = Casteller.objects.all()
        resource_name = 'casteller'
        #allowed_methods = ['get']

