from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from Secure.services.rbac import is_query_allowed


class RBACMiddleware(MiddlewareMixin):
    """
    Middleware to enforce RBAC rules on incoming requests
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Ignore admin & static files
        if request.path.startswith("/admin/"):
            return None

        if not request.user.is_authenticated:
            return None

        # Determine query type from HTTP method
        method_map = {
            "GET": "SELECT",
            "POST": "INSERT",
            "PUT": "UPDATE",
            "PATCH": "UPDATE",
            "DELETE": "DELETE",
        }

        query_type = method_map.get(request.method)

        if not query_type:
            return None

        # RBAC check
        if not is_query_allowed(request.user, query_type):
            return JsonResponse(
                {
                    "error": "Access denied by RBAC policy",
                    "query_type": query_type,
                },
                status=403
            )

        return None
