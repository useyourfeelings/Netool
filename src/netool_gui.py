# -*- coding: utf-8 -*- 

###################################
# Netool
#
# tcp/udp tool
#
# gui
###################################

import wx
import wx.xrc
import sys
import wx.dataview

import json

import time
import base64

from netool_common import DBG, DBG_TRACE
from netool_forms import MainFrame, ConnPage, NewServerDialog, StashDialog

import socket
COMMAND_SERVER_ADDRESS = ("127.0.0.1", 62223)

CONN_TYPE_UNKNOWN = 0
CONN_TYPE_UDP_CONN = 1
CONN_TYPE_TCP_CONN = 2
CONN_TYPE_HTTP_CONN = 3
CONN_TYPE_UDP_CLIENT = 4
CONN_TYPE_TCP_ACCEPTED = 5

wx.ID_DELETE_NODE = 2000
wx.ID_STASH_MODIFY = 2001
wx.ID_STASH_TAKE = 2002
wx.ID_STASH_ADD = 2003
wx.ID_STASH_DELETE = 2004

DEFAULT_CONFIG = {"connections": [{"name": "conn at 11:02:03 test", "remote_port": 22223, "random_port": True, "remote_ip": "127.0.0.1", "type": "udpconn", "specific_port": 55556},
                                  {"name": "conn at 11:02:21 test", "remote_port": 22223, "random_port": True, "remote_ip": "127.0.0.1", "type": "udpconn", "specific_port": 55556}],
                "config": {"udp_recv_buffer_len": 65535},
                "stash": [{"data": "??", "name": "shortcut"},
                          {"data": "01 02 003 456", "name": "shortcut"}],
                "servers": []}

###########################################################################
# Class MainFrame
###########################################################################


class NetoolNewServerDialog(NewServerDialog):
	def __init__(self):
		NewServerDialog.__init__(self, None)
		default_name = "server at %02d:%02d:%02d" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
		self.name.SetValue(default_name)
		self.radio_tcp.SetValue(True)
		self.radio_udp.Disable()

	def on_click_ok(self, event):
		event.Skip()

	def on_click_cancel(self, event):
		event.Skip()


