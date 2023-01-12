from django.urls import path
from . import views

urlpatterns = [
    # Run Scheduled Jobs
    path('run', views.run_jobs, name='run_jobs'),
    path('aws/run', views.run_jobs_from_aws_health_check, name='run_jobs_aws'),

    # A sample/test job
    path('scheduled/test', views.test_job, name='test_job'),

    # Manage Schedules
    path('list', views.job_list, name='jobs'),
    path('save', views.save_job, name='save_job'),
    path('update', views.update_job, name='update_job'),
    path('delete/<int:job_id>', views.delete_job, name='delete_job'),
    path('toggle/<int:job_id>', views.toggle_job_status, name='toggle'),

    # Manage Jobs
    path('endpoint/list', views.endpoint_list, name='endpoints'),
    path('endpoint/save', views.save_endpoint, name='save_endpoint'),
    path('endpoint/update', views.update_endpoint, name='update_endpoint'),
    path('endpoint/delete', views.delete_endpoint, name='delete'),
    path('endpoint/delete/<int:endpoint_id>', views.delete_endpoint, name='delete_endpoint'),

    # View scheduled job executions
    path('endpoint/executions', views.executions, name='executions'),
]
