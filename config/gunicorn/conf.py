import multiprocessing

workers = multiprocessing.cpu_count() + 1
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(q)s" "%(D)s"'
keepalive = 1000
timeout = 1000
worker_class = "gevent"
threads = 4
