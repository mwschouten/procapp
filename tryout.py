import logging

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)15s - %(levelname)s - %(message)s')
logger = logging.getLogger('Test')
formatter = logging.Formatter()

from tasks.experts.tasks import *

a1 = Add(a=2,b=3)
a2 = Add(a=1,b=1)

b = Add2(a=a1.result,b=a2.result)
