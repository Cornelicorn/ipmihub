
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .status_updates import updateAllHostStatus
from ipmihub.env import refresh_interval

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(updateAllHostStatus, 'interval', seconds=refresh_interval)
    scheduler.start()