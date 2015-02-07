# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import sys
import wx.aui
import wx.dataview
import wx.richtext

wx.ID_ANYf = 1000

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Netool  V0.01  20150108 XC", pos = wx.DefaultPosition, size = wx.Size( 1080,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 960,500 ), wx.DefaultSize )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel9 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel11 = wx.Panel( self.m_panel9, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel11.SetMinSize( wx.Size( 200,-1 ) )
		self.m_panel11.SetMaxSize( wx.Size( 200,-1 ) )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.connection_tree = wx.TreeCtrl( self.m_panel11, wx.ID_ANYf, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		bSizer14.Add( self.connection_tree, 8, wx.ALL|wx.EXPAND, 2 )
		
		self.button_new_connection = wx.Button( self.m_panel11, wx.ID_ANY, u"New Connection", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.button_new_connection, 1, wx.ALL|wx.EXPAND, 2 )
		
		self.button_new_server = wx.Button( self.m_panel11, wx.ID_ANY, u"New Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.button_new_server, 1, wx.ALL|wx.EXPAND, 2 )
		
		self.button_option = wx.Button( self.m_panel11, wx.ID_ANY, u"Option", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_option.Enable( False )
		
		bSizer14.Add( self.button_option, 1, wx.ALL|wx.EXPAND, 2 )
		
		
		self.m_panel11.SetSizer( bSizer14 )
		self.m_panel11.Layout()
		bSizer14.Fit( self.m_panel11 )
		bSizer13.Add( self.m_panel11, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panel12 = wx.Panel( self.m_panel9, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel20 = wx.Panel( self.m_panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel20.SetMinSize( wx.Size( 620,-1 ) )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.connection_notebook = wx.aui.AuiNotebook( self.m_panel20, wx.ID_ANY, wx.DefaultPosition, wx.Size( 600,400 ), wx.aui.AUI_NB_DEFAULT_STYLE )
		
		bSizer18.Add( self.connection_notebook, 8, wx.EXPAND |wx.ALL, 2 )
		
		
		self.m_panel20.SetSizer( bSizer18 )
		self.m_panel20.Layout()
		bSizer18.Fit( self.m_panel20 )
		bSizer15.Add( self.m_panel20, 1, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel19 = wx.Panel( self.m_panel12, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.list_stash = wx.dataview.DataViewListCtrl( self.m_panel19, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		bSizer17.Add( self.list_stash, 1, wx.ALL|wx.EXPAND, 0 )
		
		
		self.m_panel19.SetSizer( bSizer17 )
		self.m_panel19.Layout()
		bSizer17.Fit( self.m_panel19 )
		bSizer15.Add( self.m_panel19, 2, wx.ALL|wx.EXPAND, 2 )
		
		
		self.m_panel12.SetSizer( bSizer15 )
		self.m_panel12.Layout()
		bSizer15.Fit( self.m_panel12 )
		bSizer13.Add( self.m_panel12, 4, wx.EXPAND |wx.ALL, 1 )
		
		
		self.m_panel9.SetSizer( bSizer13 )
		self.m_panel9.Layout()
		bSizer13.Fit( self.m_panel9 )
		bSizer12.Add( self.m_panel9, 15, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer12 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.close_app )
		self.connection_tree.Bind( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_item_right_click )
		self.connection_tree.Bind( wx.EVT_TREE_SEL_CHANGED, self.on_node_changed )
		self.button_new_connection.Bind( wx.EVT_BUTTON, self.new_connection )
		self.button_new_server.Bind( wx.EVT_BUTTON, self.new_server )
		self.connection_notebook.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_page_changed )
		self.connection_notebook.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_page_close )
		self.Bind( wx.dataview.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.on_stash_context_menu, id = wx.ID_ANY )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def close_app( self, event ):
		event.Skip()
	
	def on_item_right_click( self, event ):
		event.Skip()
	
	def on_node_changed( self, event ):
		event.Skip()
	
	def new_connection( self, event ):
		event.Skip()
	
	def new_server( self, event ):
		event.Skip()
	
	def on_page_changed( self, event ):
		event.Skip()
	
	def on_page_close( self, event ):
		event.Skip()
	
	def on_stash_context_menu( self, event ):
		event.Skip()
	

###########################################################################
## Class ConnPage
###########################################################################

class ConnPage ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 620,491 ), style = wx.TAB_TRAVERSAL )
		
		self.SetMinSize( wx.Size( 600,-1 ) )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel241 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer241 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel251 = wx.Panel( self.m_panel241, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer251 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel12 = wx.Panel( self.m_panel251, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_connect = wx.Button( self.m_panel12, wx.ID_ANY, u"connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.button_connect, 1, wx.ALL|wx.EXPAND, 0 )
		
		
		self.m_panel12.SetSizer( bSizer11 )
		self.m_panel12.Layout()
		bSizer11.Fit( self.m_panel12 )
		bSizer251.Add( self.m_panel12, 1, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel28 = wx.Panel( self.m_panel251, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel8 = wx.Panel( self.m_panel28, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"remote :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer8.Add( self.m_staticText2, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.remote_ip = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 162,-1 ), 0 )
		self.remote_ip.SetMaxSize( wx.Size( 162,-1 ) )
		
		bSizer8.Add( self.remote_ip, 0, wx.ALL|wx.EXPAND, 0 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel8, wx.ID_ANY, u":", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer8.Add( self.m_staticText4, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.remote_port = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )
		self.remote_port.SetMinSize( wx.Size( 46,-1 ) )
		self.remote_port.SetMaxSize( wx.Size( 46,-1 ) )
		
		bSizer8.Add( self.remote_port, 0, wx.ALL|wx.EXPAND, 0 )
		
		
		self.m_panel8.SetSizer( bSizer8 )
		self.m_panel8.Layout()
		bSizer8.Fit( self.m_panel8 )
		bSizer26.Add( self.m_panel8, 1, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel10 = wx.Panel( self.m_panel28, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel10, wx.ID_ANY, u"local port :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer9.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.radio_random_port = wx.RadioButton( self.m_panel10, wx.ID_ANY, u"random", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.radio_random_port, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.radio_specific_port = wx.RadioButton( self.m_panel10, wx.ID_ANY, u"specific :", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.radio_specific_port, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.specific_port = wx.TextCtrl( self.m_panel10, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 46,-1 ), wx.TE_RIGHT )
		self.specific_port.SetMinSize( wx.Size( 46,-1 ) )
		self.specific_port.SetMaxSize( wx.Size( 46,-1 ) )
		
		bSizer9.Add( self.specific_port, 0, wx.ALL|wx.EXPAND, 0 )
		
		
		self.m_panel10.SetSizer( bSizer9 )
		self.m_panel10.Layout()
		bSizer9.Fit( self.m_panel10 )
		bSizer26.Add( self.m_panel10, 1, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel11 = wx.Panel( self.m_panel28, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self.m_panel11, wx.ID_ANY, u"protocol :", wx.DefaultPosition, wx.Size( 63,-1 ), 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer10.Add( self.m_staticText5, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.radio_udp = wx.RadioButton( self.m_panel11, wx.ID_ANY, u"udp", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.radio_udp, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.radio_tcp = wx.RadioButton( self.m_panel11, wx.ID_ANY, u"tcp", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.radio_tcp, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.radio_http = wx.RadioButton( self.m_panel11, wx.ID_ANY, u"http", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.radio_http.Enable( False )
		
		bSizer10.Add( self.radio_http, 0, wx.ALL|wx.EXPAND, 4 )
		
		
		self.m_panel11.SetSizer( bSizer10 )
		self.m_panel11.Layout()
		bSizer10.Fit( self.m_panel11 )
		bSizer26.Add( self.m_panel11, 1, wx.EXPAND |wx.ALL, 2 )
		
		
		self.m_panel28.SetSizer( bSizer26 )
		self.m_panel28.Layout()
		bSizer26.Fit( self.m_panel28 )
		bSizer251.Add( self.m_panel28, 5, wx.EXPAND |wx.ALL, 2 )
		
		
		self.m_panel251.SetSizer( bSizer251 )
		self.m_panel251.Layout()
		bSizer251.Fit( self.m_panel251 )
		bSizer241.Add( self.m_panel251, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panel26 = wx.Panel( self.m_panel241, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer241.Add( self.m_panel26, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_panel241.SetSizer( bSizer241 )
		self.m_panel241.Layout()
		bSizer241.Fit( self.m_panel241 )
		bSizer6.Add( self.m_panel241, 1, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel231 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer231 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel6 = wx.Panel( self.m_panel231, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel9 = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.input_send_preview = wx.richtext.RichTextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.HSCROLL|wx.VSCROLL|wx.WANTS_CHARS )
		bSizer19.Add( self.input_send_preview, 4, wx.EXPAND |wx.ALL, 2 )
		
		self.input_send = wx.richtext.RichTextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.HSCROLL|wx.VSCROLL|wx.WANTS_CHARS )
		bSizer19.Add( self.input_send, 8, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel14 = wx.Panel( self.m_panel9, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel16 = wx.Panel( self.m_panel14, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_send = wx.Button( self.m_panel16, wx.ID_ANY, u"send", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.button_send, 0, wx.ALL|wx.EXPAND, 2 )
		
		self.m_panel161 = wx.Panel( self.m_panel16, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer24 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel24 = wx.Panel( self.m_panel161, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText10 = wx.StaticText( self.m_panel24, wx.ID_ANY, u"encode :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		bSizer25.Add( self.m_staticText10, 0, wx.ALL|wx.EXPAND, 5 )
		
		choice_send_encodingChoices = []
		self.choice_send_encoding = wx.Choice( self.m_panel24, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_send_encodingChoices, 0 )
		self.choice_send_encoding.SetSelection( 0 )
		self.choice_send_encoding.SetMaxSize( wx.Size( 80,-1 ) )
		
		bSizer25.Add( self.choice_send_encoding, 0, wx.ALL|wx.EXPAND, 2 )
		
		self.text_encoding_result = wx.StaticText( self.m_panel24, wx.ID_ANY, u"ok", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.text_encoding_result.Wrap( -1 )
		bSizer25.Add( self.text_encoding_result, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel24.SetSizer( bSizer25 )
		self.m_panel24.Layout()
		bSizer25.Fit( self.m_panel24 )
		bSizer24.Add( self.m_panel24, 0, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panel25 = wx.Panel( self.m_panel161, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer24.Add( self.m_panel25, 0, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_panel161.SetSizer( bSizer24 )
		self.m_panel161.Layout()
		bSizer24.Fit( self.m_panel161 )
		bSizer14.Add( self.m_panel161, 1, wx.EXPAND |wx.ALL, 2 )
		
		
		self.m_panel16.SetSizer( bSizer14 )
		self.m_panel16.Layout()
		bSizer14.Fit( self.m_panel16 )
		bSizer13.Add( self.m_panel16, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_panel14.SetSizer( bSizer13 )
		self.m_panel14.Layout()
		bSizer13.Fit( self.m_panel14 )
		bSizer19.Add( self.m_panel14, 1, wx.EXPAND |wx.ALL, 2 )
		
		
		self.m_panel9.SetSizer( bSizer19 )
		self.m_panel9.Layout()
		bSizer19.Fit( self.m_panel9 )
		bSizer7.Add( self.m_panel9, 15, wx.EXPAND |wx.ALL, 2 )
		
		
		self.m_panel6.SetSizer( bSizer7 )
		self.m_panel6.Layout()
		bSizer7.Fit( self.m_panel6 )
		bSizer231.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panel7 = wx.Panel( self.m_panel231, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel7.SetMinSize( wx.Size( 300,-1 ) )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel15 = wx.Panel( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.input_recv_bytes = wx.richtext.RichTextCtrl( self.m_panel15, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.HSCROLL|wx.VSCROLL|wx.WANTS_CHARS )
		bSizer15.Add( self.input_recv_bytes, 4, wx.EXPAND |wx.ALL, 2 )
		
		self.input_recv = wx.richtext.RichTextCtrl( self.m_panel15, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.VSCROLL|wx.WANTS_CHARS )
		bSizer15.Add( self.input_recv, 8, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel17 = wx.Panel( self.m_panel15, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_clear = wx.Button( self.m_panel17, wx.ID_ANY, u"clear", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer16.Add( self.button_clear, 0, wx.ALL|wx.EXPAND, 2 )
		
		self.button_copy = wx.Button( self.m_panel17, wx.ID_ANY, u"copy", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer16.Add( self.button_copy, 0, wx.ALL|wx.EXPAND, 2 )
		
		self.m_panel21 = wx.Panel( self.m_panel17, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer22 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel22 = wx.Panel( self.m_panel21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9 = wx.StaticText( self.m_panel22, wx.ID_ANY, u"decode :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer23.Add( self.m_staticText9, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 4 )
		
		choice_recv_encodingChoices = []
		self.choice_recv_encoding = wx.Choice( self.m_panel22, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_recv_encodingChoices, 0 )
		self.choice_recv_encoding.SetSelection( 0 )
		bSizer23.Add( self.choice_recv_encoding, 2, wx.ALL|wx.EXPAND, 2 )
		
		
		self.m_panel22.SetSizer( bSizer23 )
		self.m_panel22.Layout()
		bSizer23.Fit( self.m_panel22 )
		bSizer22.Add( self.m_panel22, 0, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panel23 = wx.Panel( self.m_panel21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer22.Add( self.m_panel23, 0, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_panel21.SetSizer( bSizer22 )
		self.m_panel21.Layout()
		bSizer22.Fit( self.m_panel21 )
		bSizer16.Add( self.m_panel21, 1, wx.EXPAND |wx.ALL, 2 )
		
		
		self.m_panel17.SetSizer( bSizer16 )
		self.m_panel17.Layout()
		bSizer16.Fit( self.m_panel17 )
		bSizer15.Add( self.m_panel17, 1, wx.EXPAND|wx.ALL, 2 )
		
		
		self.m_panel15.SetSizer( bSizer15 )
		self.m_panel15.Layout()
		bSizer15.Fit( self.m_panel15 )
		bSizer12.Add( self.m_panel15, 1, wx.EXPAND |wx.ALL, 2 )
		
		
		self.m_panel7.SetSizer( bSizer12 )
		self.m_panel7.Layout()
		bSizer12.Fit( self.m_panel7 )
		bSizer231.Add( self.m_panel7, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.m_panel231.SetSizer( bSizer231 )
		self.m_panel231.Layout()
		bSizer231.Fit( self.m_panel231 )
		bSizer6.Add( self.m_panel231, 5, wx.EXPAND |wx.ALL, 2 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		# Connect Events
		self.button_connect.Bind( wx.EVT_BUTTON, self.on_button_connect )
		self.input_send.Bind( wx.EVT_TEXT, self.input_text_changed )
		self.button_send.Bind( wx.EVT_BUTTON, self.send_data )
		self.choice_send_encoding.Bind( wx.EVT_CHOICE, self.on_change_send_encoding )
		self.button_clear.Bind( wx.EVT_BUTTON, self.on_button_clear )
		self.choice_recv_encoding.Bind( wx.EVT_CHOICE, self.on_change_recv_encoding )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_button_connect( self, event ):
		event.Skip()
	
	def input_text_changed( self, event ):
		event.Skip()
	
	def send_data( self, event ):
		event.Skip()
	
	def on_change_send_encoding( self, event ):
		event.Skip()
	
	def on_button_clear( self, event ):
		event.Skip()
	
	def on_change_recv_encoding( self, event ):
		event.Skip()
	

###########################################################################
## Class NewServerDialog
###########################################################################

class NewServerDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"New Server", pos = wx.DefaultPosition, size = wx.Size( 320,160 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer526 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel44 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer45 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.name = wx.StaticText( self.m_panel44, wx.ID_ANY, u"name :", wx.DefaultPosition, wx.Size( 63,-1 ), 0 )
		self.name.Wrap( -1 )
		bSizer45.Add( self.name, 0, wx.ALL, 4 )
		
		self.name = wx.TextCtrl( self.m_panel44, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 162,-1 ), 0 )
		bSizer45.Add( self.name, 0, wx.ALL|wx.EXPAND, 0 )
		
		
		self.m_panel44.SetSizer( bSizer45 )
		self.m_panel44.Layout()
		bSizer45.Fit( self.m_panel44 )
		bSizer526.Add( self.m_panel44, 0, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel10 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel10, wx.ID_ANY, u"local port :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer9.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.specific_port = wx.TextCtrl( self.m_panel10, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.specific_port.SetMaxSize( wx.Size( 60,-1 ) )
		
		bSizer9.Add( self.specific_port, 0, wx.ALL|wx.EXPAND, 0 )
		
		
		self.m_panel10.SetSizer( bSizer9 )
		self.m_panel10.Layout()
		bSizer9.Fit( self.m_panel10 )
		bSizer526.Add( self.m_panel10, 0, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel11 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self.m_panel11, wx.ID_ANY, u"protocol :", wx.DefaultPosition, wx.Size( 63,-1 ), 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer10.Add( self.m_staticText5, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.radio_udp = wx.RadioButton( self.m_panel11, wx.ID_ANY, u"udp", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.radio_udp, 0, wx.ALL|wx.EXPAND, 4 )
		
		self.radio_tcp = wx.RadioButton( self.m_panel11, wx.ID_ANY, u"tcp", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.radio_tcp, 0, wx.ALL|wx.EXPAND, 4 )
		
		
		self.m_panel11.SetSizer( bSizer10 )
		self.m_panel11.Layout()
		bSizer10.Fit( self.m_panel11 )
		bSizer526.Add( self.m_panel11, 0, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel45 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer46 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_ok = wx.Button( self.m_panel45, wx.ID_OK, u"ok", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.button_ok, 1, wx.ALL|wx.EXPAND, 2 )
		
		self.button_cancel = wx.Button( self.m_panel45, wx.ID_CANCEL, u"cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.button_cancel, 1, wx.ALL|wx.EXPAND, 2 )
		
		
		self.m_panel45.SetSizer( bSizer46 )
		self.m_panel45.Layout()
		bSizer46.Fit( self.m_panel45 )
		bSizer526.Add( self.m_panel45, 0, wx.EXPAND |wx.ALL, 2 )
		
		
		self.SetSizer( bSizer526 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_ok.Bind( wx.EVT_BUTTON, self.on_click_ok )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.on_click_cancel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_click_ok( self, event ):
		event.Skip()
	
	def on_click_cancel( self, event ):
		event.Skip()
	

###########################################################################
## Class StashDialog
###########################################################################

class StashDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Shortcut setting", pos = wx.DefaultPosition, size = wx.Size( 462,196 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer87 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel90 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer88 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText42 = wx.StaticText( self.m_panel90, wx.ID_ANY, u"Name :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		bSizer88.Add( self.m_staticText42, 0, wx.ALL|wx.EXPAND, 3 )
		
		self.input_name = wx.TextCtrl( self.m_panel90, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer88.Add( self.input_name, 1, wx.ALL|wx.EXPAND, 0 )
		
		
		self.m_panel90.SetSizer( bSizer88 )
		self.m_panel90.Layout()
		bSizer88.Fit( self.m_panel90 )
		bSizer87.Add( self.m_panel90, 1, wx.EXPAND |wx.ALL, 2 )
		
		self.m_panel91 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer90 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText43 = wx.StaticText( self.m_panel91, wx.ID_ANY, u"Data :", wx.DefaultPosition, wx.Size( 38,-1 ), 0 )
		self.m_staticText43.Wrap( -1 )
		bSizer90.Add( self.m_staticText43, 0, wx.ALL, 5 )
		
		self.input_data = wx.richtext.RichTextCtrl( self.m_panel91, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.HSCROLL|wx.VSCROLL|wx.WANTS_CHARS )
		bSizer90.Add( self.input_data, 1, wx.EXPAND |wx.ALL, 2 )
		
		
		self.m_panel91.SetSizer( bSizer90 )
		self.m_panel91.Layout()
		bSizer90.Fit( self.m_panel91 )
		bSizer87.Add( self.m_panel91, 4, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panel92 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer91 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel93 = wx.Panel( self.m_panel92, wx.ID_ANY, wx.DefaultPosition, wx.Size( 36,-1 ), wx.TAB_TRAVERSAL )
		bSizer91.Add( self.m_panel93, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_button19 = wx.Button( self.m_panel92, wx.ID_OK, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91.Add( self.m_button19, 1, wx.ALL|wx.EXPAND, 2 )
		
		self.m_button20 = wx.Button( self.m_panel92, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91.Add( self.m_button20, 1, wx.ALL|wx.EXPAND, 2 )
		
		
		self.m_panel92.SetSizer( bSizer91 )
		self.m_panel92.Layout()
		bSizer91.Fit( self.m_panel92 )
		bSizer87.Add( self.m_panel92, 1, wx.EXPAND |wx.ALL, 2 )
		
		
		self.SetSizer( bSizer87 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

