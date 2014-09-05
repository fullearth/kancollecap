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

        # bind
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_BUTTON, self.onClickShot, shotButton)

    def onKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.Close()

    def onClickShot(self, e):
        # todo:座標取得できていればSSをとり、できていなければ座標を取得してからSSをとる
        # とりあえずの実装
        camera = kc.KCCamera(self)
        camera.captureGameArea()
        print ("onclickshot")
        pass

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, -1, 'Main')
    frame.Show(True)
    app.MainLoop()

