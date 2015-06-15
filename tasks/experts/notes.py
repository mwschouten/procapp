

# sett things to work well in ipython
export DJANGO_SETTINGS_MODULE="proc.settings"

# load an example groupresult
from tasks.experts.tools.hbobject import HbObject
obj = HbObject({'hash': 'd0f7b7149bc25933ef5e09ff5978a541', 'type': 'data'})
gr = obj.content

# load an example groupresult
obj2 = HbObject(hash="b2d3f217fae95843303fd6092a93b784")
ar = obj2.content

