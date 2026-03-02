from .models import SQLQueryLog


def log_query(user, query_text, query_type, is_allowed, is_malicious=False):
    """
    Logs every database-related action.
    """

    final_decision = "ALLOWED" if is_allowed and not is_malicious else "BLOCKED"

    SQLQueryLog.objects.create(
        user=user,
        query_text=query_text,
        query_type=query_type,
        is_allowed_by_rbac=is_allowed,
        is_malicious_ml=is_malicious,
        final_decision=final_decision
    )