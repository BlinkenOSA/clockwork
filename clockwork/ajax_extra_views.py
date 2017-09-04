from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext
from fm.views import AjaxDeleteView


class AjaxDeleteProtectedView(AjaxDeleteView):
    success_message = ugettext("Record was removed successfully!")
    error_message = ugettext("Record can't be deleted, because there are related records!")

    def get_error_message(self):
        return self.error_message

    def get_success_message(self):
        return self.success_message

    def get_success_result(self):
        return {'status': 'ok', 'message': self.get_success_message()}

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.pre_delete()
            self.object.delete()
            self.post_delete()
            if self.request.is_ajax():
                return self.render_json_response(self.get_success_result())
        except ProtectedError:
                return self.render_json_response({'status': 'error',
                                                  'message': self.get_error_message()})

        return HttpResponseRedirect(self.get_success_url())
