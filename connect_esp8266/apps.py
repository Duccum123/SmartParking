from django.apps import AppConfig
import threading
# from modelAI.empty_space.emptySpace import camera_loop


class ConnectEsp8266Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'connect_esp8266'
    
    # def ready(self):
    #     # Khởi động thread chỉ 1 lần duy nhất
    #     if not hasattr(self, 'thread_started'):
    #         self.thread_started = True
    #         threading.Thread(target=camera_loop, daemon=True).start()