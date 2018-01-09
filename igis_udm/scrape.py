import os
import sys
import json
from datetime import datetime, date
from urllib import parse
from transliterate import translit

sys.path.append('/home/oleg/PycharmProjects/igis/myproject')
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

import django
django.setup()

from django.utils.text import slugify
from igis_udm.models import Place, Hospital, Person, Speciality, DayofWeek, FreeDay
from scrapy_igis.scrapy_igis.settings import logger

def load_hospitals_in_db():
    counter = 0

    for line in open('../igis_udm.jl'):
        item = json.loads(line)
        place_obj = Place.objects.get(igis_url=item['place_url'])
        img_url = item.get('image_urls', [''])
        img_url = img_url[0]
        img_path = os.path.join('igis_udm', item['images'][0].get('path', ''))
        h = Hospital(
            name=item.get('hospital_name', ''),
            igis_name=item.get('hospital_name', ''),
            igis_url=item.get('url', ''),
            place=place_obj,
            phone=item.get('phone', ''),
            slug=item.get('slug', ''),
            address=item.get('hospital_address', ''),
            site_url=item.get('site_address', ''),
            x_coord=item.get('x_coord', ''),
            y_coord=item.get('y_coord', ''),
            image=img_path,
            igis_image_url=img_url
        )
        h.save()
        counter += 1
    print('Закончено - ', counter)


def load_izh_hospitals_in_db():
    counter = 0

    for line in open('../iz.jl'):
        item = json.loads(line)
        place_obj = Place.objects.get(name='Ижевск')
        img_url = item.get('image_urls', [''])
        img_url = img_url[0]
        img_path = os.path.join('igis_udm', item['images'][0].get('path', ''))
        h = Hospital(
            name=item.get('hospital_name', ''),
            igis_name=item.get('hospital_name', ''),
            igis_url=item.get('url', ''),
            place=place_obj,
            phone=item.get('phone', ''),
            slug=item.get('slug', ''),
            address=item.get('hospital_address', ''),
            site_url=item.get('site_address', ''),
            x_coord=item.get('x_coord', ''),
            y_coord=item.get('y_coord', ''),
            image=img_path,
            igis_image_url=img_url
        )
        h.save()
        counter += 1
    print('Закончено - ', counter)


def load_persons_in_db():
    counter = 0
    logger.debug('Start laoding items')
    date_now = datetime.now()

    for line in open('person_igis1.jl'):
        item = json.loads(line)

        igis_url = item['igis_url']
        u = parse.urlparse(igis_url)
        q = parse.parse_qs(u.query)
        obj = q['obj']
        obj = int(obj[0])
        if obj == 999 or obj == 998:
            continue
        hospital = Hospital.objects.get(igis_obj=obj)

        spec_name = item.get('speciality', ['unknown'])
        if spec_name == 'Акуш-гин':
            spec_name = 'Акушер-гинеколог'
        logger.debug('Speciality: {0}'.format(spec_name))
        spec_slug = slugify(translit(spec_name, 'ru', reversed=True))
        spec, is_new = Speciality.objects.get_or_create(slug=spec_slug)
        if not spec.name:
            spec.name = spec_name
            spec.save()

        weekends = item.get('weekends', '')
        w_days = []
        if weekends:
            logger.debug('Weekends: {0}'.format(weekends))
            weekends = weekends.rstrip(';')
            weekends = weekends.split(';')
            w_days = DayofWeek.objects.filter(name__in=weekends)
            logger.debug('Weekends db: {0}'.format(w_days))

        update_date = item.get('update_date', '')
        if update_date:
            try:
                update_date = datetime.strptime(update_date, '%d.%m.%Y %H:%M')
            except Exception:
                update_date = ''

        free_days = item.get('not_working_days', '')
        db_free_days = []
        if free_days:
            logger.debug('Free days: {0}'.format(free_days))
            try:
                free_days = [x.lstrip('Не рабочий день: ') for x in free_days]
                free_days = [datetime.strptime(x, '%d.%m.%Y') for x in free_days]
                free_days = [date.fromordinal(x.toordinal()) for x in free_days if x > date_now]
                for d in free_days:
                    new_day, is_new_day = FreeDay.objects.get_or_create(date=d)
                    db_free_days.append(new_day)
                logger.debug('Db_free_days: {0}'.format(db_free_days))
            except Exception as e:
                logger.error('Db_free_days error: {0}'.format(e))
                db_free_days = False

        h = Person(
            igis_fio=item.get('fio', ''),
            igis_url=item.get('igis_url', ''),
            igis_person_id=item.get('igis_person_id', ''),
            igis_update_date = update_date,
            family=item.get('fio', ''),
            speciality=spec,
            hospital=hospital,
            room=item.get('room', ''),
            time_limit=item.get('time_limit', ''),
            kod=item.get('kod', ''),
            sector=item.get('sector', ''),
            time_filter=item.get('time_filter', ''),
            unit=item.get('unit', ''),
            info=item.get('info', ''),
        )
        h.save()
        if db_free_days:
            h.free_days = db_free_days
        h.weekends = w_days
        h.save()
        counter += 1
    print('Закончено - ', counter)

if __name__ == '__main__':
    load_persons_in_db()
