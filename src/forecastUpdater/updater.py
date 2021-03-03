from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.scheduler import Scheduler

from forecastUpdater import forecastApi
import logging

#Get an instance of a logger
logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()
    #sched = Scheduler()
    scheduler.add_job(forecastApi.getForecast, 'interval', minutes=5)
    scheduler.add_job(forecastApi.getForecadtData, 'cron', day_of_week='tue-wed', minute=5)
    #sched.add_cron_job(job_function, 'interval', minutes=5)

    logger.info("Crone job started")
    scheduler.start()