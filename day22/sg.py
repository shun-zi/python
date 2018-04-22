from django.db.models.signals import post_save
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='log/DB.log', level=logging.DEBUG, format=LOG_FORMAT)

def post_save_func(sender,**kwargs):
    log_inf = kwargs['instance'].db_name() + "创建了一条新纪录"
    logging.debug(log_inf)


post_save.connect(post_save_func)