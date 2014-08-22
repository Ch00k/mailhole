#!/usr/bin/env python


import asyncore
import base64
import ConfigParser
import email
import json
import sys
import os
import threading
import SimpleHTTPServer
import SocketServer
import logging as log

from smtpd import SMTPServer


CONFIG = ConfigParser.RawConfigParser(allow_no_value=True)

CONFIG.read('/etc/mailhole/mailhole.conf')

SMTP_HOST = CONFIG.get('DEFAULT', 'smtp_host')
SMTP_PORT = CONFIG.getint('DEFAULT', 'smtp_port')
HTTP_HOST = CONFIG.get('DEFAULT', 'http_host')
HTTP_PORT = CONFIG.getint('DEFAULT', 'http_port')
MAIL_DIR = CONFIG.get('DEFAULT', 'maildir')
LOG_FILE = CONFIG.get('DEFAULT', 'log_file')

log.basicConfig(filename=LOG_FILE,
                format='[%(asctime)s]: %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d, %H:%M:%S',
                level=log.DEBUG)


class MailHoleSMTP(SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        msg = email.message_from_string(data)
        original_subject = msg.get('Subject')
        subject = original_subject.replace(' ', '_').lower()
        mail_file = '{}__{}'.format(subject, '_'.join(rcpttos))
        body = base64.b64decode(msg.get_payload()[0].get_payload())
        mail_data = {'from': mailfrom, 'to': rcpttos,
                     'subject': original_subject, 'body': body}
        log.debug(mail_data)
        with open('{}/{}'.format(MAIL_DIR, mail_file), 'w') as f:
            f.write(json.dumps(mail_data))


def run_smtp():
    MailHoleSMTP((SMTP_HOST, SMTP_PORT), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        sys.exit()
    except Exception, e:
        log.debug(e)
        pass


def run_http():
    try:
        os.chdir(MAIL_DIR)
        handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer((HTTP_HOST, HTTP_PORT), handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit()
    except Exception, e:
        log.debug(e)
        pass


if __name__ == '__main__':
    http_thread = threading.Thread(target=run_http)
    smtp_thread = threading.Thread(target=run_smtp)
    http_thread.start()
    smtp_thread.start()

    http_thread.join()
    smtp_thread.join()
