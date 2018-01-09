from django.db import models
from django.db.models import Sum, F

from django.db.models import Sum
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone

class Discount(models.Model):
    name = models.CharField(max_length=128)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.end_time < now:
            raise RuntimeError('End_time in the past')
        super(Discount, self).save(*args, **kwargs)
        if self.start_time > now:
            activate_discount.apply_async((self.id), eta=self.start_time)
        delete_scount.apply_async((self.id), eta=self.end_time)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=128)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    full_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def set_full_discount(self, is_recursive=True):
        all_ancestors = self.get_ancestors(include_self=True).filter(discount__is_active=True)
        full_discount = all_ancestors.aggregate(Sum('discount__discount'))
        if full_discount['discount__discount__sum']:
            self.full_discount = full_discount['discount__discount__sum']
        if is_recursive:
            all_desendants = self.get_descendants()
            for item in all_desendants:
                item.set_full_discount(is_recursive=False)
                item.save()

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        self.set_full_discount()

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.ForeignKey(Discount, null=True)

    def __str__(self):
        return self.name

# @app.task
# def activate_discount(discount_id):
#     item = Discount.objects.get(discount_id)
#     item.is_active = True
#     item.save()

# @app.task
# def delete_discount(discount_id):
#     item = Discount.objects.get(discount_id)
#     categories = item.category_set.all()
#     for category in categories:


Product.objects.annotate(real_price=F('price') - \
                                    F('discount__discount') - \
                                    (F('category__full_discount'))).filter(real_price__gt=1000,
                                                                              real_price__lt=10000).order_by('real_price')
