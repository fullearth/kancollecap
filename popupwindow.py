import wx

class PopupWindow(wx.Frame):
    def __init__(self, parent=None, id=-1, title=""):
        wx.Frame.__init__(self, parent=parent, id=id, title=title, style=wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT)
        self.parent = parent
        self.bitmap = None
        self.Centre()
        # キャプションなどのサイズ考慮
        # self.SetSize(wx.Size(800, 480))
        self.SetClientSize(wx.Size(800, 480))

        self.Bind(wx.EVT_LEFT_DOWN, self.onClick)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_PAINT, self.onPaint)

    def onClick(self, e):
        self.parent.popupWindow = None
        self.Close()

    def onKeyDown(self, e):
        self.parent.popupWindow = None
        self.Close()

    def onPaint(self, e):
        if self.bmp is None:
            return
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)
        pass

    def setBitmap(self, bmp):
        self.bmp = bmp

