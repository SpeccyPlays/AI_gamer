import numpy as np
import win32gui, win32ui, win32con
import cv2

class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd : int

    # constructor
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        self.w += 150
        self.h += 150

    def get_screenshot(self):

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)

        cDC.BitBlt(
            (0, 0),
            (self.w, self.h),
            dcObj,
            (0, 0),
            win32con.SRCCOPY
        )

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype=np.uint8)
        img.shape = (self.h, self.w, 4)

        img = img[:, :, :3]

        success, png_data = cv2.imencode(".png", img)
        png_bytes = png_data.tobytes()

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return png_bytes

    def set_foreground_window(self):
        win32gui.SetForegroundWindow(self.hwnd)