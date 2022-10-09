from issue.models import Task
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
task_2 = Task.objects.filter(Q(summary__iregex='bug') | Q(type__name='Bug')).exclude(status__name='Done')
