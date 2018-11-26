import os
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web
import time
import signal
import logging

import settings 

import templates
import lib.apply

class Application(tornado.web.Application):
  def __init__(self):

    app_settings = {
      "cookie_secret" :u"Rock_You_Like_A_Hurricane",
      "debug": False,
      "static_path" : os.path.join(os.path.dirname(__file__), "static"),
      "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    }
    handlers = [

      # apply stuff
      (r"/", lib.apply.Process),
      (r"", lib.apply.Process),
      (r"/apply", lib.apply.Process),
      (r"/apply/", lib.apply.Process),
      (r"/apply/admin", lib.apply.AdminList),
      (r"/apply/admin/api/tags/([^\/]+)", lib.apply.AdminApiTags),
      (r"/apply/admin/api/rate/([^\/]+)", lib.apply.AdminApiRate),
      (r"/apply/admin/api/comment/([^\/]+)", lib.apply.AdminApiComment),

    ]
    
    tornado.web.Application.__init__(self, handlers, **app_settings)
def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)
    
def shutdown():
    logging.info('Stopping http server')
    server.stop()

    logging.info('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')
    stop_loop()    

def main():
  tornado.options.define("port", default=8001, help="Listen on port", type=int)
  tornado.options.parse_command_line()
  logging.info("starting tornado_server on 0.0.0.0:%d" % tornado.options.options.port)
  http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
  http_server.listen(tornado.options.options.port)
  
  signal.signal(signal.SIGTERM, sig_handler)
  signal.signal(signal.SIGINT, sig_handler)
  
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
