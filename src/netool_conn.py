# -*- coding: utf-8 -*-

###################################
# Netool
#
# tcp/udp tool
#
# connections
###################################

from gevent.server import DatagramServer, StreamServer
from gevent import socket, Greenlet
from gevent import monkey
monkey.patch_all()
from gevent.event import AsyncResult

import _socket

import time
import sys
import json
import base64

import wx

from netool_common import DBG, DBG_TRACE


class CloseSocket(Exception):
    pass


class SendData(Exception):
    pass


class StopServer(Exception):
    pass

conn_greenlets = {}
guifeeder_socket = socket.socket(type = socket.SOCK_DGRAM)
LOCAL_IP = '127.0.0.1'
GUIFEEDER_ADDRESS = (LOCAL_IP, 62222)


class NetoolDatagramServer(DatagramServer):  # modify recvfrom buffer length
    def __init__(self, *args, **kwargs):
        DBG("NetoolDatagramServer __init__")
        DatagramServer.__init__(self, *args, **kwargs)

    def do_read(self):
        try:
            data, address = self._socket.recvfrom(65535)
        except _socket.error, err:
            if err[0] == socket.EWOULDBLOCK:
                return
            raise
        return data, address


class NetoolGUIFeeder(NetoolDatagramServer):
    def __init__(self, window, *args, **kwargs):
        DBG("NetoolGUIFeeder __init__ %r" % window)
        NetoolDatagramServer.__init__(self, *args, **kwargs)
        self.window = window

    def handle(self, data, address):
        DBG('NetoolGUIFeeder %s %s: got %r' % (time.ctime(), address[0], data))

        try:
            data = json.loads(data)
            if data['op'] == 'closeapp':
                DBG("GUIFeeder stop")
                self.stop()
                return
            wx.CallAfter(self.window.eat, data)
        except:
            DBG_TRACE()


def run_connection(conn_data):
    DBG('run_connection %r' % conn_data)
    need_to_close = False
    need_to_send_data = False
    conn_socket = None
    try:
        if conn_data['type'] == 'udpconn':
            conn_socket = socket.socket(type = socket.SOCK_DGRAM)
        elif conn_data['type'] == 'tcpconn':
            conn_socket = socket.socket(type = socket.SOCK_STREAM)
        if not conn_data['random_port']:
            conn_socket.bind(("192.168.0.100", conn_data['specific_port']))
        conn_socket.connect((conn_data['remote_ip'], int(conn_data['remote_port'])))

        conn_greenlets[conn_data['name']]['result'].set({'result':'ok', 'port':conn_socket.getsockname()[1]})  # new connection ok
    except:
        DBG_TRACE()
        conn_greenlets[conn_data['name']]['result'].set({'result':'error', 'error':base64.b64encode(str(sys.exc_info()[1]))})  # new connection failed
        return

    while True:
        if need_to_close:
            DBG('run_connection need_to_close')
            conn_socket.close()
            conn_greenlets[conn_data['name']]['result'].set({'result':'ok'})
            return
        if need_to_send_data:
            try:
                conn_socket.sendall(base64.b64decode(conn_greenlets[conn_data['name']]['data']))
                conn_greenlets[conn_data['name']]['result'].set('ok')
                need_to_send_data = False
            except:
                DBG_TRACE()
                conn_greenlets[conn_data['name']]['result'].set('error')

        try:
            data = conn_socket.recv(4096)
            if not data:  # closed by remote
                DBG('run_connection got nothing')
                conn_socket.close()
                data_pack = {"name":conn_data['name'], "op":"disconnected"}
                re = guifeeder_socket.sendto(json.dumps(data_pack), GUIFEEDER_ADDRESS)
                DBG("sent to gui feeder %r" % re)

                return  # die
            else:
                DBG(type(data))
                DBG('run_connection %s got %r' % (time.ctime(), bytearray(data)))
                data_pack = {"name":conn_data['name'], "op":"recvdata", "text":base64.b64encode(bytearray(data))}
            re = guifeeder_socket.sendto(json.dumps(data_pack), GUIFEEDER_ADDRESS)
            DBG("sent to gui feeder %r" % re)
        except CloseSocket:
            DBG("run_connection CloseSocket")
            need_to_close = True
        except SendData:
            DBG("run_connection SendData")
            need_to_send_data = True
        except:
            DBG_TRACE()
            data_pack = {"name":conn_data['name'], 'type':conn_data['type'], "op":"error", 'msg':base64.b64encode(str(sys.exc_info()[1]))}
            conn_socket.close()
            del conn_greenlets[conn_data['name']]
            re = guifeeder_socket.sendto(json.dumps(data_pack), GUIFEEDER_ADDRESS)
            DBG("sent to gui feeder %r" % re)
            return
        '''
        except _socket.error:
            ex = sys.exc_info()[1]
            strerror = getattr(ex, 'strerror', None)
            if strerror is not None:
                ex.strerror = strerror + ': ' + repr(address)
        '''


