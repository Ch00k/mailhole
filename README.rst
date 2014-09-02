mailhole
========

**A simple application to test email sending functionality**

The application starts two servers:

- a simple SMTP server that when it receives an email saves it into a file in JSON format;
- a simple HTTP server that serves files in the directory where SMTP server puts them.

Default behavior is to listen on :code:`127.0.0.1:4025` for SMTPconnections and :code:`127.0.0.1:4080` for HTTP connetctions,
write email files into current directory and log to STDOUT.
All of these settings can be overridden with command-line options. Also a configuration file can be specified.

Help::

    $ mailhole -h
    usage: mailhole.py [-h] [-m SMTP_HOST] [-p SMTP_PORT] [-t HTTP_HOST]
                       [-q HTTP_PORT] [-d MAILDIR] [-l LOG_FILE] [-c CONFIG_FILE]

    optional arguments:
      -h, --help            show this help message and exit
      -m SMTP_HOST, --smtp_host SMTP_HOST
                            SMTP server host (default: 127.0.0.1)
      -p SMTP_PORT, --smtp_port SMTP_PORT
                            SMTP server port (default: 4025)
      -t HTTP_HOST, --http_host HTTP_HOST
                            HTTP server host (default: 127.0.0.1)
      -q HTTP_PORT, --http_port HTTP_PORT
                            HTTP server port (default: 4080)
      -d MAILDIR, --maildir MAILDIR
                            Directory where emails are stored (default:
                            /Users/ay/PycharmProjects/mailhole)
      -l LOG_FILE, --log_file LOG_FILE
                            Log file (default: None)
      -c CONFIG_FILE, --config_file CONFIG_FILE
                            Config file path (default: None)

    Default behavior is to listen on 127.0.0.1:4025 for SMTPconnections and
    127.0.0.1:4080 for HTTP connetctions, write email files into current directory
    and log to STDOUT. All of these settings can be overridden with the options
    above. Also a configuration file can be specified that must contain all the
    above options.

Installation
------------

To install simply run::

    pip install mailhole

Running
-------

Start mailhole::

    $ mailhole
    [2014-09-02, 13:04:17]: INFO: SMTP server listening on 127.0.0.1:4025
    [2014-09-02, 13:04:17]: INFO: HTTP server listening on 127.0.0.1:4080

In another terminal send an email via a telnet connection::

    $ telnet 127.0.0.1 4025
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    220 ay-air Python SMTP proxy version 0.2
    MAIL FROM: sender@mailhole.net
    250 Ok
    RCPT TO: recepient@mailhole.net
    250 Ok
    DATA
    354 End data with <CR><LF>.<CR><LF>
    From: sender@mailhole.net
    To: recepient@mailhole.net
    Subject: Testing mailhole

    Hi!
    This is a mailhole test email

    .
    250 Ok
    ^]
    telnet> Connection closed.

Then in the terminal with mailhole running you should get this log line::

    [2014-09-02, 13:20:43]: DEBUG: {'body': ['Hi!\nThis is a mailhole test email\n'], 'to': ['recepient@mailhole.net'], 'from': 'sender@mailhole.net', 'headers': {'To': 'recepient@mailhole.net', 'From': 'sender@mailhole.net', 'Subject': 'Testing mailhole'}}

To test the HTTP server a simple curl request would work::

    $ curl 127.0.0.1:4080/testing_mailhole__recepient@mailhole.net
    {"body": ["Hi!\nThis is a mailhole test email\n"], "to": ["recepient@mailhole.net"], "from": "sender@mailhole.net", "headers": {"To": "recepient@mailhole.net", "From": "sender@mailhole.net", "Subject": "Testing mailhole"}}[2.1.2][refactoring] ~/PycharmProjects/gun
