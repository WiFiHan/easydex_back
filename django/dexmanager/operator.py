from apscheduler.schedulers.background import BackgroundScheduler
from .views import DexListView, DexDetailView
from .models import SrcDex
import signal

def start():
    scheduler=BackgroundScheduler(job_defaults={'max_instances': 2})

    @scheduler.scheduled_job('cron', hour='1', name = 'refresh_dexes', misfire_grace_time=60)
    def refresh_dexes():
        DexListView.post(DexListView, None)

    @scheduler.scheduled_job('cron', hour='23', name = 'refresh_dex_value', misfire_grace_time=60)
    def refresh_dex_value():
        id_array = SrcDex.objects.values_list('id', flat=True)
        for idx in id_array:
            DexDetailView.post(DexDetailView, None, idx)

    scheduler.start()

    def gracefully_exit(signum, frame):
        print('Stopping...')
        scheduler.shutdown()

    signal.signal(signal.SIGINT, gracefully_exit)   
    signal.signal(signal.SIGTERM, gracefully_exit)