class NetoolTcpServer(StreamServer):
    def __init__(self, conn_data = None, *args, **kwargs):
        StreamServer.__init__(self, *args, **kwargs)
        DBG("xcc NetoolTcpServer")
        self.conn_data = conn_data
        self.accept_count = 0

    def do_read(self):
        DBG("xcc NetoolTcpServer.do_read()")
        try:
            client_socket, address = self.socket.accept()
        except _socket.error, err:
            if err[0] == socket.EWOULDBLOCK:
                DBG("NetoolTcpServer do_read() EWOULDBLOCK return")
                return
            raise
        DBG("NetoolTcpServer do_read() return")
        self.accept_count += 1
        return socket.socket(_sock=client_socket), address, self.conn_data, self.accept_count


def tcp_handler(socket, address, conn_data, accept_count):
    need_to_close = False
    need_to_send_data = False
    accepted_name = conn_data['name'] + '-%d' % accept_count
    conn_greenlets[accepted_name] = {'greenlet':Greenlet.getcurrent(), 'result':None, 'data':None}
    DBG('new tcp accepted from %s:%s conn_data = %r' % (address[0], address[1], conn_data))
    data_pack = dict(name = conn_data['name'], accepted_name = accepted_name, op = "accepted", remote_ip = address[0],
                     remote_port = address[1], local_port = conn_data['specific_port'], type = 'tcpserver')
    re = guifeeder_socket.sendto(json.dumps(data_pack), GUIFEEDER_ADDRESS)
    DBG("sent to gui feeder %r" % re)

    while True:
        try:
            if need_to_close:
                DBG('tcp_handler need_to_close')
                socket.close()
                conn_greenlets[accepted_name]['result'].set({'result':'ok'})
                return
            if need_to_send_data:
                try:
                    re = socket.send(base64.b64decode(conn_greenlets[accepted_name]['data']))
                    conn_greenlets[accepted_name]['result'].set('ok')
                    DBG("sent to remote %r" % re)
                    need_to_send_data = False
                except:
                    DBG_TRACE()
                    conn_greenlets[accepted_name]['result'].set('error')

            data = socket.recv(8012)

            if not data:  # closed by remote
                DBG('tcp_handler got nothing')
                socket.close()
                data_pack = {"name":accepted_name, "op":"disconnected"}
                re = guifeeder_socket.sendto(json.dumps(data_pack), GUIFEEDER_ADDRESS)
                del conn_greenlets[accepted_name]
                DBG("sent to gui feeder %r" % re)
                return  # die

            else:
                DBG(type(data))
                DBG('tcp_handler %s got %r' % (time.ctime(), bytearray(data)))
                data_pack = {"name":accepted_name, "op":"recvdata", "text":base64.b64encode(bytearray(data))}
                # socket.send('hi')
            re = guifeeder_socket.sendto(json.dumps(data_pack), GUIFEEDER_ADDRESS)
            DBG("sent to gui feeder %r" % re)
        except CloseSocket:
            DBG("tcp_handler CloseSocket")
            need_to_close = True
        except SendData:
            DBG("tcp_handler SendData")
            need_to_send_data = True
        except:
            DBG_TRACE()
            data_pack = {"name":conn_data['name'], 'type':conn_data['type'], "op":"error", 'msg':base64.b64encode(str(sys.exc_info()[1]))}
            socket.close()
            del conn_greenlets[conn_data['name']]
            re = guifeeder_socket.sendto(json.dumps(data_pack), GUIFEEDER_ADDRESS)
            DBG("sent to gui feeder %r" % re)
            return


def start_tcp_server(conn_data):
    DBG("start_tcp_server")
    server = None
    try:
        conn_greenlets[conn_data['name']]['result'].set({'result':'ok'})  # new server ok
        server = NetoolTcpServer(conn_data, (LOCAL_IP, conn_data['specific_port']), tcp_handler)
        server.serve_forever()
    except StopServer:
        DBG("StopServer")
        server.stop()
        conn_greenlets[conn_data['name']]['result'].set({'result':'ok'})  # new server ok
        return
    except:
        DBG_TRACE()
        data_pack = {'name':conn_data['name'], 'type':conn_data['type'], 'op':'error', 'msg':base64.b64encode(str(sys.exc_info()[1]))}
        server.stop()
        del conn_greenlets[conn_data['name']]
        guifeeder_socket.sendto(json.dumps(data_pack), GUIFEEDER_ADDRESS)


