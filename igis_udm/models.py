from django.db import models
from django.urls import reverse_lazy


class SEOitems(models.Model):
    head_title = models.CharField(max_length=255, unique=True)
    head_description = models.CharField(max_length=255, unique=True)
    head_keywords = models.CharField(max_length=255, unique=True)


class Place(models.Model):
    name = models.CharField('название', max_length=255, unique=True)
    igis_name = models.CharField(max_length=255, null=True, blank=True)
    seo = models.ForeignKey(SEOitems, on_delete=models.PROTECT, null=True, blank=True)
    igis_url = models.URLField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse_lazy('place', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']
        app_label = 'igis_udm'

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField('название', max_length=255, unique=True)
    igis_name = models.CharField(max_length=255, null=True, blank=True)
    seo = models.ForeignKey(SEOitems, on_delete=models.PROTECT, null=True, blank=True)
    igis_url = models.URLField(max_length=255, null=True, blank=True, unique=True)
    igis_obj = models.SmallIntegerField(unique=True)
    place = models.ForeignKey(Place, verbose_name='населенный пункт', on_delete=models.CASCADE)
    phone = models.CharField('телефон', max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255)
    address = models.CharField('адрес', max_length=255, null=True, blank=True)
    site_url = models.URLField(max_length=255, null=True, blank=True)
    x_coord = models.CharField(max_length=24, null=True, blank=True)
    y_coord = models.CharField(max_length=24, null=True, blank=True)
    image = models.ImageField(upload_to='igis_udm/full',
                              height_field='image_height',
                              width_field='image_width',
                              max_length=256,
                              blank=True,
                              null=True)
    igis_image_url = models.CharField(max_length=255, null=True, blank=True)
    image_width = models.SmallIntegerField(blank=True, null=True)
    image_height = models.SmallIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy('hospital', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']
        verbose_name = 'мед учереждение'
        verbose_name_plural = 'мед учереждения'
        app_label = 'igis_udm'

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField('название', max_length=255, unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse_lazy('speciality', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']
        app_label = 'igis_udm'

    def __str__(self):
        return self.name


class DayofWeek(models.Model):
    WEEK_DAYS = (
        ('Пн', 'Понедельник'),
        ('Вт', 'Вторник'),
        ('Ср', 'Среда'),
        ('Чт', 'Четверг'),
        ('Пт', 'Пятница'),
        ('Сб', 'Суббота'),
        ('Вс', 'Воскресенье'),
    )

    name = models.CharField('день недели',
                            max_length=2,
                            unique=True,
                            choices=WEEK_DAYS)

    class Meta:
        app_label = 'igis_udm'

    def __str__(self):
        return self.get_name_display()


class FreeDay(models.Model):
    date = models.DateField()

    class Meta:
        app_label = 'igis_udm'

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')


class Person(models.Model):
    igis_fio = models.CharField(max_length=255)
    igis_url = models.URLField(max_length=255)
    igis_person_id = models.CharField(max_length=255, blank=True, null=True)
    igis_update_date = models.DateTimeField(blank=True, null=True)
    family = models.CharField(max_length=255, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True)
    speciality = models.ForeignKey(Speciality, on_delete=None, blank=True, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=None)
    room = models.CharField(max_length=255, blank=True, null=True)
    time_limit = models.CharField(max_length=255, blank=True, null=True)
    kod = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=512, blank=True, null=True)
    time_filter = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)
    free_days = models.ManyToManyField(FreeDay, verbose_name='нерабочие дни', blank=True)
    weekends = models.ManyToManyField(DayofWeek, verbose_name='выходные', blank=True)

    def __str__(self):
        return self.family
