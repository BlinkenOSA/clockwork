from django.contrib import messages
from django.http import JsonResponse


class InlineSuccessMessageMixin(object):
    """
    Adds a success message on successful form submission.
    """
    success_message = ''

    def forms_valid(self, form, formset):
        response = super(InlineSuccessMessageMixin, self).forms_valid(form, formset)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class FormSetSuccessMessageMixin(object):
    """
    Adds a success message on successful form submission.
    """
    success_message = ''

    def formset_valid(self, formset):
        response = super(InlineSuccessMessageMixin, self).formset_valid(formset)
        success_message = self.get_success_message(formset)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, formset):
        return self.success_message


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
