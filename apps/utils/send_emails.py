from django.core.mail import EmailMessage


def send_email(message, from_email, to_emails,
               subject, html_message=None,
               is_html_activate=False):
    email = EmailMessage(subject, message, from_email, to_emails)

    if is_html_activate:
        email.content_subtype = 'html'
        email.attach_alternative(html_message, 'text/html')

    email.send()
