"""
contains :class:`ForumModeMiddleware`, which is
enabling support of closed forum mode
"""
from future import standard_library
standard_library.install_aliases()
from builtins import object
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.urlresolvers import resolve
from askbot.conf import settings as askbot_settings
from askbot.utils.views import is_askbot_view
import urllib.request, urllib.parse, urllib.error

ALLOWED_VIEWS = (
    'askbot.views.meta.config_variable',
)


def is_view_allowed(func):
    """True, if view is allowed to access
    by the special rule
    """
    if hasattr(func, '__name__'):
        view_path = func.__module__ + '.' + func.__name__
    elif hasattr(func, '__class__'):
        view_path = func.__module__ + '.' + func.__class__.__name__
    else:
        view_path = ''

    return view_path in ALLOWED_VIEWS

class ForumModeMiddleware(object):
    """protects forum views is the closed forum mode"""

    def process_request(self, request):
        """when askbot is in the closed mode
        it will let through only authenticated users.
        All others will be redirected to the login url.
        """
        if (askbot_settings.ASKBOT_CLOSED_FORUM_MODE
                and request.user.is_anonymous()):
            resolver_match = resolve(request.path)
            if not is_askbot_view(resolver_match.func):
                return

            internal_ips = getattr(settings, 'ASKBOT_INTERNAL_IPS', None)
            if internal_ips and request.META.get('REMOTE_ADDR') in internal_ips:
                return None

            if is_view_allowed(resolver_match.func):
                return

            if is_askbot_view(resolver_match.func):
                request.user.message_set.create(
                    _('Please log in to use %s') % \
                    askbot_settings.APP_SHORT_NAME
                )
                redirect_url = '%s?next=%s' % (
                    settings.LOGIN_URL,
                    urllib.parse.quote_plus(request.get_full_path())
                )
                return HttpResponseRedirect(redirect_url)
        return None
