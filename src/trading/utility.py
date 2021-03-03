
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta, date
import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from finance.settings import base as BASE_SETTINGS

# send email
def send_remider_mail(date, tracking):
	if date:
		context = {'current_site': "www.kubermitra.com", 'date': date, 'tracking': tracking}
		txt_  = render_to_string("partial/mail/message.txt", context)
		html_ = render_to_string('partial/mail/message.html', context)
		subject = 'kuebermitra.com : Daily Tracking Task !!!'
		from_email = BASE_SETTINGS.EMAIL_HOST_USER
		recipient_list = ['raj@koolbuch.com',]
		send_mail(
			subject,
			txt_,
			from_email,
			recipient_list,
			html_message=html_,
			fail_silently=False,
		)
		return True
	return False


