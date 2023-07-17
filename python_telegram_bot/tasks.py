import subprocess

from python_telegram_bot.celery import app


@app.task
def run_management_command():
    try:

        subprocess.run(['google_sheets'], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")
