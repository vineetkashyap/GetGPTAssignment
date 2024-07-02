from app.celery_app import celery_app

celery_app.conf.update(
    task_routes={
        'app.tasks.fetch_and_process_data': {'queue': 'data_processing'},
    },
)

if __name__ == '__main__':
    celery_app.start()
