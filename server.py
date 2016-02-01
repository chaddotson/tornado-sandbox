import tornado.ioloop
import tornado.web
import tornado.websocket

import datetime
import random
import string


from tornado.options import define, options, parse_command_line

from tornado.escape import json_encode

import uuid

define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()


#chars = "".join([random.choice(string.letters) for j in xrange(10000)])	

chars = "".join([random.choice(string.letters) for j in xrange(3000)])	


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        #self.write("This is your response")
        self.render("index.html", DATA="THIS IS A TEST")
        #we don't need self.finish() because self.render() is fallowed by self.finish() inside tornado
        #self.finish()

import struct
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        #self.id = self.get_argument("Id")
        
        self.id = str(uuid.uuid4())
        
        self.stream.set_nodelay(True)

        # clients[self.id] = {"id": self.id, "object": self}
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0.25), self.update_client)
        # self.updater = tornado.ioloop.PeriodicCallback(self.update_client, 250)
        # self.updater.start()
        #
        # self.write_message(json_encode({"id": self.id}))

    def on_message(self, message):        
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        #print "Client %s received a message : %s" % (self.id, message)
        #self.write_message("Client %s received a message : %s" % (self.id, message))
        pass
       
    def update_client(self):
        #self.write_message(json_encode({"contents": chars}))
        #self.write_message("{\"TITLE\"=\"TEST\", \"DATA\"=" + struct.pack("3f", 1.2, 2.3, 3.4) + "}", binary=True)
        tester_string = "This is a test"
        fmt = "<I{0}s3f".format(len(tester_string))
        print fmt, len(struct.pack(fmt, len(tester_string), tester_string, 1.2, 2.3, 3.4))
        self.write_message(struct.pack(fmt, len(tester_string), tester_string, 1.2, 2.3, 3.4), binary=True)


    def on_close(self):
        # self.updater.stop()

        if self.id in clients:
            del clients[self.id]

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws/', WebSocketHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
