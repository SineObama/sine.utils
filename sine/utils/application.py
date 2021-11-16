# encoding: UTF-8
from tqdm import tqdm
from threading import Lock
from config_file import ConfigFile
from .func import *

class PredictableProcessBar(tqdm):
    '''继承自tqdm进度条模块，对总体大小未知的进度进行近似估算，使进度条尽量平滑。
    使用简单的算法进行预测计算。'''
    loaded_size=0 # 已知的总大小
    loaded_total=0 # 已知的总进度数，对应tqdm.total
    loaded_avg=0 # 已知的平均大小
    updated_size=0 # 已完成进度的大小
    updated_time=0 # 已完成进度的消耗时间(秒)由调用方给出
    origin_n=0 # 已完成的进度数，顶替tqdm.n的值，动态调整tqdm.n使其平滑
    lock=Lock() # 并发锁
    total_error=0.00001 # 进度完成时的判断误差（比值）
    def __init__(self, *args, **kw):
        if 'bar_format' not in kw:
            # 默认避免n进度小数点太多
            kw['bar_format'] = '{l_bar}{bar}| {n:.2f}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
        tqdm.__init__(self, *args, **kw)
    def load_in(self, size, total=1):
        '''载入已知的进度size大小，对应的total进度数默认为1'''
        self.lock.acquire()
        self.loaded_size = self.loaded_size + size
        self.loaded_total = self.loaded_total + total
        self.lock.release()
    def update_out(self, size, total=1, updated_time=0):
        '''完成size大小的进度，对应的total进度数默认为1，消耗updated_time秒'''
        self.lock.acquire()
        self.updated_size = self.updated_size + size
        self.origin_n = self.origin_n + total
        self.updated_time = self.updated_time + updated_time
        if self.loaded_total == 0:
            self.update(total)
        elif abs(self.origin_n - self.total) <= self.total * self.total_error:
            self.update((self.total - self.n))
        else:
            self.loaded_avg = avg = self.loaded_size / self.loaded_total
            self.update(size / avg / (self.total - self.origin_n + size / avg) * (self.total - self.n))
        self.lock.release()

class ConfigFileAlone(ConfigFile):
    '''继承自config-file，简单且便利的配置文件读取、保存。
    主要场景：
    1.文件不存在时创建。
    2.获取配置时指定默认值，不存在则同时完成设置。
    3.保存配置到文件（仅在配置有修改时）'''
    changed=False # 配置是否有修改
    def __init__(self, file_path):
        if isinstance(file_path, str) and not os.path.exists(file_path):
            mkdir(os.path.dirname(os.path.abspath(file_path)))
            with open(file_path, 'w') as file:
                file.write('{}')
        ConfigFile.__init__(self, file_path)
    def getAlone(self, key, default=None):
        if default != None and not self.has(key):
            self.changed = True
            self.set(key, default)
            return default
        return self.get(key)
    def setAlone(self, key, val):
        old_val = self.get(key)
        if old_val == val:
            return
        self.changed = True
        self.set(key, val)
    def saveAlone(self, *args, **kw):
        if self.changed:
            self.changed = False
            self.save(*args, **kw)

__all__ = ['PredictableProcessBar', 'ConfigFileAlone']
