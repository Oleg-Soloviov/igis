import re
import random
import json
from datetime import datetime
from urllib import parse
import requests
import logging
from lxml import html
from requests.exceptions import Timeout
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, FormView, View
from .forms import *
from .models import Place, Hospital
from .utils import get_sign_items


timeout = settings.MY_REQUESTS_CONNECT_TIMEOUT, settings.MY_REQUESTS_READ_TIMEOUT
logger = logging.getLogger('django')


class PlaceListView(TemplateView):
    template_name = 'igis_udm/place_list.html'

    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data(**kwargs)
        places_list = Place.objects.all()
        paginator = Paginator(places_list, 10)
        context['page_obj_1'] = paginator.page(1)
        context['page_obj_2'] = paginator.page(2)
        context['page_obj_3'] = paginator.page(3)
        context['debug'] = settings.DEBUG
        return context


class PlaceDetailView(DetailView):
    template_name = 'igis_udm/place_detail.html'
    model = Place

    def get_context_data(self, **kwargs):

        # освободить авторизацию при выходе из больницы
        if self.request.session.get('igis_obj_id', False):
            medical_cookie = 'medical__{}'.format(self.request.session['igis_obj_id'])
            cookies = self.request.session.get('igis_cookies', False)
            if cookies and (self.request.session['igis_cookies'].get(medical_cookie, '+') != '+'):
                params = {'exit': '1', 'obj': self.request.session['igis_obj_id']}
                r = requests.get('http://igis.ru/online', params=params, cookies=cookies)
                self.request.session.flush()

        context = super(PlaceDetailView, self).get_context_data(**kwargs)
        place_list = Place.objects.all()
        context['place_list'] = place_list
        context['debug'] = settings.DEBUG
        return context


class HospitalDetailView(DetailView):
    template_name = 'igis_udm/hospital_detail.html'
    model = Hospital

    def get_context_data(self, **kwargs):
        context = super(HospitalDetailView, self).get_context_data(**kwargs)
        self.request.session['igis_obj_id'] = self.object.igis_obj
        persons = []
        context['login_form'] = LoginForm()
        context['place_list'] = Place.objects.all()
        context['debug'] = settings.DEBUG
        context['failure'] = False
        context['error'] = False

        my_user = self.request.session.get('my_user', False)
        if my_user:
            my_user = json.loads(parse.unquote(my_user))
        context['my_user'] = my_user

        url = 'http://igis.ru/online?obj={}&page=rasp'.format(self.object.igis_obj)
        r_session = self.request.session.get('r_session', False)

        cached = cache.get(str(self.object.igis_obj), False)
        if cached:
            context['sign_items'] = cached['sign_items']
            context['persons'] = cached['persons']
            logger.debug('get cache')
        else:
            logger.debug('without cache')
            # если существует, то берем уже готовую requests.session, если нет, то создаем новую
            if not r_session:
                r_session = requests.Session()
            try:
                r = r_session.get(url, timeout=timeout)
            except Timeout:
                context['error'] = True
                print('93', '-------', 'timeout error')
            except Exception as e:
                context['error'] = True
                print(e)
            else:
                cached = {}
                sign_items = self.request.session.get('sign_items', [])
                context['sign_items'] = sign_items
                cached['sign_items'] = sign_items
                doc = html.document_fromstring(r.text)
                rows = doc.xpath('//table[@id="medlist"]/tr')
                for row in rows:
                    if row.xpath('contains(@class, "table-border-light")'):
                        speciality = row.text_content()
                        continue
                    elif row.xpath('./td[@colspan= "7"]'):
                        item = dict()
                        item['speciality'] = speciality
                        item['fio'] = row.xpath('./td/div/div/a[1]')[0].text_content()
                        foo = row.xpath('./td/div/div/a[1]/@href')[0]
                        m = re.search(r'id=([\d]+)', foo)
                        item['person_id'] = m.group(1)
                        if row.xpath('./td/div/small'):
                            # item['info'] = row.xpath('./td/div/small')[0].text_content()
                            foo = row.xpath('./td/div/small/text()')
                            item['info'] = []
                            item['uch'] = False
                            for txt in foo:
                                if 'Участки:' in txt:
                                    m = re.search(r'Участки:[\s]+([\d,\s]+);', txt)
                                    if m:
                                        item['uch'] = m.group(1)
                                if 'Ограничение на запись через ИГИС:' in txt:
                                    m = re.search(r'Ограничение на запись через ИГИС:(.*)', txt)
                                    if 'Ограничений нет' in m.group(1):
                                        continue
                                    elif 'Ограничение на запись через ИГИС: нет' in txt:
                                        continue
                                    else:
                                        item['info'].append(m.group(1))
                                else:
                                    item['info'].append(txt)

                        else:
                            item['info'] = ''
                        foo = row.text_content()
                        if 'Номерков нет' in foo:
                            item['col_n'] = ''
                        else:
                            m = re.search(r'Номерков - ([\d]+)', foo)
                            if m:
                                item['col_n'] = m.group(1)  # количество номерков
                            else:
                                item['col_n'] = ''
                        persons.append(item)
                context['persons'] = persons
                cached['persons'] = persons
                cache.set(str(self.object.igis_obj), cached, 60*60*3)

            self.request.session['r_session'] = r_session

        return context


