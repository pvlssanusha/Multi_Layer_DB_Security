from django.shortcuts import render


from django.http import HttpResponse

from django.shortcuts import render
from django.db.models import Count
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .rbac import *
from .ml_model import predict_query
@login_required
def dashboard(request):

    role = get_user_role(request.user)

    # -----------------------------
    # FILTER BASED ON ROLE
    # -----------------------------
    if role == "Admin":
        logs = SQLQueryLog.objects.all()

    elif role == "Analyst":
        logs = SQLQueryLog.objects.all()  # or limited view

    else:  # User
        logs = SQLQueryLog.objects.filter(user=request.user)

    # -----------------------------
    # ANALYTICS
    # -----------------------------
    total_queries = logs.count()

    allowed_queries = logs.filter(final_decision="ALLOWED").count()

    blocked_queries = logs.filter(final_decision="BLOCKED").count()

    malicious_queries = logs.filter(is_malicious_ml=True).count()

    query_types = logs.values('query_type').annotate(
        count=Count('query_type')
    )

    context = {
        "role": role,
        "total": total_queries,
        "allowed": allowed_queries,
        "blocked": blocked_queries,
        "malicious": malicious_queries,
        "query_types": query_types
    }

    return render(request, "dashboard.html", context)

@login_required
def edit_record(request, record_id):

    record = SecureRecord.objects.get(id=record_id)

    # -----------------------------
    # UPDATE PERMISSION CHECK
    # -----------------------------
    action = "UPDATE"
    allowed = is_allowed(request.user, action)

    if not allowed:
        messages.error(request, "⚠ UPDATE not allowed.")
        return redirect("records")

    # -----------------------------
    # HANDLE UPDATE POST
    # -----------------------------
    if request.method == "POST":

        name = request.POST.get("name")
        secret_data = request.POST.get("secret_data")

        query_text = f"UPDATE SecureRecord SET name={name}, secret_data={secret_data} WHERE id={record_id}"

        # ML check
        is_malicious, confidence = predict_query(query_text)

        final_decision = "ALLOWED"
        if not allowed or is_malicious:
            final_decision = "BLOCKED"

        # LOG QUERY
        query_log = SQLQueryLog.objects.create(
            user=request.user,
            query_text=query_text,
            query_type="UPDATE",
            is_allowed_by_rbac=allowed,
            is_malicious_ml=is_malicious,
            final_decision=final_decision
        )

        MLDetectionResult.objects.create(
            query_log=query_log,
            prediction="MALICIOUS" if is_malicious else "BENIGN",
            confidence_score=confidence,
            model_version="v1.0"
        )

        # BLOCK CONDITIONS
        if is_malicious:
            messages.error(request, "🚫 Malicious input detected!")
            return redirect("records")

        # PERFORM UPDATE
        record.name = name
        record.secret_data = secret_data
        record.save()

        return redirect("records")

    return render(request, "edit_record.html", {"record": record})
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def hii(request):
     return HttpResponse("Hello, ajay")


