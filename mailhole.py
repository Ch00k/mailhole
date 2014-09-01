#!/usr/bin/env python


import asyncore
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
        subject = self.compile_subject(msg)
        body = self.get_body(msg)
        headers = self.get_headers(msg)
        mail_data = {
            'from': mailfrom, 'to': rcpttos, 'subject': headers['Subject'],
            'headers': headers, 'body': body
        }
        log.debug(mail_data)
        mail_file = '{}__{}'.format(subject, '_'.join(rcpttos)).lower()
        with open('{}/{}'.format(MAIL_DIR, mail_file), 'w') as f:
            f.write(json.dumps(mail_data))

    def compile_subject(self, message):
        original_subject = message.get('Subject')
        if original_subject:
            subject = original_subject.replace(' ', '_')
        else:
            subject = '__NOSUBJECT'
        return subject

    def get_headers(self, message):
        headers = {}
        for header in message.items():
            headers[header[0]] = header[1]
        return headers

    def get_body(self, message):
        body = []
        if message.is_multipart():
            for msg_part in message:
                body.append(msg_part.get_payload(decode=True))
        else:
            body.append(message.get_payload(decode=True))
        return body


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


def main():
    http_thread = threading.Thread(target=run_http)
    http_thread.daemon = True
    smtp_thread = threading.Thread(target=run_smtp)
    smtp_thread.daemon = True
    http_thread.start()
    smtp_thread.start()

    while http_thread.is_alive():
        http_thread.join(1)
    while smtp_thread.is_alive():
        smtp_thread.join(1)


if __name__ == '__main__':
    exit(main())
