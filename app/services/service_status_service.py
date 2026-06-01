from app.repositories.service_status_repository import (
    refresh_registration_service_statuses,
)


def sync_registration_service_statuses():
    refresh_registration_service_statuses()