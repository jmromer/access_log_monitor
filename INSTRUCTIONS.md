HTTP log monitoring console program
===================================

At Datadog, we value working on real solutions to real problems, and as such we
think the best way to understand your capabilities is to give you the
opportunity to solve a problem similar to the ones we solve on a daily basis. As
the next step in our process, we ask that you write a simple console program
that monitors HTTP traffic on your machine. Treat this as an opportunity to show
us how you would write something you would be proud to put your name on. Feel
free to impress us.

* Consume an actively written-to [W3C-formatted HTTP access
  log][common-log-format]. It should default to reading /var/log/access.log and
  be overridable.

  Example:
  ```
  127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 1234
  127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 1234
  127.0.0.1 - frank [09/May/2018:16:00:42 +0000] "GET /api/user HTTP/1.0" 200 1234
  127.0.0.1 - mary [09/May/2018:16:00:42 +0000] "GET /api/user HTTP/1.0" 200 1234
  ```
* Display stats every 10s about the traffic during those 10s: the sections of
  the web site with the most hits, as well as interesting summary statistics on
  the traffic as a whole. A section is defined as being what's before the second
  '/' in the path. For example, the section for
  "http://my.site.com/pages/create” is "http://my.site.com/pages".

* Make sure a user can keep the app running and monitor the log file
  continuously

* Whenever total traffic for the past 2 minutes exceeds a certain number on
  average, add a message saying that “High traffic generated an alert - hits =
  {value}, triggered at {time}”. The default threshold should be 10 requests per
  second and should be overridable.

* Whenever the total traffic drops again below that value on average for the
  past 2 minutes, print or displays another message detailing when the alert
  recovered.

  * Write a test for the alerting logic.

* Explain how you'd improve on this application design.

* If you have access to a linux docker environment, we'd love to be able to
  docker build and run your project! If you don't though, don't sweat it. As an
  example:
  ```dockerfile
  FROM python:3

  RUN touch /var/log/access.log # since the program will read this by default

  WORKDIR /usr/src

  ADD . /usr/src

  ENTRYPOINT ["python", "main.py"]
  ```
  and we'll have something else write to that log file.

[common-log-format]: https://en.wikipedia.org/wiki/Common_Log_Format