class HospitalLoginFormView(FormView):
    form_class = LoginForm
    template_name = 'igis_udm/hospital_detail.html'

    def form_valid(self, form):
        data = {}
        data['person_id'] = ''
        data['status'] = ''
        data['failure'] = ''

        medical_cookie = 'medical__{}'.format(self.request.session['igis_obj_id'])
        params = {'login': '1',
                  'obj': self.request.session['igis_obj_id'],
                  'f': parse.quote(form.cleaned_data['name']),
                  'p': form.cleaned_data['polis'],
                  'rnd': str(random.randint(1000, 100000))}
        url = 'http://igis.ru/com/online/login.php'
        r_session = self.request.session.get('r_session', False)
        if not r_session:
            r_session = requests.Session()
        try:
            r = r_session.get(url, params=params, timeout=timeout)
        except Timeout:
            data['status'] = 'error'
            data['failure'] = 'Сервер больницы не ответил. Попробуйте еще раз.'
            print('182 --------')
        except Exception as e:
            data['status'] = 'error'
            data['failure'] = 'Ошибка обращения к серверу больницы.'
            print(e)
        else:
            self.request.session['r_session'] = r_session
            doc = html.document_fromstring(r.text)
            if r_session.cookies.get(medical_cookie, '+') == '+':
                self.request.session['my_user'] = False
                data['status'] = 'error'
                mistake = doc.xpath('//font[@color="red"]')
                print('200', '--------------')
                if mistake:
                    mistake_text = mistake[0].text_content()
                    print('203', mistake_text)
                    if 'Нет ответа от больницы, пробуем подключиться еще' in mistake_text:
                        data['failure'] = 'Нет ответа от больницы, попробуйте еще раз.'
                    else:
                        data['failure'] = mistake_text
                else:
                    data['failure'] = 'Авторизация в больнице не удалась. Попробуйте еще раз.'
                    print('210', '343434343434')
            else:
                if 'вы успешно авторизованы' in r.text:
                    print('213', '-------------')
                    # перейдем на страницу больницы, чтобы получить данные о записях пациента
                    data['status'] = 'authorized'
                    data['info'] = r_session.cookies.get(medical_cookie, 'Unknown error')

                    my_user = r_session.cookies.get(medical_cookie)
                    # my_user = json.loads(parse.unquote(my_user))
                    self.request.session['my_user'] = my_user

                    self.request.session['my_user'] = r_session.cookies.get(medical_cookie, False)
                    url = 'http://igis.ru/online'
                    params = {'obj': self.request.session['igis_obj_id']}
                    try:
                        r = r_session.get(url, params=params, timeout=timeout)
                    except Timeout:
                        data['error'] = 'failed_signs'
                        data['failure'] = 'Не удалось получить данные о ваших записях к врачу.'
                        print('230', '676767676767')
                    except Exception as e:
                        data['error'] = 'failed_signs'
                        data['failure'] = 'Не удалось получить данные о ваших записях к врачу.'
                        print('234', e)
                    else:
                        print('236', '-------------')
                        self.request.session['r_session'] = r_session
                        doc = html.document_fromstring(r.text)
                        # получим все данные о записях пациента
                        sign_items = doc.xpath('//*[contains(text(), "Отменить запись")]/..')
                        if sign_items:
                            data['sign_items'] = get_sign_items(sign_items)
                            self.request.session['sign_items'] = data['sign_items']
                        print('274', '----------------')
                else:
                    # for debug, if there something else, maybe not actual
                    data['status'] = 'error'
                    data['failure'] = 'Неизвестная ошибка. Попробуйте еще раз.'
                    print('279', '---------------')
        finally:
            return JsonResponse(data, status=200, safe=False)


