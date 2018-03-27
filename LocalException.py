
class NormalException(Exception):
    def __init__(self,err = "常规错误"):
        Exception.__init__(self,err)
