from fortalesa.models import Casteller, Event, EventType
from fortalesa.api import authorization
from fortalesa.api.cors_resource import CORSModelResource
from django.contrib.auth.models import User, Group

from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseNotFound
from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.utils import trailing_slash
from tastypie.models import ApiKey, create_api_key
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.db import models

from tastypie.authentication import BasicAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from django.core.mail import send_mail
from django.conf import settings

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CastellerResource(CORSModelResource):
    class Meta:
        queryset = Casteller.objects.all()
        resource_name = 'casteller'
        allowed_methods = ['get', 'patch']
        authorization = authorization.CastellerAuthorization()
        authentication = BasicAuthentication()


class CastellerAuthResource(CORSModelResource):
    class Meta:
        queryset = Casteller.objects.all()
        allowed_methods = ['post']
        resource_name = 'castellerauth'
        filtering = {
            'mail': ('exact'),
            'birthday': ('exact')
        }

    def dispatch(self, request_type, request, **kwargs):
        return super(CastellerAuthResource, self).dispatch(request_type, request, **kwargs)

    def post_list(self, request, **kwargs):
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
            self.send_email(casteller.mail, password)
            return HttpResponse(content='Email sended:{}'.format( user.email))
        #response.content.
       # if len(response.content.)
    def send_email(self, mail, password):
        send_mail('New Password',
                  'Your new user is: {}\nYour new password is: {}'.format(mail, password),
                  settings.DEFAULT_FROM_EMAIL,
                  [mail], fail_silently=False)


class UserResource(CORSModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['get', 'post']
        resource_name = 'user'

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        logger.debug('The login method')
        logger.debug(request.body)

        self.method_check(request, allowed=['post'])
        #print 4444; import pdb;pdb.set_trace()

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        logger.debug('The login method')

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)


        if user:
            logger.debug("user authenticated")

            if user.is_active:
                logger.debug("user is active")
                login(request, user)
                logger.debug("user loged")

                try:
                    key = ApiKey.objects.get(user=user)
                    logger.debug("user key {}:".format(key))

                except ApiKey.DoesNotExist:
                    logger.debug("User api key do not exist")

                    return self.create_response(
                        request, {
                            'success': False,
                            'reason': 'missing key',
                        },
                        HttpForbidden,
                    )
                logger.debug("user Api key returned")

                ret = self.create_response(request, {
                    'success': True,
                    'username': user.username,
                    'key': key.key
                })
                #print 5656; import pdb;pdb.set_trace()
                return ret
            else:
                logger.debug("user is not active")

                return self.create_response(
                    request, {
                        'success': False,
                        'reason': 'disabled',
                    },
                    HttpForbidden,
                )
        else:
            logger.debug("user not authenticated")

            return self.create_response(
                request, {
                    'success': False,
                    'reason': 'invalid login',
                    'skip_login_redir': True,
                },
                HttpUnauthorized,
            )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)

models.signals.post_save.connect(create_api_key, sender=User)



class GroupResource(CORSModelResource):
    class Meta:
        queryset = Group.objects.all()
        resouce_name = 'group'
        allowed_methods = ['get']



class EventResource(CORSModelResource):
    event_type = fields.ToOneField('fortalesa.api.resources.EventTypeResource','type')
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        allowed_methods = ['get', 'post', 'patch', 'delete']
        filtering = {
            "date": ['lte', 'gte'],
            "type": ALL_WITH_RELATIONS,
        }
        authorization = authorization.EventAuthorization()
        authentication = BasicAuthentication()

class EventTypeResource(CORSModelResource):
    events = fields.ToManyField('fortalesa.api.resources.EventResource', 'events')
    class Meta:
        queryset = EventType.objects.all()
        resource_name = 'event'
        allowed_methods = ['get']
        filter = {'pk': ALL}
        authorization = ReadOnlyAuthorization()
        authentication = BasicAuthentication()