class NetoolCommandServer(NetoolDatagramServer):
    def __init__(self, *args, **kwargs):
        NetoolDatagramServer.__init__(self, *args, **kwargs)

    def make_new_connection(self, data, reply_address):
        DBG("NetoolCommandServer make_new_connection %r" % data)
        try:
            g = Greenlet(run_connection, data)
            g.start()

            result = AsyncResult()
            conn_greenlets[data['name']] = {'greenlet':g, 'result':result, 'data':None}
            re = result.get()
            value = re['result']
            if value != 'ok':
                del(conn_greenlets[data['name']])
            re = self.socket.sendto(json.dumps(re), reply_address)
            DBG("sent %d" % re)
        except:
            DBG_TRACE()
            self.socket.sendto(json.dumps({'result':'error', 'msg':base64.b64encode(sys.exc_info()[1])}), reply_address)

    def disconnect_connection(self, data, reply_address):
        DBG("NetoolCommandServer disconnect_connection %r" % data)
        try:
            conn_greenlets[data['name']]['greenlet'].kill(exception = CloseSocket, block = False)

            result = AsyncResult()
            conn_greenlets[data['name']]['result'] = result
            value = result.get()
            conn_greenlets[data['name']]['greenlet'].join()
            del conn_greenlets[data['name']]
            re = self.socket.sendto(json.dumps(value), reply_address)
            DBG("sent %d" % re)
        except:
            DBG_TRACE()
            self.socket.sendto(json.dumps({'result':'error', 'msg':base64.b64encode(sys.exc_info()[1])}), reply_address)

    def disconnect_accepted(self, data, reply_address):
        DBG("NetoolCommandServer disconnect_accepted %r" % data)
        try:
            if not data['accepted_name'] in conn_greenlets:  # already closed
                self.socket.sendto(json.dumps({'result':'ok'}), reply_address)
                return
            conn_greenlets[data['accepted_name']]['greenlet'].kill(exception = CloseSocket, block = False)

            result = AsyncResult()
            conn_greenlets[data['accepted_name']]['result'] = result
            value = result.get()
            conn_greenlets[data['accepted_name']]['greenlet'].join()
            del conn_greenlets[data['accepted_name']]
            re = self.socket.sendto(json.dumps(value), reply_address)
            DBG("sent %d" % re)
        except:
            DBG_TRACE()
            self.socket.sendto(json.dumps({'result':'error', 'msg':base64.b64encode(sys.exc_info()[1])}), reply_address)

    def make_new_tcp_server(self, data, reply_address):
        DBG("NetoolCommandServer make_new_tcp_server %r" % data)
        try:
            g = Greenlet(start_tcp_server, data)
            g.start()

            result = AsyncResult()
            conn_greenlets[data['name']] = {'greenlet':g, 'result':result, 'data':None}
            re = result.get()
            value = re['result']
            if value != 'ok':
                del(conn_greenlets[data['name']])
            re = self.socket.sendto(json.dumps(re), reply_address)
            DBG("sent %d" % re)
        except:
            DBG_TRACE()
            self.socket.sendto(json.dumps({'result':'error', 'msg':base64.b64encode(sys.exc_info()[1])}), reply_address)

    def stop_tcp_server(self, data, reply_address):
        DBG("NetoolCommandServer stop_tcp_server %r" % data)
        try:
            conn_greenlets[data['name']]['greenlet'].kill(exception = StopServer, block = False)

            result = AsyncResult()
            conn_greenlets[data['name']]['result'] = result
            re = result.get()
            value = re['result']
            if value != 'ok':
                del(conn_greenlets[data['name']])
            re = self.socket.sendto(json.dumps(re), reply_address)
            DBG("sent %d" % re)
        except:
            DBG_TRACE()
            self.socket.sendto(json.dumps({'result':'error', 'msg':base64.b64encode(sys.exc_info()[1])}), reply_address)

    def send_data(self, data, reply_address):
        DBG("NetoolCommandServer disconnect_connection %r" % data)
        try:
            conn_greenlets[data['name']]['greenlet'].kill(exception = SendData, block = False)

            result = AsyncResult()
            conn_greenlets[data['name']]['result'] = result
            conn_greenlets[data['name']]['data'] = data['data']
            value = result.get()
            re = self.socket.sendto(value, reply_address)
            DBG("sent %d" % re)
        except:
            DBG_TRACE()
            self.socket.sendto(json.dumps({'result':'error', 'msg':base64.b64encode(sys.exc_info()[1])}), reply_address)

    def handle(self, data, address):
        DBG('NetoolCommandServer %s %s:%d got %r' % (time.ctime(), address[0], address[1], data))
        DBG('len = %d' % len(data))

        try:
            data = json.loads(data)

            op = data['op']

            if op == 'closeapp':
                self.socket.sendto(json.dumps({'op':'closeapp'}), GUIFEEDER_ADDRESS)
                self.socket.sendto(json.dumps({'result':'ok'}), address)
                DBG("NetoolCommandServer stop")
                self.stop()
            elif op == 'disconnect':
                if data['type'] == 'tcpaccepted':
                    self.disconnect_accepted(data, address)
                else:
                    self.disconnect_connection(data, address)
            elif op == 'senddata':
                self.send_data(data, address)
            elif op == 'connect':
                if data['type'] == 'udpconn' or data['type'] == 'tcpconn':
                    self.make_new_connection(data, address)
            elif op == 'start':
                if data['type'] == 'tcpserver':
                    self.make_new_tcp_server(data, address)
            elif op == 'stop':
                if data['type'] == 'tcpserver':
                    self.stop_tcp_server(data, address)
            else:
                self.socket.sendto(json.dumps({'result':'error', 'msg':'unknown command'}), address)
        except:
            DBG_TRACE()
            self.socket.sendto(json.dumps({'result':'error', 'msg':base64.b64encode(sys.exc_info()[1])}), address)