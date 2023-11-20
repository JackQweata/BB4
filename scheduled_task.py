from config import app

app.conf.beat_schedule = {
    'run-every-hour': {
        'task': 'tasks.run_parser',
        'schedule': 3600
    },
}

if __name__ == '__main__':
    app.start()
