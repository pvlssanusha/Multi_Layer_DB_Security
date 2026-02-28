from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import SecureRecord, SQLQueryLog
from .rbac import is_allowed

from .rbac import get_user_role


@login_required
def records_page(request):

    # -----------------------------
    # HANDLE INSERT OPERATION
    # -----------------------------
    if request.method == "POST" and "add_record" in request.POST:

        action = "INSERT"
        allowed = is_allowed(request.user, action)

        # Log the query attempt
        SQLQueryLog.objects.create(
            user=request.user,
            query_text="INSERT INTO SecureRecord (...)",
            query_type=action,
            is_allowed_by_rbac=allowed,
            is_malicious_ml=False,
            final_decision="ALLOWED" if allowed else "BLOCKED"
        )

        if not allowed:
            return HttpResponseForbidden("INSERT not allowed")

        SecureRecord.objects.create(
            name=request.POST.get("name"),
            secret_data=request.POST.get("secret_data"),
            created_by=request.user
        )

        return redirect("records")

    # -----------------------------
    # HANDLE SELECT OPERATION
    # -----------------------------
    action = "SELECT"
    allowed = is_allowed(request.user, action)

    SQLQueryLog.objects.create(
        user=request.user,
        query_text="SELECT * FROM SecureRecord",
        query_type=action,
        is_allowed_by_rbac=allowed,
        is_malicious_ml=False,
        final_decision="ALLOWED" if allowed else "BLOCKED"
    )

    if not allowed:
        return HttpResponseForbidden("SELECT not allowed")

    records = SecureRecord.objects.all()

    return render(request, "records.html", {
        "records": records,
        "can_insert": is_allowed(request.user, "INSERT"),
        "can_delete": is_allowed(request.user, "DELETE"),
        "role": get_user_role(request.user)
    })


@login_required
def delete_record(request, record_id):

    action = "DELETE"
    allowed = is_allowed(request.user, action)

    SQLQueryLog.objects.create(
        user=request.user,
        query_text=f"DELETE FROM SecureRecord WHERE id={record_id}",
        query_type=action,
        is_allowed_by_rbac=allowed,
        is_malicious_ml=False,
        final_decision="ALLOWED" if allowed else "BLOCKED"
    )

    if not allowed:
        return HttpResponseForbidden("DELETE not allowed")

    SecureRecord.objects.filter(id=record_id).delete()

    return redirect("records")