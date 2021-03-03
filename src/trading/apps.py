from django.apps import AppConfig


class TradingConfig(AppConfig):
    name = 'trading'

    def ready(self):
    	from forecastUpdater import updater
    	print("CALL CRONE JOBS")
    	updater.start()