class HospitalLogOutFormView(View):
    def dispatch(self, request, *args, **kwargs):
        data = {}
        data['status'] = ''
        data['failure'] = ''

        params = {'exit': '1', 'obj': self.request.session['igis_obj_id']}

        r_session = self.request.session.get('r_session', False)
        if not r_session:
            r_session = requests.Session()
        r = r_session.get('http://igis.ru/online', params=params)
        self.request.session['r_session'] = r_session
        if r.ok:
            data['status'] = 'logout'
            if 'sign_items' in self.request.session:
                del self.request.session['sign_items']
            del self.request.session['my_user']
            return JsonResponse(data, status=200, safe=False)
        else:
            data['status'] = 'error'
            data['failure'] = 'Unknown error, try again'
            return JsonResponse(data, status=200, safe=False)


class HospitalGetPersonTime(View):
    form_class = TimePersonForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        data = {}
        data['dates_of_sign'] = {}
        data['person_id'] = ''
        data['status'] = ''
        data['failure'] = ''

        if form.is_valid():
            url = 'http://igis.ru/online?obj={}&page=doc&id={}'.format(self.request.session['igis_obj_id'], form.cleaned_data['id'])
            try:
                r = requests.get(url, timeout=timeout)
            except Timeout:
                data['status'] = 'error'
                data['failure'] = 'Сервер больницы не отвечает. Попробуйте еще раз.'
            else:
                doc = html.document_fromstring(r.text)
                if doc.xpath('//h2[contains(text(), "Список доступных номерков")]/../following-sibling::div//*[contains(text(), "К выбранному специалисту свободных номерков нет")]'):
                    data['status'] = 'nomerkov_net'
                    data['failure'] = 'Номерков нет'
                else:
                    divs = doc.xpath('//h2[contains(text(), "Список доступных номерков")]/../following-sibling::div[@style="padding:10px 0;" and a[@class="btn green" and not(@title)]]')
                    data['person_id'] = form.cleaned_data['id']
                    for div in divs:
                        time_links = div.xpath('a[@class="btn green"]')
                        sign_date = div.xpath('h2')[0].text_content()
                        m = re.search(r'[\d]{2}.[\d]{2}.[\d]{4}', sign_date)
                        foo_date = m.group(0)
                        foo_date = datetime.strptime(foo_date, '%d.%m.%Y')
                        foo_date = foo_date.strftime('%s')
                        data['dates_of_sign'][foo_date] = []
                        for link in time_links:
                            if 'Время%20для%20записи%20прошло' in link.xpath('@href')[0]:
                                data['dates_of_sign'][foo_date].append((link.text_content(), 'false'))
                            else:
                                data['dates_of_sign'][foo_date].append((link.text_content(), 'true'))

            return JsonResponse(data, status=200, safe=False)
        else:
            data = form.errors.as_json()
            return HttpResponse(data, content_type='application/json')


