from .models import SQLQueryLog, MLDetectionResult
from .ml_model import predict_query


def log_query(user, query_text, query_type, is_allowed):

    # ML Detection
    is_malicious, confidence = predict_query(query_text)

    # Final decision
    final_decision = "ALLOWED"
    if not is_allowed or is_malicious:
        final_decision = "BLOCKED"

    # Save log
    log = SQLQueryLog.objects.create(
        user=user,
        query_text=query_text,
        query_type=query_type,
        is_allowed_by_rbac=is_allowed,
        is_malicious_ml=is_malicious,
        final_decision=final_decision
    )

    # Save ML result
    MLDetectionResult.objects.create(
        query_log=log,
        prediction="MALICIOUS" if is_malicious else "BENIGN",
        confidence_score=confidence,
        model_version="RF_v1"
    )

    return is_malicious  # 🔥 important for blocking