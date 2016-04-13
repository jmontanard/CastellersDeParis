from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

TECNICA = 'tecnica'
DIRECTIVA = 'directiva'

def is_tecnica_or_directiva( bundle):
    return bundle.request.user.groups.filter(name__in=[TECNICA, DIRECTIVA]).count() > 0

def is_tecnica( bundle):
    return bundle.request.user.groups.filter(name=TECNICA).count() > 0


def is_directiva( bundle):
    return bundle.request.user.groups.filter(name=DIRECTIVA).count() > 0

class CastellerAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        if is_tecnica_or_directiva(bundle):
            return object_list
        else:
            return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        if is_tecnica_or_directiva(bundle):
            return True
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        if is_tecnica_or_directiva(bundle):
            return object_list
        else:
            return []

    def create_detail(self, object_list, bundle):
        return is_tecnica_or_directiva(bundle)

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user or is_directiva():
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user or is_directiva()

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")


class UserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(pk=bundle.request.user.pk)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return []

    def create_detail(self, object_list, bundle):
        return False

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise object_list.filter(pk=bundle.request.user.pk)

    def delete_detail(self, object_list, bundle):
        raise bundle.obj == bundle.request.user

class EventAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return True

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list if is_tecnica_or_directiva(bundle) else []

    def create_detail(self, object_list, bundle):
        return is_tecnica_or_directiva()

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.organizer == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.organizer == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise object_list.filter(organizer=bundle.request.user)

    def delete_detail(self, object_list, bundle):
        raise bundle.obj.organizer == bundle.request.user