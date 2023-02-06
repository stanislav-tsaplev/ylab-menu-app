from celery import shared_task

from .catalog import generate_xls_file

generate_xls_file_task = shared_task(name="catalog.generate_xls_file", acks_late=True)(
    generate_xls_file
)
