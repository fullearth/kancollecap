# coding:utf-8

import cv2
import ImageGrab
import numpy as np


class KCCamera:
    def __init__(self):
        pass

    def getScreenImage(self):
        pilImage = ImageGrab.grab().convert('RGB')
        # pilをcv2(numpy)に変換
        srcimg = np.array(pilImage, dtype=np.uint8)
        srcimg.reshape((pilImage.size[0], pilImage.size[1], 3))
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
        x,y,w,h = (0,0,0,0)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # ゲーム画面の面積で判定。仕様上縦横-1
            if np.size(cnt) == 8 and area == 799 * 479:
                x,y,w,h = cv2.boundingRect(cnt)
                break
        return (x,y,w,h)

    # test
    # todo:毎回findgameareaしていたら重い
    # 検出していない判定と処理が雑
    def captureGameArea(self):
        img = self.getScreenImage()
        x,y,w,h = self.findGameArea(img)
        if w == 0:
            print ("cannot find game area")
            return
        cv2.imwrite('game.png', img[y:y+h, x:x+w])

if __name__ == '__main__':
    camera = KCCamera()
    camera.captureGameArea()

