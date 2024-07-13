from typing import Any


class Bit:
    def __init__(self,val:bool) -> None:
        self.__val = val
    
    def __call__(self) -> Any:
        return self.__val
    
    def __sizeof__(self) -> int:
        return 1

class Byte:
    def __init__(self,vals:list[bool]) -> None:
        #这里应该在列表头处补0对其的，但懒得写，所以这里vals长度必须是8的倍数，即使非8倍数第18行也不会报错
        if len(vals) % 8 != 0:raise SyntaxError("无效值vals")
        self.__vals = [vals[x:x+8] for x in range(0,len(vals),8)]
    
    def __call__(self) -> Any:
        return self.__vals
    
    def __sizeof__(self) -> int:
        return 8*len(self.__vals)

if __name__ == "__main__":
    b = Byte([1,2,3,4,5,6,7,8])
    print(b())
        
    