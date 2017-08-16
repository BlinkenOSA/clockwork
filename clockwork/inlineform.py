from django.http import HttpResponseRedirect
from extra_views.advanced import ProcessFormWithInlinesView, ModelFormWithInlinesMixin
from fm.views import AjaxFormMixin
from django.template.loader import render_to_string


class FormWithInlinesMixin(AjaxFormMixin, ModelFormWithInlinesMixin):
    """
    A mixin that provides a way to show and handle a modelform and inline
    formsets in a request.
    """
    inlines = []

    def get_inlines(self):
        """
        Returns the inline formset classes
        """
        return self.inlines

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        self.object = form.save()
        for formset in inlines:
            formset.save()

        if self.request.is_ajax():
            return self.render_json_response(self.get_success_result())
        else:
            return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, inlines):
        """
        If the form or formsets are invalid, re-render the context data with the
        data-filled form and formsets and errors.
        """
        if self.request.is_ajax():
            return self.render_json_response(self.get_error_result(form, inlines))
        else:
            return self.render_to_response(self.get_context_data(form=form, inlines=inlines))

    def get_error_result(self, form, inlines):
        html = render_to_string(
            self.template_name,
            self.get_context_data(form=form, inlines=inlines),
            request=self.request
        )
        return {'status': 'error', 'message': html}


class BaseCreateWithInlinesView(FormWithInlinesMixin, ProcessFormWithInlinesView):
    def get(self, request, *args, **kwargs):
        self.object = None
        return super(BaseCreateWithInlinesView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(BaseCreateWithInlinesView, self).post(request, *args, **kwargs)


class CreateWithInlinesAjaxView(BaseCreateWithInlinesView):
    template_name_suffix = '_form'


class BaseUpdateWithInlinesView(FormWithInlinesMixin, ProcessFormWithInlinesView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseUpdateWithInlinesView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BaseUpdateWithInlinesView, self).post(request, *args, **kwargs)


class UpdateWithInlinesAjaxView(BaseUpdateWithInlinesView):
    template_name_suffix = '_form'
