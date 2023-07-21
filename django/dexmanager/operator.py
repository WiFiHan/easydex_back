from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .views import DexListView, DexDetailView
from datetime import datetime

def start():
    scheduler=BackgroundScheduler(job_defaults={'max_instances': 2})
    # scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    # register_events(scheduler)

    # @scheduler.scheduled_job('cron', hour=23, name = 'refresh_dexes')
    @scheduler.scheduled_job('cron', second='*/15', name = 'refresh_dexes')
    def refresh_dexes():
        # print("refresh...")
        DexListView.post(DexListView, None)

    # @scheduler.scheduled_job('cron', minute='*/1', name = 'refresh_dex_value')
    # def refresh_dex_value():
        # print("refresh...{}".format(datetime.now()))
        # DexListView.post(DexListView, None)

    scheduler.start()

# import logging
# from django.conf import settings
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import register_events, DjangoJobStore
# from apscheduler.triggers.cron import CronTrigger
# from .views import DexListView, DexDetailView

# logger = logging.getLogger(__name__)

# def start():
#   def handle(self, *args, **options):
#     scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE) # BlockingScheduler를 사용할 수도 있습니다.
#     scheduler.add_jobstore(DjangoJobStore(), "default") 

#     scheduler.add_job(
#         DexListView.post(None),
#         trigger=CronTrigger(second="*/60"),  # 60초마다 작동합니다.
#         id="refresh_all",  # id는 고유해야합니다. 
#         max_instances=1,
#         replace_existing=True,
#     )
#     logger.info("Added job 'my_job_a'.")

#     scheduler.add_job(
#         DexDetailView.post(None, 31),
#         trigger=CronTrigger(
#         day_of_week="mon", hour="03", minute="00"
#         ),  # 실행 시간입니다. 여기선 매주 월요일 3시에 실행합니다.
#         id="refresh_values",
#         max_instances=1,
#         replace_existing=True,
#     )
#     logger.info("Added job 'my_job_b'.")

#     try:
#         logger.info("Starting scheduler...")
#         scheduler.start() # 없으면 동작하지 않습니다.
#     except KeyboardInterrupt:
#         logger.info("Stopping scheduler...")
#         scheduler.shutdown()
#         logger.info("Scheduler shut down successfully!")