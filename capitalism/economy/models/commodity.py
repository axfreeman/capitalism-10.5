from django.db import models
from .states import TimeStamp,State
from capitalism.global_constants import ORIGIN_CHOICES, USAGE_CHOICES, UNDEFINED

class Commodity(models.Model):
    time_stamp_FK = models.ForeignKey(TimeStamp, related_name='commodity', on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=25, default=UNDEFINED)
    origin = models.CharField(max_length=20,choices=ORIGIN_CHOICES,default=UNDEFINED)
    usage = models.CharField(verbose_name='Usage', max_length=25, choices=USAGE_CHOICES,default=UNDEFINED)
    size = models.FloatField(verbose_name="Quantity", default=0)
    total_value = models.FloatField(verbose_name="Total Price", default=0)
    total_price = models.FloatField(verbose_name="Total Value", default=0)
    unit_value = models.FloatField(verbose_name="Unit Value", default=1)
    unit_price = models.FloatField(verbose_name="Unit Price", default=1)
    turnover_time = models.FloatField(verbose_name="Turnover Time", default=360)
    demand = models.FloatField(verbose_name="Demand", default=0)
    supply = models.FloatField(verbose_name="Supply", default=0)
    allocation_ratio = models.FloatField(verbose_name="Allocation Ratio", default=1)
    display_order = models.IntegerField(null=True, default=1)
    image_name = models.CharField(max_length=25, default="###")
    tooltip = models.CharField(max_length=50, default="###")
    owner = models.ForeignKey('auth.User', related_name='commodities', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Commodity'
        verbose_name_plural = 'Commodities'
        ordering = ['time_stamp_FK']

    def time_stamped_queryset():
        current_state=State.objects.get()
        qs=Commodity.objects.filter(time_stamp_FK=current_state.time_stamp_FK)
        return qs

    def __str__(self):
        return f"[Project {self.time_stamp_FK.project_FK.number}] {self.name}"
