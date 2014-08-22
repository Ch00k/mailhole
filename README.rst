**A simple service that can be used to test email sending functionality**

The service starts and listens on two different ports: one is a simple SMTP server that when it receives an email saves it into a file in JSON format; the other is a simple HTTP server that serves files in the directory where SMTP server puts them.

In order to use the service you need to create a config file in :code:`/etc/mailhole/mailhole.conf`

The service works with BASE64 encoded multipart emails (first part is plaintext, second part - HTML). It only take into account the first, plaintext part. It can easily be tuned to for any scenario you like though.