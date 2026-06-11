from .models import AuditLog


def create_audit_log(
    user,
    action,
    module,
    description
):

    AuditLog.objects.create(
        user=user,
        action=action,
        module=module,
        description=description
    )