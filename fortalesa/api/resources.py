from fortalesa.models import Casteller, Event, EventType
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseNotFound
from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from django.core.mail import send_mail
from django.conf import settings


class CastellerResource(ModelResource):
    class Meta:
        queryset = Casteller.objects.all()
        resource_name = 'casteller'
        allowed_methods = ['get']
        authorization = DjangoAuthorization()
        #authentication = DjangoAuthorization()


class CastellerAuthResource(ModelResource):
    class Meta:
        queryset = Casteller.objects.all()
        allowed_methods = ['get']
        resource_name = 'castellerauth'
        filtering = {
            'mail': ('exact'),
            'birthday': ('exact')
        }

    def dispatch(self, request_type, request, **kwargs):
        return super(CastellerAuthResource, self).dispatch(request_type, request, **kwargs)

    def get_list(self, request, **kwargs):
        mail = request.GET.get(u'mail', None)
        birthday = request.GET.get(u'birthday', None)
        if mail is None or birthday is None:
            return HttpResponseBadRequest('mail and birthday must be provided')

        # TODO: Uncached for now. Invalidation that works for everyone may be
        #       impossible.
        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        if len(objects)==0:
            return HttpResponseNotFound('The Casteller does not exist')
        else:
            casteller = objects[0]
            user = casteller.user
            if user is None:
                # Create user
                user = User(username=casteller.mail)
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
                casteller.user = user
                casteller.save()
            else:
                # new password
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
            #TODO: Send Email
            return HttpResponse(content='Email sended\npass:{}'.format(password))
        #response.content.
       # if len(response.content.)
    def send_email(self, mail, password):
        send_mail('New Password',
                  'Your new user is:{}\nYour new password is:{}'.format(mail,password),
                  settings.DEFAULT_FROM_EMAIL,
                  [mail], fail_silently=False)


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']
        # Add it here.
        authentication = Authentication()