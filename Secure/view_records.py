from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import *
from .rbac import is_allowed, get_user_role
from .ml_model import predict_query
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib import messages
from django.shortcuts import redirect

@login_required
def records_page(request):

    # -----------------------------
    # HANDLE INSERT OPERATION
    # -----------------------------
    if request.method == "POST" and "add_record" in request.POST:

        action = "INSERT"
        allowed = is_allowed(request.user, action)
        name=request.POST.get("name"),
        secret_data=request.POST.get("secret_data"),
        query_text=f"INSERT INTO SecureRecord VALUES ({name}, {secret_data})"
        is_malicious, confidence = predict_query(query_text)
        print("checking malicious or not")
        print(is_malicious)
        print("confidence",confidence)

        # 🔥 Final Decision
        final_decision = "ALLOWED"
        if not is_allowed or is_malicious:
            final_decision = "BLOCKED"
        query_log=SQLQueryLog.objects.create(
            user=request.user,
           query_text=f"INSERT INTO SecureRecord VALUES ({name}, {secret_data})",
            query_type=action,
            is_allowed_by_rbac=allowed,
            is_malicious_ml=is_malicious,
            final_decision=final_decision
        )
        MLDetectionResult.objects.create(
            query_log=query_log,
           prediction = "MALICIOUS" if is_malicious else "BENIGN",
            confidence_score=confidence,
            model_version="v1.0"
        )
        if not allowed:
            messages.error(request, "⚠ INSERT operation is not allowed.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if is_malicious:
            messages.error(request, "🚫 Malicious input detected! Please check your input.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        

        

       
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
    "can_update": is_allowed(request.user, "UPDATE"),   # ✅ ADD THIS
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