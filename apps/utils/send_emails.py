from django.core import mail


def send_email(message: str, from_email: str, to_emails: list[str],
               subject: str, html_message: str = None,
               is_html_activate: bool = False):
    try:
        email = mail.EmailMessage(subject, message,
                                  from_email, to_emails)

        if is_html_activate:
            email.content_subtype = 'html'
            email.attach_alternative(html_message, 'text/html')

        email.send(fail_silently=False)
    except Exception as e:
        print("SMTP ERROR: ", e)