class SignInFormView(FormView):
    form_class = SignInForm
    template_name = 'igis_udm/empty_template.html'

    def form_valid(self, form):
        data = {}
        url = 'http://igis.ru/com/online/zapis.php'
        params = {'zapis': '1',
                  'obj': self.request.session['igis_obj_id'],
                  'kw': parse.quote(form.cleaned_data['specialist_id']),
                  'd': form.cleaned_data['date'],
                  't': form.cleaned_data['time'],
                  'rnd': str(random.randint(1000, 100000))}

        r_session = self.request.session.get('r_session', False)
        if not r_session:
            r_session = requests.Session()
            print('aaaaaaaaaaaaa')
        try:
            r = r_session.get(url, params=params, timeout=timeout)
            print('bbbbbbbbbbbbbbb')
        except Timeout:
            data['status'] = 'error'
            data['failure'] = 'Сервер больницы не отвечает. Попробуйте еще раз.'
            print('ccccccccccccc')
            return JsonResponse(data, status=200, safe=False)

        self.request.session['r_session'] = r_session
        if self.request.session.get('my_user', False):
            data['info'] = self.request.session.get('my_user', False)
            print('dddddddddd')
        else:
            data['status'] = 'logout'
            print('eeeeeeeeeeeeeeeee')
            return JsonResponse(data, status=200, safe=False)

        if r.ok and ("Вы успешно записаны на прием" in r.text):
            print('4444444444444444444')
            url = 'http://igis.ru/online/'
            params = {'obj': self.request.session['igis_obj_id']}
            r = r_session.get(url, params=params, timeout=timeout)
            self.request.session['r_session'] = r_session
            doc = html.document_fromstring(r.text)
            sign_items = doc.xpath('//*[contains(text(), "Отменить запись")]/..')
            print('raw_items -- ', sign_items)
            data['sign_items'] = []
            if sign_items:
                data['status'] = 'sign'
                data['sign_items'] = get_sign_items(sign_items)
                self.request.session['sign_items'] = data['sign_items']
                print('readdy items -- ', data['sign_items'])
            print('555555555555555555')
            return JsonResponse(data, status=200, safe=False)
        elif r.ok and ("ожидайте ответа больницы" in r.text):
            data['status'] = 'error'
            data['failure'] = 'Сервер больницы не отвечает.'
            print('6666666666666666666')
            return JsonResponse(data, status=200, safe=False)
        elif r.ok and ("Выбранного номерка не существует" in r.text):
            data['status'] = 'error'
            data['failure'] = 'Номерок уже занят, обновите страницу.'
            print('77777777776666666666')
            return JsonResponse(data, status=200, safe=False)
        else:
            data['status'] = 'error'
            data['failure'] = 'Сервер больницы не отвечает.'
            print('signin errorr -- ', r.text)
            print('ffffffffffffffffff')
            return JsonResponse(data, status=200, safe=False)

    def form_invalid(self, form):
        data = {}
        data['status'] = 'error'
        print('ggggggggggggggggg')
        return JsonResponse(data, status=200, safe=False)


class SignOutFormView(FormView):
    form_class = SignOutForm
    template_name = 'igis_udm/empty_template.html'

    def form_valid(self, form):
        data = {}
        url = 'http://igis.ru/com/online/delete.php'
        params = {'delete': '1',
                  'obj': self.request.session['igis_obj_id'],
                  'kw': form.cleaned_data['specialist_id'],
                  'd': form.cleaned_data['date'],
                  't': form.cleaned_data['time'],
                  'rnd': str(random.randint(1000, 100000))}

        r_session = self.request.session.get('r_session', False)
        if not r_session:
            r_session = requests.Session()
        r = r_session.get(url, params=params, timeout=timeout)
        self.request.session['r_session'] = r_session

        if r.ok and ('Ваша запись успешно отменена' in r.text):
            data['status'] = 'signout'
            url = 'http://igis.ru/online'
            params = {'obj': self.request.session['igis_obj_id']}
            r = r_session.get(url, params=params, timeout=timeout)
            self.request.session['r_session'] = r_session

            doc = html.document_fromstring(r.text)
            sign_items = doc.xpath('//*[contains(text(), "Отменить запись")]/..')
            data['sign_items'] = []
            if sign_items:
                data['sign_items'] = get_sign_items(sign_items)
            self.request.session['sign_items'] = data['sign_items']

            return JsonResponse(data, status=200, safe=False)
        else:
            data['status'] = 'error'
            data['failure'] = r.text
            return JsonResponse(data, status=200, safe=False)

    def form_invalid(self, form):
        data = {}
        data['status'] = 'error'
        return JsonResponse(data, status=200, safe=False)


class ContactView(FormView):
    template_name = 'igis_udm/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts_success')

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'igis_udm/contact_success.html'