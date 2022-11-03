import logging
import datetime

handler = logging.FileHandler('./logs/{}.log'.format(str(datetime.datetime.now()).replace(' ', '_').replace(':', 'h', 1).replace(':', 'm').split('.')[0][:-2]), encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s::%(levelname)s::%(name)s::%(message)s'))
logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(handler)