class NetoolMainFrame(MainFrame):

	def __init__(self, command_server_address = COMMAND_SERVER_ADDRESS):
		MainFrame.__init__(self, None)

		self.pages = {}
		self.nodes = {}
		self.servers = {}
		self.command_server_address = command_server_address

		root = self.connection_tree.AddRoot("root")
		self.connection_node = self.connection_tree.AppendItem(root, 'connection')
		self.server_node = self.connection_tree.AppendItem(root, 'server')
		self.nodes['connection'] = self.connection_node
		self.nodes['server'] = self.server_node

		self.connection_tree.ExpandAll()
		try:
			self.command_sender = socket.socket(type = socket.SOCK_DGRAM)
		except:
			DBG_TRACE()
			self.alert("NetoolMainFrame __init__ error")

		self.node_menu = wx.Menu()
		menu_item = wx.MenuItem(self.node_menu, wx.ID_DELETE_NODE, 'Close')
		self.node_menu.AppendItem(menu_item)
		self.Bind(wx.EVT_MENU, self.on_popup_close_node, menu_item)

		self.stash_menu = wx.Menu()
		menu_item = wx.MenuItem(self.stash_menu, wx.ID_STASH_ADD, 'Add')
		self.stash_menu.AppendItem(menu_item)
		self.Bind(wx.EVT_MENU, self.on_popup_stash_add, menu_item)

		menu_item = wx.MenuItem(self.stash_menu, wx.ID_STASH_MODIFY, 'Modify')
		self.stash_menu.AppendItem(menu_item)
		self.Bind(wx.EVT_MENU, self.on_popup_stash_modify, menu_item)

		menu_item = wx.MenuItem(self.stash_menu, wx.ID_STASH_DELETE, 'Delete')
		self.stash_menu.AppendItem(menu_item)
		self.Bind(wx.EVT_MENU, self.on_popup_stash_delete, menu_item)

		menu_item = wx.MenuItem(self.stash_menu, wx.ID_STASH_TAKE, 'Take')
		self.stash_menu.AppendItem(menu_item)
		self.Bind(wx.EVT_MENU, self.on_popup_stash_take, menu_item)

		self.list_stash.AppendTextColumn('Name', width = 80)
		self.list_stash.AppendTextColumn('Data', width = 150)

	def on_stash_context_menu(self, event):
		DBG('on_stash_context_menu')
		self.PopupMenu(self.stash_menu)
		event.Skip()

	def on_item_right_click(self, event):
		DBG(event.GetId())
		self.connection_tree.SelectItem(event.GetItem())

		name = self.connection_tree.GetItemText(event.GetItem())

		for i in range(0, self.connection_notebook.GetPageCount()):
			if self.connection_notebook.GetPageText(i) == name:
				self.connection_notebook.SetSelection(i)

		self.connection_tree.SetFocus()

		self.PopupMenu(self.node_menu)
		event.Skip()

	def on_popup_close_node(self, event):
		name = self.connection_tree.GetItemText(self.connection_tree.GetFocusedItem())
		self.close_node(name)
		event.Skip()

	def on_popup_stash_add(self, event):
		dlg = StashDialog(self)
		if dlg.ShowModal() != wx.ID_OK:
			dlg.Destroy()
			return

		self.list_stash.AppendItem((dlg.input_name.GetValue(), dlg.input_data.GetValue()))

	def on_popup_stash_modify(self, event):
		row = self.list_stash.GetSelectedRow()
		if row == -1:
			return
		name = self.list_stash.GetTextValue(row, 0)
		data = self.list_stash.GetTextValue(row, 1)
		dlg = StashDialog(self)
		dlg.input_name.SetValue(name)
		dlg.input_data.SetValue(data)
		if dlg.ShowModal() != wx.ID_OK:
			dlg.Destroy()
			return

		self.list_stash.SetTextValue(dlg.input_name.GetValue(), row, 0)
		self.list_stash.SetTextValue(dlg.input_data.GetValue(), row, 1)

		event.Skip()

	def on_popup_stash_delete(self, event):
		row = self.list_stash.GetSelectedRow()
		if row == -1:
			return
		self.list_stash.DeleteItem(row)
		event.Skip()

	def on_popup_stash_take(self, event):
		row = self.list_stash.GetSelectedRow()
		if row == -1:
			return
		DBG(self.list_stash.GetColumns()[0])
		self.connection_notebook.GetCurrentPage().input_send.SetValue(self.list_stash.GetTextValue(row, 1))
		event.Skip()

	def close_node(self, name):# close a initiative connection or an accepted connection or a server(with its all accepted connections)
		DBG('close_node %s' % name)

		if name == 'root' or name == 'connection' or name == 'server':
			return False

		try:
			if name in self.pages:  #a connection
				page = self.pages[name]
				result = page.on_close()
				if result['result'] == 'ok':
					for i in range(0, self.connection_notebook.GetPageCount()):
						if name == self.connection_notebook.GetPageText(i):
							self.connection_notebook.DeletePage(i)
					del self.pages[name]

					self.connection_tree.Delete(self.nodes[name])
					del self.nodes[name]
					return True
				else:
					return False
			else:#a server
				node = self.nodes[name]

				DBG('close children')

				accepted_node = self.connection_tree.GetFirstChild(node)[0]
				DBG(accepted_node)
				while accepted_node.IsOk():
					accepted_name = self.connection_tree.GetItemText(accepted_node)
					accepted_node = self.connection_tree.GetNextSibling(accepted_node)
					if not self.close_node(accepted_name):
						return False

				query = {"name":name, "type":self.servers[name]['type'], "op":"stop"}

				re = self.command_sender.sendto(json.dumps(query), self.command_server_address)
				DBG('sent %d' % re)
				data = self.command_sender.recv(4096)
				DBG("reply - %r" % data)
				data = json.loads(data)
				if data['result'] != 'ok':
					self.alert(base64.b64decode(data['error']))
					return False
				else:
					self.connection_tree.Delete(self.nodes[name])
					del self.nodes[name]
					del self.servers[name]
					return True
		except:
			DBG_TRACE()
			return False

	def new_connection(self, event):
		DBG("new_connection")
		try:
			default_name = "conn at %02d:%02d:%02d" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
			dlg = wx.TextEntryDialog(self, "name", "New connection", default_name, pos = wx.DefaultPosition)
			name = None
			while True:
				if dlg.ShowModal() != wx.ID_OK:
					return
				name = dlg.GetValue()
				if name in self.pages or name == 'server' or name == 'connection' or name == 'root':
					self.alert("this name already exist")
				else:
					break
			dlg.Destroy()

			node = self.connection_tree.AppendItem(self.connection_node, name)
			self.nodes[name] = node

			page = ConnectionPage(self.connection_notebook, self, name, command_sender = self.command_sender)
			self.connection_notebook.AddPage(page, name)
			index = self.connection_notebook.GetPageCount() - 1  # get the index of the final page.
			self.connection_notebook.SetSelection(index)
			self.pages[name] = page

			self.connection_tree.ExpandAll()
		except:
			DBG_TRACE()
		event.Skip()

	def new_server(self, event):
		DBG("new_server")
		try:
			dlg = NetoolNewServerDialog()
			name = ''
			conn_type = ''
			while True:
				if dlg.ShowModal() != wx.ID_OK:
					dlg.Destroy()
					return
				name = dlg.name.GetValue()
				if name in self.nodes or name == 'server' or name == 'connection' or name == 'root':
					self.alert("this name already exist")
				else:
					break

			if dlg.radio_tcp.GetValue():
				conn_type = 'tcpserver'
			else:
				conn_type = 'udpserver'
			query = {"name":name, "type":conn_type, "op":"start", "specific_port":int(dlg.specific_port.GetValue())}

			re = self.command_sender.sendto(json.dumps(query), self.command_server_address)
			DBG('sent %d' % re)
			data = self.command_sender.recv(4096)
			DBG("reply - %r" % data)
			data = json.loads(data)
			if data['result'] != 'ok':
				self.alert(base64.b64decode(result['error']))
			else:
				node = self.connection_tree.AppendItem(self.server_node, dlg.name.GetValue())
				self.nodes[dlg.name.GetValue()] = node
				self.servers[dlg.name.GetValue()] = {'name':name, 'type':conn_type, 'specific_port':int(dlg.specific_port.GetValue())}
				self.connection_tree.ExpandAll()
			dlg.Destroy()
		except:
			DBG_TRACE()
			self.alert(str(sys.exc_info()[1]))
		event.Skip()

	def load_status(self):

		DBG("load_status")
		file = None
		data = None
		try:
			file = open('netool.config', 'r+')
			data = file.read()
			data = json.loads(data)
		except IOError:
			DBG_TRACE()
			file = open('netool.config', 'w')
			file.write(json.dumps(DEFAULT_CONFIG))
			file.close()
			data = DEFAULT_CONFIG
			self.alert('Wrong config file, using default!')

		except:
			DBG_TRACE()
			file.truncate(0)
			file.seek(0, 0)
			file.write(json.dumps(DEFAULT_CONFIG))
			file.close()
			data = DEFAULT_CONFIG
			self.alert('Wrong config file, using default!')

		DBG(data)

		try:
			for conn in data['connections']:
				name = conn['name']
				node = self.connection_tree.AppendItem(self.connection_node, name)
				self.nodes[name] = node

				page = ConnectionPage(self.connection_notebook, self, name, command_sender = self.command_sender)
				page.remote_ip.SetValue(conn['remote_ip'])
				page.remote_port.SetValue(str(conn['remote_port']))
				if conn['type'] == 'udpconn':
					page.radio_udp.SetValue(True)
				else:
					page.radio_tcp.SetValue(True)
				if conn['random_port']:
					page.radio_random_port.SetValue(True)
				else:
					page.radio_specific_port.SetValue(True)
				page.specific_port.SetValue(str(conn['specific_port']))

				self.connection_notebook.AddPage(page, name)
				index = self.connection_notebook.GetPageCount() - 1  # get the index of the final page.
				self.connection_notebook.SetSelection(index)
				self.pages[name] = page

			self.connection_tree.ExpandAll()

			for item in data['stash']:
				self.list_stash.AppendItem((item['name'], item['data']))

		except:
			DBG_TRACE()

	def save_status(self):
		file = None
		config = None
		try:
			file = open('netool.config', 'r+')
			config = file.read()
		except IOError:
			try:
				file = open('netool.config', 'w')
				config = {'stash':[], 'config':{'udp_recv_buffer_len':65535}, 'connections':[], 'servers':[]}
			except:
				DBG_TRACE()
		except:
			DBG_TRACE()

		try:
			config = json.loads(config)
		except:
			config = {'stash':[], 'config':{'udp_recv_buffer_len':65535}, 'connections':[], 'servers':[]}

		# save connections
		connections = []
		node = self.nodes['connection']
		node = self.connection_tree.GetFirstChild(node)[0]
		while node.IsOk():
			name = self.connection_tree.GetItemText(node)
			page = self.pages[name]
			conn_type = 'udpconn'
			if page.radio_tcp.GetValue():
				conn_type = 'tcpconn'
			connections.append({"name":page.name, "type":conn_type, "remote_ip":page.remote_ip.GetValue(),
						 		"remote_port":int(page.remote_port.GetValue()), "random_port":page.radio_random_port.GetValue(),
								"specific_port":int(page.specific_port.GetValue())})
			node = self.connection_tree.GetNextSibling(node)

		# save servers
		servers = []
		node = self.nodes['server']
		node = self.connection_tree.GetFirstChild(node)[0]
		while node.IsOk():
			name = self.connection_tree.GetItemText(node)
			server = self.servers[name]
			servers.append({"name":server['name'], "type":server['type'], "specific_port":server['specific_port']})
			node = self.connection_tree.GetNextSibling(node)

		config['connections'] = connections
		config['servers'] = servers

		# save stash
		stash = []
		for i in xrange(0, self.list_stash.GetStore().GetCount()):
			stash.append({'name':self.list_stash.GetTextValue(i, 0), 'data':self.list_stash.GetTextValue(i, 1)})
		config['stash'] = stash

		try:
			DBG(json.dumps(config))
			file.truncate(0)
			file.seek(0, 0)
			file.write(json.dumps(config))
			file.close()
			return True
		except:
			DBG_TRACE()
			return False

	def close_app(self, event):
		DBG("close_app")
		DBG(event)

		self.save_status()

		all_done = True

		# close all connections
		node = self.nodes['connection']
		node = self.connection_tree.GetFirstChild(node)[0]
		while node.IsOk():
			name = self.connection_tree.GetItemText(node)
			node = self.connection_tree.GetNextSibling(node)
			if not self.close_node(name):
				all_done = False

		# close all servers
		node = self.nodes['server']
		node = self.connection_tree.GetFirstChild(node)[0]
		while node.IsOk():
			name = self.connection_tree.GetItemText(node)
			node = self.connection_tree.GetNextSibling(node)
			if not self.close_node(name):
				all_done = False

		# close command server
		try:
			query = {"name":'netool', "type":'netool', "op":"closeapp"}
			re = self.command_sender.sendto(json.dumps(query), self.command_server_address)
			DBG('sent %d' % re)
			data = self.command_sender.recv(4096)
			DBG("reply - %r" % data)
			data = json.loads(data)
			if data['result'] != 'ok':
				self.alert(base64.b64decode(data['msg']))
				all_done = False
		except:
			DBG_TRACE()
			self.alert(str(sys.exc_info()[1]))
			all_done = False

		if not all_done:
			DBG('not all_done')
			if wx.MessageDialog(None, 'Some connections are not shut down properly, still quit?', 'warning', wx.YES_NO | wx.ICON_QUESTION).ShowModal() == wx.ID_YES:
				pass
			else:
				return
		event.Skip()

	def on_node_changed(self, event):
		DBG('on_node_changed')
		try:
			name = self.connection_tree.GetItemText(self.connection_tree.GetSelection())
			if name == 'server' or name == 'connection':
				pass
			else:
				DBG(name)
				for i in range(0, self.connection_notebook.GetPageCount()):
					if self.connection_notebook.GetPageText(i) == name:
						self.connection_notebook.SetSelection(i)
		except:
			DBG_TRACE()
		event.Skip()

	def on_page_changed(self, event):
		DBG('on_page_changed')
		try:
			name = self.connection_notebook.GetPageText(self.connection_notebook.GetSelection())
			self.connection_tree.SelectItem(self.nodes[name])
		except:
			DBG_TRACE()
		event.Skip()

	def on_page_close(self, event):  # close from otherwhere
		DBG(event.GetSelection())
		name = self.connection_notebook.GetPageText(event.GetSelection())
		result = self.pages[name].on_close()
		self.connection_tree.Delete(self.nodes[name])
		del self.nodes[name]
		del self.pages[name]
		if result['result'] == 'ok':
			pass
		else:
			self.alert(base64.b64decode(result['error']))
		event.Skip()

	def delete_accepted_page(self, accepted_name):
		for i in range(0, self.connection_notebook.GetPageCount()):
			if accepted_name == self.connection_notebook.GetPageText(i):
				self.connection_notebook.DeletePage(i)
		self.connection_tree.Delete(self.nodes[accepted_name])
		del self.nodes[accepted_name]
		del self.pages[accepted_name]

	def alert(self, text):
		dlg = wx.MessageDialog(None, text, "!", wx.OK | wx.ICON_QUESTION)
		dlg.ShowModal()
		dlg.Destroy()

	def eat(self, data):
		DBG('eat')
		try:
			op = data['op']
			name = data['name']
			if op == 'recvdata':
				self.pages[data['name']].get_bytes(base64.b64decode(data['text']))
			elif op == 'disconnected':

				page = self.pages[name]
				if page.on_disconnect():
					DBG('close page')
					for i in range(0, self.connection_notebook.GetPageCount()):
						if name == self.connection_notebook.GetPageText(i):
							self.connection_notebook.DeletePage(i)
					self.connection_tree.Delete(self.nodes[name])

					del self.nodes[name]
					del self.pages[name]
				else:
					DBG('don\'t close page')
			elif op == 'error':
				if data['type'] == 'tcpserver':
					self.connection_tree.Delete(self.nodes[name])
					del self.nodes[name]
				else:
					page = self.pages[name]
					if page.on_disconnect():
						for i in range(0, self.connection_notebook.GetPageCount()):
							if name == self.connection_notebook.GetPageText(i):
								self.connection_notebook.DeletePage(i)
						self.connection_tree.Delete(self.nodes[name])

						del self.nodes[name]
						del self.pages[name]
				self.alert(base64.b64decode(data['msg']))
			elif op == 'accepted':
				server_node = self.nodes[name]
				node = self.connection_tree.AppendItem(server_node, data['accepted_name'])
				self.nodes[data['accepted_name']] = node
				page = AcceptedPage(parent = self.connection_notebook, mainframe = self, name = name, conn_type = 'tcpaccepted', command_sender = self.command_sender, command_server_address = COMMAND_SERVER_ADDRESS, accepted_name = data['accepted_name'])
				self.connection_notebook.AddPage(page, data['accepted_name'])
				index = self.connection_notebook.GetPageCount() - 1  # get the index of the final page.
				self.connection_notebook.SetSelection(index)
				self.pages[data['accepted_name']] = page

				page.make_accepted_page(data)

				self.connection_tree.ExpandAll()
		except:
			DBG_TRACE()


