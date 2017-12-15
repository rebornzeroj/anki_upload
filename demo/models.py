from django.db import models
from django.contrib.auth.models import User, Group
import datetime
# Create your models here.

class Stats(models.Model):
    user = models.ForeignKey(User, verbose_name='注册用户')
    date = models.DateField(verbose_name='日期')
    cards = models.IntegerField(verbose_name='学习卡片数')
    thetime = models.IntegerField(verbose_name='学习时间')
    passed = models.BooleanField(default=False, verbose_name='是否达标')
    upload_time = models.DateTimeField(auto_now=True, verbose_name='提交时间')

    class Meta:
        verbose_name = "统计信息"
        verbose_name_plural = "统计信息"
        ordering = ['date', '-thetime', '-cards']

    def __str__(self):
        return '{username} studied {cards} cards in {thetime} seconds.'.format(username=self.user.username, cards=self.cards, thetime=self.thetime)

class FailRecord(models.Model):
    username = models.CharField(max_length=50, verbose_name="失败用户")
    s_count = models.IntegerField(verbose_name="连续打卡天数")
    penalty = models.IntegerField(verbose_name="罚金")

    class Meta:
        verbose_name = "失败信息统计"
        verbose_name_plural = "失败信息统计"

    def __str__(self):
        return '{username} studied {s_count} days.'.format(username=self.username, s_count=self.s_count)

class JoinRecord(models.Model):
    user = models.ForeignKey(User, verbose_name="注册用户")
    deposit = models.IntegerField(verbose_name="缴纳群费")

    class Meta:
        verbose_name = "入群信息统计"
        verbose_name_plural = "入群信息统计"

    def __str__(self):
        return '{username} paied {deposit} money.'.format(username=self.user.username, deposit=self.deposit)
