# coding:utf-8
import datetime
import os

import cv2
import wx
import ImageGrab
import numpy as np


class KCCamera:
    def __init__(self, parent=None):
        self.parent = parent
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.snapShotDir = 'snapshot'
        self.recentImage = None

    def getScreenImage(self):
        # convert('RGB')とreshapeは明示的に書いているだけで書かなくても動く
        pilImage = ImageGrab.grab().convert('RGB')
        # pilをcv2(numpy)に変換
        srcimg = np.array(pilImage, dtype=np.uint8)
        # なくても動くどころかsize[0]とsize[1]を逆にしても動いたのでコメントアウト
        # srcimg.reshape((pilImage.size[1], pilImage.size[0], 3))
        # RGB to BGR
        srcimg = srcimg[:,:,::-1]
        return srcimg

    # src:srcimg -> x,y,w,h or None(or exception)
    def findGameArea(self, src):
        grayimg = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        # to binary 255 or else
        ret,imgBinary = cv2.threshold(grayimg, 254, 255, cv2.THRESH_BINARY)
        # 検出する画面を白に
        imgBinary = cv2.bitwise_not(imgBinary)
        # 頂点探索
        contours, ret = cv2.findContours(imgBinary, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
        self.x,self.y,self.width,self.height = (0,0,0,0)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # ゲーム画面の面積で判定。仕様上縦横-1
            if np.size(cnt) == 8 and area == 799 * 479:
                self.x,self.y,self.width,self.height = cv2.boundingRect(cnt)
                break
        if not (self.width == 0 or self.height == 0):
            self.recentImage = src[self.y:self.y+self.height, self.x:self.x+self.width]
        return (self.x,self.y,self.width,self.height)

    # todo:mainに移動,
    def showCaptureArea(self):
        THICKNESS = 2
        frame = wx.Frame(self.parent)
        frame.SetWindowStyle(wx.NO_BORDER | wx.FRAME_SHAPED | wx.STAY_ON_TOP)
        frame.SetSize(wx.Size(self.width+(THICKNESS*2), self.height+(THICKNESS*2)))
        frame.SetPosition(wx.Point(self.x-THICKNESS, self.y-THICKNESS))
        frame.SetBackgroundColour("red")
        borderRegion = wx.Region(0, 0, self.width+(THICKNESS*2), self.height+(THICKNESS*2))
        borderRegion.Subtract(THICKNESS,THICKNESS,self.width,self.height)
        frame.SetShape(borderRegion)
        frame.Show()

        frame.count = 0
        frame.timer = wx.Timer(frame, -1)
        def ontimer(e):
            # print (frame.count)
            frame.count += 1
            if frame.count >= 5:
                frame.Destroy()
        frame.timer.Start(100)
        frame.Bind(wx.EVT_TIMER, ontimer)

    # test
    # todo:毎回findgameareaしていたら重い
    # 検出していない判定と処理が雑
    def captureGameArea(self):
        img = self.getScreenImage()
        if self.width == 0 or self.height == 0:
            x,y,w,h = self.findGameArea(img)
            self.showCaptureArea()
            if w == 0 or h == 0:
                print ("cannot find game area")
                return False
        # self.showCaptureArea()
        # numpyは行列
        self.recentImage = img[self.y:self.y+self.height, self.x:self.x+self.width]
        self.saveImage(img[self.y:self.y+self.height, self.x:self.x+self.width])
        return True

    # とりあえず保存するファイル名とディレクトリは固定
    def saveImage(self, img):
        date = datetime.datetime.now()
        filename = "game" + date.strftime("%Y-%m-%d_%H%M%S_%f") + ".png"
        if not os.path.isdir(self.snapShotDir):
            os.mkdir(self.snapShotDir)
        subDir = date.strftime("%Y%m%d")
        if not os.path.isdir(self.snapShotDir + "/" + subDir):
            os.mkdir(self.snapShotDir + "/" + subDir)
        cv2.imwrite(self.snapShotDir + '/' + subDir + '/' + filename, img)

    def resizeImage(self, src, dstx, dsty):
        return cv2.resize(src, (dstx, dsty))

    def getStringFromImage(self, src):
        srcrgb = src[:,:,::-1]
        return srcrgb.tostring()

if __name__ == '__main__':
    camera = KCCamera()
    camera.captureGameArea()

