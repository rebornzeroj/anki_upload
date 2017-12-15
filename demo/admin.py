from django.contrib import admin
from demo.models import *
from django.http import HttpResponse
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse
# Register your models here.


def get_penalty_percent(s_count):
    if s_count < 7:
        return 1
    elif s_count >= 7 and s_count < 15:
        return 0.8
    elif s_count >= 15 and s_count < 21:
        return 0.6
    elif s_count >= 21 and s_count < 30:
        return 0.4
    elif s_count >= 30 and s_count < 60:
        return 0.2
    else:
        return 0

def get_penalty(deposit, s_count):
    percent = get_penalty_percent(s_count)
    return deposit * percent

def fail_amend(modeladmin, request, queryset):
    user = queryset.get().user
    deposit = JoinRecord.objects.get(user=user).deposit
    total_stats = Stats.objects.filter(user=user)
    successful_stats = total_stats.filter(passed=True)
    s_count = successful_stats.count()
    penalty = get_penalty(deposit, s_count)
    FailRecord.objects.create(username=user.username, s_count=s_count, penalty=penalty)
    user.delete()
    return HttpResponse('连续打卡天数为{s_count}, 需要返还{r_money}元的费用'.format(s_count=s_count, r_money=deposit-penalty))

def fail(modeladmin, request, queryset):
    deposit = 5
    user = queryset.get().user
    total_stats = Stats.objects.filter(user=user)
    successful_stats = total_stats.filter(passed=True)
    s_count = successful_stats.count()
    penalty = get_penalty(deposit, s_count)
    FailRecord.objects.create(username=user.username, s_count=s_count, penalty=penalty)
    return HttpResponse('连续打卡天数为{s_count}, 需要返还{r_money}元的费用'.format(s_count=s_count, r_money=deposit-penalty))

class StatsAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = (
        'user', 'cards', 'thetime', 'passed', 'get_pretty_time', 'date')
    list_filter = [('user', admin.RelatedOnlyFieldListFilter), 'passed', 'date']
    search_fields = ['user__username', 'user__email', 'date']
    actions = [fail]

    def get_pretty_time(self, obj):
        thetime = obj.thetime
        if thetime < 60:
            return '{second}秒'.format(second=thetime)
        elif thetime > 60 and thetime < 3600:
            minute = thetime // 60
            second = thetime % 60
            return '{mintue}分{second}秒'.format(mintue=minute, second=second)
        elif thetime > 3600:
            hour = thetime // 3600
            minute = (thetime - hour * 3600) // 60
            second = thetime - hour * 3600 - minute * 60
            return '{hour}小时{minute}分钟{second}秒'.format(hour=hour, minute=minute, second=second)

    get_pretty_time.short_description = '别算时间了'

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_superuser', 'date_joined']
    def has_add_permission(self, request):
        return request.user.username == 'arco'

    def has_change_permission(self, request, obj=None):
        return request.user.username == 'arco'

    def has_delete_permission(self, request, obj=None):
        return request.user.username == 'arco'

class GroupAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.username == 'arco'

    def has_change_permission(self, request, obj=None):
        return request.user.username == 'arco'

    def has_delete_permission(self, request, obj=None):
        return request.user.username == 'arco'

class FailRecordAdmin(admin.ModelAdmin):
    list_display = (
        'username', 's_count', 'penalty')

class JoinRecordAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'deposit')

class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]
    search_fields = [
        'object_repr',
        'change_message'
    ]
    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return request.user.username == 'arco'

    def has_change_permission(self, request, obj=None):
        return request.user.username == 'arco'

    def has_delete_permission(self, request, obj=None):
        return request.user.username == 'arco'

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' %
                        (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

admin.site.register(Stats, StatsAdmin)
# admin.site.register(FailRecord, FailRecordAdmin)
# admin.site.register(JoinRecord, JoinRecordAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
