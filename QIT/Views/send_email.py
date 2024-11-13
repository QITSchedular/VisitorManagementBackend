# from django.core.mail import EmailMessage
# from QIT.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
# from QIT.Views import common

# import threading
# from threading import Thread

# class EmailThread(threading.Thread):
#     def __init__(self, subject, html_content, recipient_list):
#         self.subject = subject
#         self.recipient_list = recipient_list
#         self.html_content = html_content
#         threading.Thread.__init__(self)

#     def run (self):
#         msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
#         msg.content_subtype = "html"
#         msg.send()

# def send_html_mail(subject, html_content, recipient_list,cmpid):
#     data = common.get_host_credentials(cmpid)
#     if data:
#         hostname = data.get("hostname")
#         hostpasscode = data.get("hostpasscode")
#         # You can now use hostname and hostpasscode as needed
#         print("Hostname:", hostname)
#         print("Hostpasscode:", hostpasscode)
#     else:
#         hostname = data.get("hostname")
#         hostpasscode = data.get("hostpasscode")
#         print("No configuration found for the given company ID.")
#     EmailThread(subject, html_content, recipient_list).start()

from django.core.mail import EmailMessage, get_connection
from QIT.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD,EMAIL_HOST
from QIT.Views import common
import threading

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, hostname, hostpasscode):
        self.subject = subject
        self.html_content = html_content
        self.recipient_list = recipient_list
        self.hostname = hostname
        self.hostpasscode = hostpasscode
        super().__init__()

    def run(self):
        # Create a custom email connection using the provided hostname and hostpasscode
        print("--->",self.hostname)
        print("--->",self.hostpasscode)
        connection = get_connection(
            host=EMAIL_HOST,
            port=587,  # or the appropriate port for your SMTP server
            username=self.hostname,
            password=self.hostpasscode,
            use_tls=True  # or use_ssl=True depending on your SMTP server
        )

        # Create the email message with the custom connection
        msg = EmailMessage(
            self.subject,
            self.html_content,
            self.hostname,
            self.recipient_list,
            connection=connection
        )
        msg.content_subtype = "html"
        
        # Send the email
        try:
            msg.send()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")

def send_html_mail(subject, html_content, recipient_list, cmpid=None):
    # Fetch the SMTP configuration details
    if cmpid == None:
        hostname = EMAIL_HOST_USER
        hostpasscode = EMAIL_HOST_PASSWORD
    data = common.get_host_credentials(cmpid)
    print(data)
    if data:
        hostname = data.get("hostname")
        hostpasscode = data.get("hostpasscode")
    else:
        hostname = EMAIL_HOST_USER
        hostpasscode = EMAIL_HOST_PASSWORD
        # Start the email thread with the dynamic hostname and passcode
    print("hostname :",hostname)
    print("hostpasscode :",hostpasscode)
    EmailThread(subject, html_content, recipient_list, hostname, hostpasscode).start()


# from django.core.mail import EmailMessage
# from QIT.settings import EMAIL_HOST_USER
# from django.core.mail import get_connection
# import threading

# class EmailThread(threading.Thread):
#     def __init__(self, subject, html_content, recipient_list):
#         self.subject = subject
#         self.recipient_list = recipient_list
#         self.html_content = html_content
#         threading.Thread.__init__(self)

#     def run(self):
#         connection = get_connection()  # Get the default connection
#         for recipient in self.recipient_list:
#             try:
#                 msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, [recipient], connection=connection)
#                 msg.content_subtype = "html"
#                 msg.send()
#                 print(f"Email sent to {recipient}")
#             except Exception as e:
#                 print(f"Failed to send email to {recipient}: {e}")

# def send_html_mail(subject, html_content, recipient_list):
#     print("come here")
#     EmailThread(subject, html_content, recipient_list).start()
