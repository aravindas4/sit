
from datetime import date
import calendar

from django.core.mail import send_mail
from django.conf import settings
from simple import models as simple_models

from celery.decorators import task


@task()
def issue_notifier(issue, message):

    subject = 'Issue [{0}:{1}] {2}'.format(issue.id, issue.title, message)
    message = ' Issues for you! \n {0}-{1}'.format(issue.description, issue.status)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [str(issue.assigned_to.email)]
    return send_mail(subject, message, email_from, recipient_list)


@task()
def daily_issues_updates():
    email_from = settings.EMAIL_HOST_USER

    for user in simple_models.MyUser.objects.iterator():
        all_issues = simple_models.Issue.objects.filter(assigned_to=user, status="O").values('id', 'description')

        subject = '[{0}]: List of issues'.format(date.today().strftime('%A-%d-%B-%Y'))
        if all_issues:
            message = ' Issues for you! \n {0}'.format(all_issues)
        else:
            message = "NO ISSUES CHEERS"

        recipient_list = [str(user.email)]
        send_mail(subject, message, email_from, recipient_list)
    return True

