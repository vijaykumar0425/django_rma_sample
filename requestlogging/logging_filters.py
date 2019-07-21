from __future__ import absolute_import, unicode_literals
import django


class RequestFilter(object):
    """
    Filter that adds information about a *request* to the logging record.
    :param request:
    :type request: :class:`~django.http.HttpRequest`
    Extra information can be substituted in the formatter string:
    ``http_user_agent``
       The user agent string, provided by the client.
    ``path_info``
       The requested HTTP path.
    ``remote_addr``
       The remote IP address.
    ``request_method``
       The HTTP request method (*e.g.* GET, POST, PUT, DELETE, *etc.*)
    ``server_protocol``
       The server protocol (*e.g.* HTTP, HTTPS, *etc.*)
    ``username``
       The username for the logged-in user.
    """
    def __init__(self, request=None):
        """Saves *request* (a WSGIRequest object) for later."""
        self.request = request
        
    def filter(self,record):
        """
        Adds information from the request to the logging *record*.
        If certain information cannot be extracted from ``self.request``,
        a hyphen ``'-'`` is substituted as a placeholder.
        """
        request = self.request
        #Basic
        record.request_method = getattr(request, "method", "-")
        record.path_info = getattr(request, "path_info", "-")
        # User
        user = getattr(request, "user", None)
        record.username = user.username
        # Headers
        META = getattr(request, "META", {})  # NOQA: N806
        record.remote_addr = META.get("REMOTE_ADDR", "-")
        record.server_protocol = META.get("SERVER_PROTOCOL", "-")
        record.http_user_agent = META.get("HTTP_USER_AGENT", "-")
        return True