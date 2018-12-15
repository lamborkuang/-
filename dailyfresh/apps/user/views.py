from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import re
from order.models import *
from user.models import *
from goods.models import *
from django.core.urlresolvers import reverse
from django.views.generic import View 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from itsdangerous import SignatureExpired
from django.conf import settings
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate, login, logout 
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
from django.core.paginator import Paginator 

# Create your views here.

def register(request):
    if request.method == 'GET':

        return render(request, 'register.html')
    else:
        username = request.POST.get('user_name', None)
        password = request.POST.get('pwd', None)
        check_passwd = request.POST.get('cpwd', None)
        email = request.POST.get('email', None)
        allow = request.POST.get('allow', None)

        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg':'数据不完整'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg':'邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg':'请同意协议'})

        try:
            a = User.objects.get(username=username)
        except:
            a = None
        if a:
            return render(request, 'register.html', {'errmsg':'用户名已存在'})

        if check_passwd != password:
            return render(request, 'register.html', {'errmsg':'密码不一致'})

        user = User.objects.create_user(username, email, password)
        # 刚注册　未激活
        user.is_active = 0
        user.save()
        # 调转到首页index 在goods下面  
        return redirect(reverse('goods:index'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('user_name', None)
        password = request.POST.get('pwd', None)
        check_passwd = request.POST.get('cpwd', None)
        email = request.POST.get('email', None)
        allow = request.POST.get('allow', None)

        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg':'数据不完整'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg':'邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg':'请同意协议'})

        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user:
            return render(request, 'register.html', {'errmsg':'用户名已存在'})

        if check_passwd != password:
            return render(request, 'register.html', {'errmsg':'密码不一致'})

        user = User.objects.create_user(username, email, password)
        # 刚注册　未激活
        user.is_active = 0
        user.save()
        # 加密用户的身份信息，生成激活token   密钥　　　　　　　　　　过期时间
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()

        send_register_active_email.delay(email, username, token)

        # subject = '天天生鲜欢迎信息'
        # # message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击以下链接激活您的账户<br><a href="http://127.0.0.1:8888/user/active/%s">http://127.0.0.1:8888/user/active/%s</a>'%(username, token, token)
        # message = ''
        # sender = settings.EMAIL_FROM
        # receiver = [email]
        # html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击以下链接激活您的账户<br><a href="http://127.0.0.1:8888/user/active/%s">http://127.0.0.1:8888/user/active/%s</a>'%(username, token, token)
        # #         标题　　　　　　内容　　　　　　发送者　　　　　　接受人　　　　html内容
        # send_mail(subject, message, sender, receiver, html_message=html_message)
        
        # 调转到首页index 在goods下面  
        return redirect(reverse('goods:index'))


class ActiveView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse(e, '激活链接已过期')


class LoginView(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'login.html', {'username':username, 'checked':checked})

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg':'数据不完整'})

        user = authenticate(username=username, password=password)
        print('user--->', user)
        if user is not None:
            if user.is_active:
                # 记录用户登录状态
                login(request, user)
                # 这里是 GET
                next_url = request.GET.get('next', reverse('goods:index'))
                response = redirect(next_url)

                remember = request.POST.get('remember', None)
                if remember == 'on':
                    response.set_cookie('username', username, max_age=24*3600)
                else:
                    response.delete_cookie('username')

                return response
            else:
                return render(request, 'login.html', {'errmsg':'用户尚未激活'})
        else:
            return render(request, 'login.html', {'errmsg':'用户名或密码不正确'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('goods:index'))

# /user
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        address = Address.objects.get_default_address(user)

        con = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        # 最新浏览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4)

        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        context = {
            'page':'user', 
            'address':address,
            'goods_li':goods_li

        }
        return render(request, 'user_center_info.html', context)



# /user/order
class UserOrderView(LoginRequiredMixin, View):
    def get(self, request, page):
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        for order in orders:
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            for order_sku in order_skus:
                amount = order_sku.count * order_sku.price
                order_sku.amount = amount

            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            order.order_skus = order_skus

        paginator = Paginator(orders, 1)

        try:
            page = int(page)
        except Exception as e:
            page =1

        if page > paginator.num_pages:
            page = 1
        # 获取第page页的Page实例对象
        order_page = paginator.page(page)

        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        context = {'order_page':order_page,
                   'pages':pages,
                   'page': 'order'}

        return render(request, 'user_center_order.html', context)



# /user/address
class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None
        address = Address.objects.get_default_address(user)
        return render(request, 'user_center_site.html', {'page':'address', 'address':address})


    def post(self, request):
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg':'数据不完整'})

        if not re.match(r'^1[3|4|5|6|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg':'手机格式不正确'})

        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True
        Address.objects.create(user=user, receiver=receiver, addr=addr, zip_code=zip_code, phone=phone, is_default=is_default)
        return redirect(reverse('user:address'))


