import bit_byte_bd


def adder(x:int,y:int,cin:int):
    cout = (x&y)|((x^y)&cin)
    sum_ = x^y^cin
    return [cout,sum_]

def adder8(x:list,y:list,cin:int):
    xval = x
    yval = y
    #预处理
    mE   = [[] for _ in range(8)]
    for e in reversed(range(8)):
        if e==7 :
            mE[7] = adder(xval[7],yval[7],cin)
        else :
            mE[e] = adder(xval[e],yval[e],mE[e+1][0])
    #汇处理
    ret  = [0,[0 for _ in range(8)]]
    for s in reversed(range(8)):
        if s==0 :
            ret[0] = mE[0][0]#cout
            ret[1][0] = mE[0][1]
        else :
            ret[1][s] = mE[s][1]#sumval
    return ret

def ivser(in_:list):#反数处理
        ret = [0 for _ in range(len(in_))]
        for i in range(len(in_)):
            ret[i] = 1 if (in_[i] == 0) else 0
        return ret

def cmper8(in_:bit_byte_bd.Byte):
    inval = in_()
    iv = ivser(inval[0][1:])
    iv = bit_byte_bd.Byte([1]+iv)
    _1 = bit_byte_bd.Byte([0,0,0,0,0,0,0,1])
    ret = adder8(iv,_1)
    return ret[1]

class NALU:#整数据算数逻辑单元
    def __init__(self) -> None:
        pass
    def __call__(self,xval:bit_byte_bd.Byte,yval:bit_byte_bd.Byte,code:list[int]) -> bit_byte_bd.Any:#length:4,4,8
        rxval = xval()
        ryval = yval()
        ch = code[0:4]
        cl = code[4:8]
        ret = [0 for _ in range(32)]
        #0000:0000 add;0001 sub;0010 inc;0011 dec
        #0001:0000 and;0001 or ;0010 xor;0011 not
        if ch == [0,0,0,0]:
            if cl == [0,0,0,0]:
                xhh = rxval[0];xhl = rxval[1];xlh = rxval[2];xll = rxval[3]
                yhh = ryval[0];yhl = ryval[1];ylh = ryval[2];yll = ryval[3]
                sll = adder8(xll,yll,0)
                slh = adder8(xlh,ylh,sll[0])
                shl = adder8(xhl,yhl,slh[0])
                shh = adder8(xhh,yhh,shl[0])
                cout = shh[0]
                ret = [cout,[shh[1],shl[1],slh[1],sll[1]]]
            elif cl == [0,0,0,1]:
                ret = []
                for r in rxval:
                    in_ = ivser(r)
                    ret.append(in_)
                ret[0][0] = 1
                xhh = ret[0];xhl = ret[1];xlh = ret[2];xll = ret[3]
                yhh = [0,0,0,0,0,0,0,0];yhl = [0,0,0,0,0,0,0,0];ylh = [0,0,0,0,0,0,0,0];yll = [0,0,0,0,0,0,0,1]
                sll = adder8(xll,yll,0)
                slh = adder8(xlh,ylh,sll[0])
                shl = adder8(xhl,yhl,slh[0])
                shh = adder8(xhh,yhh,shl[0])
                cout = shh[0]
                ret = [shh[1],shl[1],slh[1],sll[1]]
                xhh = rxval[0];xhl = rxval[1];xlh = rxval[2];xll = rxval[3]
                yhh = ret[0];yhl = ret[1];ylh = ret[2];yll = ret[3]
                sll = adder8(xll,yll,0)
                slh = adder8(xlh,ylh,sll[0])
                shl = adder8(xhl,yhl,slh[0])
                shh = adder8(xhh,yhh,shl[0])
                cout = shh[0]
                ret = [cout,[shh[1],shl[1],slh[1],sll[1]]]
                return ret
            elif cl == [0,0,1,0]:
                xhh = rxval[0];xhl = rxval[1];xlh = rxval[2];xll = rxval[3]
                yhh = [0,0,0,0,0,0,0,0];yhl = [0,0,0,0,0,0,0,0];ylh = [0,0,0,0,0,0,0,0];yll = [0,0,0,0,0,0,0,1]
                sll = adder8(xll,yll,1)
                slh = adder8(xlh,ylh,sll[0])
                shl = adder8(xhl,yhl,slh[0])
                shh = adder8(xhh,yhh,shl[0])
                cout = shh[0]
                ret = [cout,[shh[1],shl[1],slh[1],sll[1]]]
            elif cl == [0,0,1,1]:
                xhh = rxval[0];xhl = rxval[1];xlh = rxval[2];xll = rxval[3]
                yhh = [1,1,1,1,1,1,1,1];yhl = [1,1,1,1,1,1,1,1];ylh = [1,1,1,1,1,1,1,1];yll = [1,1,1,1,1,1,1,1]
                sll = adder8(xll,yll,1)
                slh = adder8(xlh,ylh,sll[0])
                shl = adder8(xhl,yhl,slh[0])
                shh = adder8(xhh,yhh,shl[0])
                cout = shh[0]
                ret = [cout,[shh[1],shl[1],slh[1],sll[1]]]
            else:
                raise "invalid code"
        elif ch == [0,0,0,1]:
            if cl == [0,0,0,0]:
                ret = [[0 for _ in range(8)] for _ in range(4)]
                for i1 in range(4):
                    for i2 in range(8):
                        ret[i1][i2] = rxval[i1][i2]&ryval[i1][i2]
            elif cl == [0,0,0,1]:
                ret = [[0 for _ in range(8)] for _ in range(4)]
                for i1 in range(4):
                    for i2 in range(8):
                        ret[i1][i2] = rxval[i1][i2]|ryval[i1][i2]
            elif cl == [0,0,1,0]:
                ret = [[0 for _ in range(8)] for _ in range(4)]
                for i1 in range(4):
                    for i2 in range(8):
                        ret[i1][i2] = rxval[i1][i2]^ryval[i1][i2]
            elif cl == [0,0,1,1]:
                ret = [[0 for _ in range(8)] for _ in range(4)]
                for i1 in range(4):
                    for i2 in range(8):
                        ret[i1][i2] = 0 if rxval[i1][i2] == 1 else 0
            else:
                raise "invalid code"
        else:
            raise "invalid code"
class FALU:#点数据算数逻辑单元
    ...

if __name__ == "__main__":
    a = bit_byte_bd.Byte([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    b = bit_byte_bd.Byte([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    alu = NALU()
    print(alu(a,a,[0,0,0,0,0,0,0,1]))