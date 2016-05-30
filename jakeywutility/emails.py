# __author__ = 'jakey'


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jakeywutility.config.email_conf import SERVER, USER_NAME, PASS_WORD, SERVICE_EMAIL


def send_email(content, tos, subject="系统邮件", subtype="plain"):
    """
    发送邮件服务(文本形式)
    :param content: 邮件内容 string
    :param tos: 收件人列表  list
    :param subject: 邮件标题  list
    :param subtype: 内容格式 plain, html
    :return:
    """
    msg = MIMEText(content, subtype, "utf8")
    msg["Subject"] = subject
    msg["From"] = SERVICE_EMAIL
    msg["To"] = ",".join(tos)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(host=SERVER, port=25)
        smtp.login(USER_NAME, PASS_WORD)
        smtp.send_message(msg)
        smtp.quit()
    except Exception as e:
        print(e)


def send_attach(content, tos, file_path, subject="系统邮件", subtype="plain"):
    """
    发送带附件的邮件
    :param content:  邮件内容
    :param tos:  收件人邮箱
    :param file_path:　附件路径
    :param subject: 邮件主题
    :param subtype: 邮件内容格式
    :return:
    """
    import os
    if not os.path.isfile(file_path):
        raise TypeError('bad file path')
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = SERVICE_EMAIL
    message["To"] = ",".join(tos)
    message.attach(MIMEText(content, subtype, "utf8"))
    with open(file_path) as attach:
        file_name = os.path.basename(file_path)
        attachment = MIMEText(attach.read(), "base64", "utf8")
        attachment["Content-Type"] = "application/octet-stream"
        attachment["Content-Disposition"] = "attachment; filename=%s" % file_name
    message.attach(attachment)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(host=SERVER, port=25)
        smtp.login(USER_NAME, PASS_WORD)
        smtp.send_message(message)
        smtp.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    send_email(content="<p>Python 邮件发送测试...</p>", tos=["1226231147@qq.com"], subtype="html")
    send_attach(content="<p>Python 邮件发送测试...</p>", tos=["1226231147@qq.com"], subtype="html", file_path="/home/jakey/pythonProjects/jakeywutility/jakeywutility/logger.py")
