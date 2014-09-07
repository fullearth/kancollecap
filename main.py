# coding:utf-8

import wx

import kccamera as kc

class MainFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title="no title"):
        wx.Frame.__init__(self,
                          parent=parent,
                          id=id,
                          title=title,
                          style=wx.CAPTION | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          size=wx.Size(160, 160))
        self.viewWindow = None
        self.camera = kc.KCCamera(self)
        # todo:self
        shotButton = wx.Button(self, -1, "SHOT")
        showConfigChk = wx.CheckBox(self, -1, "config")
        # todo:SSを取るためのオブジェクト
        # sizer
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(shotButton, flag=wx.GROW, proportion=1)
        layout.Add(showConfigChk, flag=wx.BOTTOM)
        self.SetSizer(layout)

        style = self.GetWindowStyle()
        self.SetWindowStyle(style | wx.STAY_ON_TOP)

        self.viewWindow = self.createViewWindow()
        self.adjustViewWindow()
        self.viewWindow.Show(True)

        # bind
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_BUTTON, self.onClickShot, shotButton)
        self.Bind(wx.EVT_MOVE, self.onMove)
        self.Bind(wx.EVT_ICONIZE, self.onIconize)

    def onKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.Close()

    def onClickShot(self, e):
        # todo:座標取得できていればSSをとり、できていなければ座標を取得してからSSをとる
        # とりあえずの実装
        self.camera.captureGameArea()
        self.viewWindow.Refresh()
        print ("onclickshot")

    def onMove(self, e):
        self.adjustViewWindow()

    def onIconize(self, e):
        if e.Iconized():
            self.viewWindow.Show(False)
        else:
            self.viewWindow.Show(True)

    def createViewWindow(self):
        prewindow = wx.Frame(self, -1)
        prewindow.SetWindowStyle(wx.NO_BORDER | wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW)
        prewindow.Bind(wx.EVT_PAINT, self.onViewPaint)
        # todo:add and bind onclick event for large window
        return prewindow

    def adjustViewWindow(self):
        if self.viewWindow is None:
            return
        # todo:メインウィンドウがsizableになるまで数値直打ち
        mainPos = self.GetPosition()
        mainSize = self.GetSize()
        self.viewWindow.SetSize(wx.Size(mainSize.width, 96))
        self.viewWindow.SetPosition(wx.Point(mainPos.x, mainPos.y + mainSize.height))

    def onViewPaint(self, e):
        dc = wx.PaintDC(self.viewWindow)
        if self.camera.recentImage is None:
            dc.Clear()
            dc.SetPen(wx.Pen(wx.Colour(50, 50, 50), style=wx.DOT))
            dc.SetBrush(wx.Brush(self.viewWindow.GetBackgroundColour()))
            w, h = dc.GetSize()
            dc.DrawRectangle(w/8, h/8, w*3/4, h*3/4)
            dc.DrawCircle(w/2,h/2,h/8)
            return
        # opencv(numpy) into wx.Image
        size = self.viewWindow.GetSize()
        viewImage = wx.EmptyImage(size.width, size.height)
        viewImage.SetData(self.camera.getStringFromImage(self.camera.resizeImage(self.camera.recentImage, size.width, size.height)))
        # wx.Image into bitmap
        bmp = viewImage.ConvertToBitmap()
        dc.DrawBitmap(bmp, 0, 0)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, -1, 'Main')
    frame.Show(True)
    app.MainLoop()

