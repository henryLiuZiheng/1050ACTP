import time

from PyQt5.QtCore import QThread, pyqtSignal


class WorkThread(QThread):
    # 使用信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    finishSignal = pyqtSignal(str)

    # 带参数示例
    def __init__(self, ip, port, parent=None):
        super(WorkThread, self).__init__(parent)

        self.ip = ip
        self.port = port

    def run(self):
        '''
        重写
        '''

        print('=============sleep======ip: {}, port: {}'.format(self.ip, self.port))
        time.sleep(20)

        self.finishSignal.emit('This is a test.')
        return