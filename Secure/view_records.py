from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import SecureRecord
from .rbac import is_allowed

@login_required
def view_records(request):
    if not is_allowed(request.user, "SELECT"):
        return HttpResponseForbidden("SELECT not allowed")

    records = SecureRecord.objects.all()
    data = "\n".join([r.name for r in records])
    return HttpResponse(f"Records:\n{data}")


@login_required
def delete_record(request, record_id):
    if not is_allowed(request.user, "DELETE"):
        return HttpResponseForbidden("DELETE not allowed")

    SecureRecord.objects.filter(id=record_id).delete()
    return HttpResponse("Record deleted")
