from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404

from django.views.generic import DetailView

from users.models import CustomUser


class UserDashboardView(UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_dashboard.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        if self.kwargs.get('user_id') and self.request.user.is_staff:
            return get_object_or_404(CustomUser, pk=self.kwargs['user_id'])
        return CustomUser.objects.get(pk=self.request.user.pk)

    def test_func(self):
        user = self.request.user
        return user.is_authenticated or user.is_staff

    def handle_no_permission(self):
        raise Http404
