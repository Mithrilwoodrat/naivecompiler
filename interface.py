# -*- coding: utf-8 -*-
import ctypes
class LibNaiveScript(object):
    def __init__(self, libpath):
        self.libpath = libpath
        self.__loadLib(libpath)

    def __loadLib(self, libpath):
        self.lib = ctypes.cdll.LoadLibrary(libpath)

    def InitCompiler(self):
        self.lib.InitCompiler()

    def LoadData(self, data_path):
        self.lib.LoadData(data_path)

    def Compile(self, output_path):
        self.lib.Compile(output_path)
