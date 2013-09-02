# HAFIZBOT
### Sufi Poetry Emailer

HAFIZBOT is a brief Python script that locates poems within a collection of poetry and emails them out simply.
It was designed to work with "Poems from the Divan of Hafiz", a late 19th century translation of the 14th C. Sufi poet.

* The SMTP library is being used to send the emails through GMail. The structure of the message gives some nice eerie to/from outputs.

* Another feature that might be fun is determining style based on the content of the line. Since the emails are sent as HTML, inline formatting is easy. There are currently rules for bolding and italicizing based on line content.

* HAFIZBOT now checks to make sure it hasn't already run on the current day before running, and records aborted attempts in the log

