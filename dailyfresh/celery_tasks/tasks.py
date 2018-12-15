from django.conf import settings
from celery import Celery
from django.core.mail import send_mail
import time
# from goods.models import *
from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django_redis import get_redis_connection
from django.template import loader

# 在任务处理者端加这几句  初始化
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()


app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')

@app.task
def send_register_active_email(to_email, username, token):
    print('send_register_active_email----->')
    subject = '天天生鲜欢迎信息'
    # message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击以下链接激活您的账户<br><a href="http://127.0.0.1:8888/user/active/%s">http://127.0.0.1:8888/user/active/%s</a>'%(username, token, token)
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击以下链接激活您的账户<br><a href="http://127.0.0.1:8888/user/active/%s">http://127.0.0.1:8888/user/active/%s</a>'%(username, token, token)
    #         标题　　　　　　内容　　　　　　发送者　　　　　　接受人　　　　html内容
    send_mail(subject, message, sender, receiver, html_message=html_message)

    time.sleep(5)

@app.task
def generate_static_index_html():

    types = GoodsType.objects.all()
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    for type in types:
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        type.image_banners = image_banners
        type.title_banners = title_banners

    context = {
        'types':types,
        'goods_banners':goods_banners,
        'promotion_banners':promotion_banners
    }

    temp = loader.get_template('static_index.html')

    static_index_html = temp.render(context)

    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')

    with open(save_path, 'w') as f:
        f.write(static_index_html)


