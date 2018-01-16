import smtplib
import subprocess
import os
from io import StringIO

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

EXPORT_PYTHON_PATH = "export PYTHONPATH=/home/vagrant/Test/Stable/" \
                     "Automation-Tests"
CMD_EXECUTOR = "python3.6 /home/vagrant/Test/Stable/Automation-Tests/" \
               "test_runner.py -rd -html"


def execute() -> str:
    """
    Execute all tests and return path to report file.

    :return: path to report file
    """
    result = subprocess.run([EXPORT_PYTHON_PATH + " & " + CMD_EXECUTOR],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=True)
    strio = StringIO(result.stdout.decode())
    path = strio.readlines()[-1].replace("Refer to ", "")
    path = path.replace("\n", "")
    return path


def create_file_attachment(file_path: str):
    """
    Create a file attachment for mail.
    :param file_path:
    :return: file attachment.
    """
    if not os.path.isfile(file_path):
        return None

    file_name = os.path.basename(file_path)
    file = open(file_path, "rb")
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition',
                          "attachment; filename= %s" % file_name)
    return attachment


def send_mail(report_path: str):
    receiver = "nghia.huynh@logigear.com"
    cc_lst = "chinh.do@logigear.com;khoi.ngo@logigear.com"

    user_name = "nhan.trong.nguyen@logigear.com"
    passwd = "KJLop1472."

    msg = MIMEMultipart()
    msg["From"] = user_name
    msg["To"] = receiver
    msg["cc"] = cc_lst
    msg["Subject"] = "[Evernym] Daily test report"

    main_body = "There is no test case executed today."

    html_report = create_file_attachment(report_path)
    json_report = create_file_attachment(report_path.replace(".html", ".json"))
    if html_report:
        main_body = "I would like to send you the report of "\
                    "test cases executed today."
        msg.attach(html_report)

    if json_report:
        msg.attach(json_report)

    body = "Hi anh Nghia,\n\n" + \
           main_body + "\n\n" \
           "Best regards.\n" \
           "--------------------------\n" \
           "Nhan Nguyen\n" \
           "Software Developer in Test"

    msg.attach(MIMEText(body, "plain"))

    mail_server = smtplib.SMTP('sgmail.logigear.com', 587)
    mail_server.starttls()
    mail_server.login(user_name, passwd)
    mail_server.sendmail(user_name, receiver, msg.as_string())
    mail_server.quit()


if __name__ == "__main__":
    send_mail(execute())
