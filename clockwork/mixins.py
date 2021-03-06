from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
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


class GeneralAllPermissionMixin(PermissionRequiredMixin):
    permission_model = None
    raise_exception = True

    def get_permission_required(self):
        if self.permission_model is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_model attribute. Define {0}.permission_model, or override '
                '{0}.get_permission_required().'.format(self.__class__.__name__)
            )
        content_type = ContentType.objects.get_for_model(self.permission_model)
        permissions = Permission.objects.filter(content_type=content_type)
        return tuple("%s.%s" % (p.content_type.app_label, p.codename) for p in permissions)


class AuditTrailContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AuditTrailContextMixin, self).get_context_data(**kwargs)

        if self.object.user_created:
            user_created = User.objects.get(username=self.object.user_created)
            context['created_by'] = "%s, %s" % (user_created.first_name, user_created.last_name)
            context['created_on'] = self.object.date_created

        if self.object.user_updated:
            user_updated = User.objects.get(username=self.object.user_updated)
            context['updated_by'] = "%s, %s" % (user_updated.first_name, user_updated.last_name)
            context['updated_on'] = self.object.date_updated

        if hasattr(self.object, 'user_published'):
            if self.object.user_published:
                user_published = User.objects.get(username=self.object.user_published)
                context['published_by'] = "%s, %s" % (user_published.first_name, user_published.last_name)
                context['published_on'] = self.object.date_published

        return context