class ConnectionPage(ConnPage):

	def __init__(self, parent = None, mainframe = None, name = "unknown", conn_type = 'unknown', command_sender = None, command_server_address = COMMAND_SERVER_ADDRESS):
		ConnPage.__init__(self, parent)
		self.connected = False
		self.name = name
		self.mainframe = mainframe
		self.command_sender = command_sender
		self.radio_udp.SetValue(True)
		self.radio_random_port.SetValue(True)
		self.button_send.Disable()

		self.conn_type = conn_type
		self.command_server_address = command_server_address

		self.remote_ip.SetValue('192.168.0.100')
		self.remote_port.SetValue('22223')
		self.specific_port.SetValue('55556')
		self.recv_bytes = bytearray([])
		self.send_bytes = bytearray([])

		self.encoding_choices = ['ascii', 'utf-8', 'bytes-10', 'bytes-16', 'hex', 'utf-16', 'utf-32', 'gbk', 'gb2312']
		self.choice_send_encoding.Set(self.encoding_choices)
		self.choice_send_encoding.SetSelection(0)
		self.choice_recv_encoding.Set(self.encoding_choices)
		self.choice_recv_encoding.SetSelection(0)

		self.button_copy.Disable()

	def alert(self, text):
		dlg = wx.MessageDialog(None, text, "info", wx.YES_NO | wx.ICON_QUESTION)
		dlg.ShowModal()
		dlg.Destroy()

	def make_preview(self):
		try:
			method = self.encoding_choices[self.choice_send_encoding.GetCurrentSelection()]
			DBG(method)
			preview = ''
			bytes_after_encoding = bytearray()
			DBG(type(self.input_send.GetValue()))
			if method == 'bytes-10':
				for string in self.input_send.GetValue().strip().split():
					bytes_after_encoding += bytearray([int(string, 10)])
			elif method == 'bytes-16':
				for string in self.input_send.GetValue().strip().split():
					bytes_after_encoding += bytearray([int(string, 16)])
			else:
				bytes_after_encoding = bytearray(self.input_send.GetValue().encode(method))

			for b in bytes_after_encoding:
				preview += str.format('0x%02X ' % b)
			DBG(preview)
			self.send_bytes = bytes_after_encoding
			self.input_send_preview.SetValue(preview)
			self.text_encoding_result.SetLabelText('ok')
		except:
			self.input_send_preview.SetValue('')
			self.text_encoding_result.SetLabelText('error')
			DBG_TRACE()

	def make_recv_content(self):
		try:
			method = self.encoding_choices[self.choice_recv_encoding.GetCurrentSelection()]
			DBG(method)
			content = ''
			if method == 'bytes-10':
				for b in self.recv_bytes:
					content += str.format('%d ' % b)
			elif method == 'bytes-16':
				for b in self.recv_bytes:
					content += str.format('%02X ' % b)
			else:
				content = self.recv_bytes.decode(method)

			self.input_recv.SetValue(content)
			self.input_recv.ShowPosition(self.input_recv.GetLastPosition())
		except:
			self.input_recv.SetValue("help! help! help! Can't decode! Change the method!")
			DBG_TRACE()

	def make_recv_bytes_content(self):
		DBG('make_recv_bytes_content len = %d' % len(self.recv_bytes))
		try:
			content = ''
			for b in self.recv_bytes:
				content += str.format('0x%02X ' % b)
			self.input_recv_bytes.SetValue(content)
			self.input_recv_bytes.ShowPosition(self.input_recv_bytes.GetLastPosition())
		except:
			DBG_TRACE()

	def get_bytes(self, data):
		self.recv_bytes += data
		self.make_recv_bytes_content()
		self.make_recv_content()

	def on_change_send_encoding(self, event):
		self.make_preview()
		event.Skip()

	def on_change_recv_encoding(self, event):
		self.make_recv_content()
		event.Skip()

	def input_text_changed(self, event):
		self.make_preview()
		event.Skip()

	def on_button_clear(self, event):
		self.recv_bytes = bytearray()
		self.make_recv_bytes_content()
		self.make_recv_content()
		event.Skip()

	def on_close(self):
		if self.button_connect.GetLabelText() == "close":
			return self.do_prepare_connection()  # close socket
		else:
			return {'result':'ok'}

	def on_disconnect(self):
		self.radio_udp.Enable()
		self.radio_tcp.Enable()
		self.radio_http.Enable()
		self.remote_ip.Enable()
		self.remote_port.Enable()
		self.radio_random_port.Enable()
		self.radio_specific_port.Enable()
		self.specific_port.Enable()
		self.button_send.Disable()
		self.button_connect.SetLabelText("connect")
		return False

	def do_prepare_connection(self):
		DBG("do_prepare_connection")
		try:
			if self.button_connect.GetLabelText() == "connect":
				query = {"name":self.name, "type":self.conn_type, "op":"connect", "remote_ip":self.remote_ip.GetValue(),
						 "remote_port":int(self.remote_port.GetValue()), "random_port":self.radio_random_port.GetValue(), "specific_port":int(self.specific_port.GetValue())}
			else:
				query = {"name":self.name, "type":self.conn_type, "op":"disconnect"}

			re = self.command_sender.sendto(json.dumps(query), self.command_server_address)
			DBG('sent %d' % re)
			data = self.command_sender.recv(4096)
			DBG("do_prepare_connection get reply - %r" % data)
			data = json.loads(data)
			return data
		except:
			DBG_TRACE()
			return {'result':'error'}

	def on_button_connect(self, event):
		self.prepare_connection()
		event.Skip()

	def prepare_connection(self):
		DBG("prepare_connection")
		result = None
		if self.radio_udp.GetValue():
			self.conn_type = 'udpconn'
			result = self.do_prepare_connection()
		elif self.radio_tcp.GetValue():
			self.conn_type = 'tcpconn'
			result = self.do_prepare_connection()
		elif self.radio_http.GetValue():
			self.conn_type = 'httpconn'
			result = self.do_prepare_connection()
		if result['result'] == 'ok':
			if self.button_connect.GetLabelText() == "connect":
				self.radio_udp.Disable()
				self.radio_tcp.Disable()
				self.radio_http.Disable()
				self.remote_ip.Disable()
				self.remote_port.Disable()
				self.radio_random_port.Disable()
				self.radio_specific_port.Disable()
				self.specific_port.Disable()
				self.button_send.Enable()
				self.button_connect.SetLabelText("close")

				self.specific_port.SetValue(str(result['port']))
				self.connected = True
			else:
				self.radio_udp.Enable()
				self.radio_tcp.Enable()
				self.radio_http.Enable()
				self.remote_ip.Enable()
				self.remote_port.Enable()
				self.radio_random_port.Enable()
				self.radio_specific_port.Enable()
				self.specific_port.Enable()
				self.button_send.Disable()
				self.button_connect.SetLabelText("connect")
				self.connected = False
		else:
			self.alert(base64.b64decode(result['error']))
		DBG("prepare_connection result = %r" % result)

	def send_data(self, event):# send button clicked
		DBG("send_data")
		if self.text_encoding_result.GetLabelText() != 'ok':
			self.alert('encoding error')
			return
		try:
			query = {"name":self.name, "op":"senddata", 'data':base64.b64encode(self.send_bytes)}
			re = self.command_sender.sendto(json.dumps(query), self.command_server_address)
			DBG('sent %d' % re)
			data = self.command_sender.recv(4096)
			DBG("reply - %r" % data)
			if data == "ok":
				pass
			else:
				self.alert(data)
		except:
			DBG_TRACE()
			self.alert(str(sys.exc_info()[1]))
		event.Skip()


