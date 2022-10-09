from issue.models import Task, Type
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Q


#Закрытые задачи за последний месяц от текущей даты
start_range = date.today() + relativedelta(months=-1)
end_range = date.today() + relativedelta(days=1)
Task.objects.filter(status__name='Done', created_at__range=[start_range, end_range])


#Задачи, имеющие один из двух указанных статусов И один из двух указанных типов
Task.objects.filter(
    Q(status__name='New') | Q(status__name='In Progress'),
    Q(type__name='Bug') | Q(type__name='Task')
)


#Задачи, в названии которых содержится слово "bug" в любом регистре или относящиеся к типу "Баг", 
# имеющие НЕ закрытый статус.
Task.objects.filter(Q(summary__iregex='bug') | Q(type__name='Bug')).exclude(status__name='Done')


# Для всех задач только следующие поля: id, название задачи, название типа и название статуса.
Task.objects.all().values('id', 'summary', 'status__name', 'type__name')


#Задачи, где краткое описание совпадает с полным.
summaries = Task.objects.all().values('summary')
summaries_list = []
for item in summaries:
    summaries_list.append(item.get('summary'))

Task.objects.filter(description__in=summaries_list)


#Количество задач по каждому типу.
types = Type.objects.all().values('name')
types_list = []
for item in types:
    types_list.append(item.get('name'))
counts = {}
for item in types_list:
    summaries = Task.objects.filter(type__name=item).count()
    counts[item] = summaries
