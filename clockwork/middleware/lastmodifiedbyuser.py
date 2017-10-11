from django.db.models import signals
from django.utils import timezone
from django.utils.functional import curry


class LastModifiedMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pub = ['publish', 'unpublish']
        if not any(x in request.path for x in pub):
            if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
                if hasattr(request, 'user') and request.user.is_authenticated():
                    user = request.user
                else:
                    user = None

                mark_whodid = curry(self.mark_whodid, user)
                signals.pre_save.connect(mark_whodid,  dispatch_uid=(self.__class__, request,), weak=False)

            response = self.get_response(request)

            if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
                signals.pre_save.disconnect(dispatch_uid=(self.__class__, request,))

            return response
        else:
            return self.get_response(request)

    @staticmethod
    def mark_whodid(user, sender, instance, **kwargs):
        if getattr(instance, 'user_created', None) == '':
            instance.user_created = user.username
        if hasattr(instance, 'user_updated'):
            instance.user_updated = user.username
            instance.date_updated = timezone.now()
