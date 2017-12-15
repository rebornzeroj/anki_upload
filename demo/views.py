from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import json
import datetime
from demo.models import *

def upload_stats(request):
    return HttpResponse('Please Download The Latest Version <br/> Link: https://pan.baidu.com/s/1o8wf0ca Password: hrkd')

def say_yes(request):
    return HttpResponse('yes')

def sync(request):
    data = json.loads(request.body.decode())
    email = data.pop('email')
    try:
        user = User.objects.get(email=email)
    except Exception as e:
        return HttpResponse('NOT REGISTERED, PlEASE CONTACT THE ADMINSTRATOR')

    today = datetime.date.today()
    raw_stats = data['data']
    raw_stats.reverse()
    raw_today_stat = raw_stats.pop(0)
    if raw_today_stat[0] != 0:
        return HttpResponse('Maybe You Should Do Some Practice And Then Upload Again')
    for raw_stat in raw_stats:
        gap = datetime.timedelta(days=raw_stat[0])
        real_date = today + gap
        stats = Stats.objects.filter(user=user, date=real_date)
        if not stats:
            cards = sum(raw_stat[2:7])
            thetime = raw_stat[1]
            passed = thetime >= 30*60
            Stats.objects.create(user=user, date=real_date, cards=cards, thetime=thetime, passed=passed)
        else:
            break
    today_stat = Stats.objects.filter(user=user, date=today)
    passed = False
    if today_stat:
        today_stat = today_stat.get()
        cards = sum(raw_today_stat[2:7])
        thetime = raw_today_stat[1]
        passed = thetime >= 30*60
        today_stat.cards = cards
        today_stat.thetime = thetime
        today_stat.passed= passed
        today_stat.save()
    else:
        try:
            cards = sum(raw_today_stat[2:7])
            thetime = raw_today_stat[1]
            passed = thetime >= 30*60
            Stats.objects.create(user=user, date=today, cards=cards, thetime=thetime, passed=passed)
        except Exception as e:
            return HttpResponse('Maybe You Should Do Some Practice And Then Upload Again')
    if passed:
        total_count = Stats.objects.filter(date=today).count()
        current_stat = Stats.objects.get(user=user, date=today)
        all_stats = Stats.objects.filter(date=today).order_by('-thetime')
        rank = 0
        for i in range(len(all_stats)):
            if all_stats[i] == current_stat:
                rank = i + 1
                break
        return HttpResponse('Congradulations! <br/> You Already Finsh The Task <br/> And.. You Are Number {rank} Of Total {t_count} People'
                            .format(rank=rank, t_count=total_count))
    else:
        return HttpResponse('Sync Succeed <br/> Keep Learning!!')

@login_required()
def statistcs(request):
    date = datetime.datetime.now()
    users = User.objects.filter(is_superuser=False)
    full_count = users.count()
    stats = Stats.objects.filter(date=date)
    total_count = stats.count()
    if total_count < full_count:
        absence_list = []
        for user in users:
            absence_list.append(user.username)
        for stat in stats:
            absence_list.remove(stat.user.username)
        absence_count = absence_list.count()
        stats = stats.filter(passed=False)
        if stats:
            unsuccessful_count = stats.count()
            successful_count = total_count - unsuccessful_count
            list = []
            for stat in stats:
                list.append(stat.user.username)
            return HttpResponse('本系统注册用户为{f_count}人<br/> 目前, {t_count} 人提交了打开数据br/> 其中, {s_count}人完成任务<br/> {u_count}人失败<br/>'
                                ' 失败名单为: {fail_list}<br/> 未提交打卡数据人员名单为: {absence_list}.'
                                .format(f_count=full_count, t_count=total_count, s_count=successful_count,
                                        u_count=unsuccessful_count, fail_list=','.join(list), absence_list=','.join(absence_list)))
        else:
            return HttpResponse('本系统注册用户为{f_count}人<br/> 目前, {t_count}人提交了打卡数据且全部完成任务<br/> 未提交打卡数据人员名单为: {absence_list}'
                                .format(f_count=full_count, t_count=total_count, absence_list=','.join(absence_list)))
    else:
        stats = stats.filter(passed=False)
        if stats:
            unsuccessful_count = stats.count()
            successful_count = total_count - unsuccessful_count
            fail_list = []
            for stat in stats:
                fail_list.append(stat.user.username)
            return HttpResponse('本系统注册用户为{f_count}人<br/> 目前, 所有注册用户都已提交打卡数据<br/> {s_count}人完成任务<br/> {u_count}人失败<br/> 失败名单为: {fail_list}.'
                            .format(f_count=full_count, s_count=successful_count,
                                    u_count=unsuccessful_count, fail_list=','.join(fail_list)))
        else:
            return HttpResponse('本系统注册用户为{f_count}人<br/> 目前, 所有注册用户都已提交打卡数据且全部完成任务.'
                            .format(f_count=full_count))


def test_mail(request):
    send_mail('test', 'test', 'friedjuice@aliyun.com', ['904568622@qq.com'])
    return HttpResponse('ok')