class AcceptedPage(ConnectionPage):
	def __init__(self, parent = None, mainframe = None, name = "unknown", conn_type = 'unknown', command_sender = None, command_server_address = COMMAND_SERVER_ADDRESS, accepted_name = 'accepted_name'):
		ConnectionPage.__init__(self, parent, mainframe, name, conn_type, command_sender, command_server_address)
		self.accepted_name = accepted_name
		self.connected = True
		DBG(self.command_sender)

	def make_accepted_page(self, data):
		self.button_connect.SetLabelText('close')
		self.remote_ip.SetLabelText(data['remote_ip'])
		self.remote_port.SetLabelText(str(data['remote_port']))
		self.specific_port.SetLabelText(str(data['local_port']))
		self.radio_specific_port.SetValue(True)
		if data['type'] == 'tcpserver':
			self.radio_tcp.SetValue(True)

		self.remote_ip.Disable()
		self.remote_port.Disable()
		self.specific_port.Disable()
		self.radio_specific_port.Disable()
		self.radio_tcp.Disable()
		self.radio_udp.Disable()
		self.radio_http.Disable()
		self.radio_random_port.Disable()
		self.button_send.Enable()

	def do_prepare_connection(self):
		DBG("AcceptedPage do_prepare_connection")
		try:
			data = None
			query = {"name":self.name, 'accepted_name':self.accepted_name, "type":self.conn_type, "op":"disconnect"}

			re = self.command_sender.sendto(json.dumps(query), self.command_server_address)
			DBG('sent %d' % re)
			data = self.command_sender.recv(4096)
			DBG("reply - %r" % data)
			data = json.loads(data)
			return data
		except:
			DBG_TRACE()
			return {'result':'error'}

	def prepare_connection(self):
		DBG("prepare_connection")
		result = None
		if self.accepted_name:
			result = self.do_prepare_connection()
		if result['result'] == 'ok':
			wx.CallAfter(self.mainframe.delete_accepted_page, self.accepted_name)
		else:
			self.alert(base64.b64decode(result['error']))
		DBG("prepare_connection result = %r" % result)
		event.Skip()

	def send_data(self, event):  # send button clicked
		DBG("send_data")
		if self.text_encoding_result.GetLabelText() != 'ok':
			self.alert('encoding error')
			return
		try:
			query = {"name":self.accepted_name, "op":"senddata", 'data':base64.b64encode(self.send_bytes)}
			re = self.command_sender.sendto(json.dumps(query), self.command_server_address)
			DBG('sent %d' % re)
			data = self.command_sender.recv(4096)
			DBG("reply - %r" % data)
			if data == "ok":
				pass
			else:
				self.alert(data)
		except:
			DBG_TRACE()
			self.alert(str(sys.exc_info()[1]))
		event.Skip()

	def on_disconnect(self):
		return True