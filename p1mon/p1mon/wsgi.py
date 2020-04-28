import os 
import time 
import traceback 
import signal 
import sys 
 
from django.core.wsgi import get_wsgi_application 
 
sys.path.append('/home/pi/p1mon') 
# adjust the Python version in the line below as needed 
# sys.path.append('/home/pi/ipcamera/env_ipcamera/lib/python3.5/site-packages/') 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "p1mon.settings") 
 
try: 
    application = get_wsgi_application() 
except Exception: 
    # Error loading applications 
    if 'mod_wsgi' in sys.modules: 
        traceback.print_exc() 
        os.kill(os.getpid(), signal.SIGINT) 
        time.sleep(2.5) 