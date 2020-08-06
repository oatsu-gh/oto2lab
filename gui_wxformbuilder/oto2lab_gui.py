# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"oto2lab (wxPython GUI version)", pos = wx.DefaultPosition, size = wx.Size( 720,460 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 640,460 ), wx.Size( 1200,640 ) )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"\n1. 変換したいファイル または 変換したいファイルがあるフォルダ を指定してください。\n2. 「変換する」 のボタンを押してください。\n", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		self.m_staticText7.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		bSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"フォルダ指定で変換" ), wx.VERTICAL )

		self.m_dirPicker1 = wx.DirPickerCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"変換したいファイルがあるフォルダを指定", wx.DefaultPosition, wx.Size( -1,-1 ), wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST )
		self.m_dirPicker1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_dirPicker1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		sbSizer2.Add( self.m_dirPicker1, 0, wx.ALL|wx.EXPAND, 5 )

		m_modeSelect1Choices = [ u"ini to lab", u"lab to ini", u"ust to ini" ]
		self.m_modeSelect1 = wx.RadioBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"機能選択", wx.DefaultPosition, wx.DefaultSize, m_modeSelect1Choices, 3, wx.RA_SPECIFY_ROWS )
		self.m_modeSelect1.SetSelection( 0 )
		self.m_modeSelect1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_modeSelect1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_modeSelect1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		sbSizer2.Add( self.m_modeSelect1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_displayConsole1 = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"コマンドライン出力を表示", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_displayConsole1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_displayConsole1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		sbSizer2.Add( self.m_displayConsole1, 0, wx.ALL, 5 )


		sbSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_convertButton1 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"変換する", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_convertButton1.SetFont( wx.Font( 9, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "ＭＳ Ｐゴシック" ) )
		self.m_convertButton1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.m_convertButton1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )

		sbSizer2.Add( self.m_convertButton1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_gauge1 = wx.Gauge( sbSizer2.GetStaticBox(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge1.SetValue( 0 )
		self.m_gauge1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		sbSizer2.Add( self.m_gauge1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer2.Add( sbSizer2, 1, wx.ALL|wx.EXPAND, 5 )

		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"ファイル指定で変換" ), wx.VERTICAL )

		self.m_filePicker1 = wx.FilePickerCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"入力ファイル選択", u"*.ust, *.ini, *.lab, *.svp", wx.DefaultPosition, wx.Size( -1,-1 ), wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST )
		self.m_filePicker1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		sbSizer3.Add( self.m_filePicker1, 0, wx.ALL|wx.EXPAND, 5 )

		m_modeSelect2Choices = [ u"ini to lab", u"lab to ini", u"ust to ini", u"svp to ini" ]
		self.m_modeSelect2 = wx.RadioBox( sbSizer3.GetStaticBox(), wx.ID_ANY, u"機能選択", wx.DefaultPosition, wx.DefaultSize, m_modeSelect2Choices, 4, wx.RA_SPECIFY_ROWS )
		self.m_modeSelect2.SetSelection( 0 )
		sbSizer3.Add( self.m_modeSelect2, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_displayConsole2 = wx.CheckBox( sbSizer3.GetStaticBox(), wx.ID_ANY, u"コマンドライン出力を表示", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_displayConsole2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		sbSizer3.Add( self.m_displayConsole2, 0, wx.ALL, 5 )


		sbSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_convertButton2 = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"変換する", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_convertButton2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )

		sbSizer3.Add( self.m_convertButton2, 0, wx.ALL, 5 )

		self.m_gauge2 = wx.Gauge( sbSizer3.GetStaticBox(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge2.SetValue( 0 )
		sbSizer3.Add( self.m_gauge2, 0, wx.ALL, 5 )


		bSizer2.Add( sbSizer3, 1, wx.EXPAND|wx.ALL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"\n© 2020 oatsu\n© 1998-2005 Julian Smart, Robert Roebling et al\n© 2001-2020 Python Software Foundation", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		self.m_staticText8.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
		self.m_staticText8.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer1.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_dirPicker1.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker1OnDirChanged )
		self.m_modeSelect1.Bind( wx.EVT_RADIOBOX, self.m_modeSelect1OnRadioBox )
		self.m_displayConsole1.Bind( wx.EVT_CHECKBOX, self.m_displayConsole1OnCheckBox )
		self.m_convertButton1.Bind( wx.EVT_BUTTON, self.m_convertButton1OnButtonClick )
		self.m_filePicker1.Bind( wx.EVT_FILEPICKER_CHANGED, self.m_filePicker1OnFileChanged )
		self.m_modeSelect2.Bind( wx.EVT_RADIOBOX, self.m_modeSelect2OnRadioBox )
		self.m_displayConsole2.Bind( wx.EVT_CHECKBOX, self.m_displayConsole2OnCheckBox )
		self.m_convertButton2.Bind( wx.EVT_BUTTON, self.m_convertButton2OnButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def m_dirPicker1OnDirChanged( self, event ):
		event.Skip()

	def m_modeSelect1OnRadioBox( self, event ):
		event.Skip()

	def m_displayConsole1OnCheckBox( self, event ):
		event.Skip()

	def m_convertButton1OnButtonClick( self, event ):
		event.Skip()

	def m_filePicker1OnFileChanged( self, event ):
		event.Skip()

	def m_modeSelect2OnRadioBox( self, event ):
		event.Skip()

	def m_displayConsole2OnCheckBox( self, event ):
		event.Skip()

	def m_convertButton2OnButtonClick( self, event ):
		event.Skip()


