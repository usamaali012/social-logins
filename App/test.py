import time
from datetime import datetime

ts = time.time()
print(int(ts))

dt_object = datetime.fromtimestamp(time.time())
print(dt_object)

sub = '106368296827960270379'

"""    <div><fb:login-button scope="public_profile,email" onlogin="checkLoginState();">
    </fb:login-button></div> """