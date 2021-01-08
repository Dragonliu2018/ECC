import base64
import binascii
from gmssl import sm2, func, sm22
#加密
def encrypt(data):
    """
    加密，这里私钥密钥固定
    """
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    sm2_crypt = sm2.CryptSM2(
        public_key=public_key, private_key=private_key)
    enc_data = sm2_crypt.encrypt(data)
    return enc_data
#解密
def decrypt(data):
    """
    解密，这里私钥密钥固定
    """
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    sm2_crypt = sm2.CryptSM2(
        public_key=public_key, private_key=private_key)
    dec_data = sm2_crypt.decrypt(data)
    return dec_data
#算法过程
def detail(message):
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

    sm2_crypt = sm22.CryptSM2(
        public_key=public_key, private_key=private_key)
    # str = input("please input message:")
    ret_message = ''#返回信息
    ret_message = ret_message + "<center><h5>加密过程</h5></center>" 
    str = message
    ret_message = ret_message + "<b>step1</b> 明文信息：" + str + "</br>\n"
    data = str.encode('utf-8')
  #  data = b'123ab'    #python对bytes类型的数据用带b前缀的单引号或双引号表示
    print("M = ",data.hex())
    ret_message = ret_message + "<b>step2</b> M = {}".format(data.hex()) + '</br>\n'
    enc_data,k,C1,x2,y2,t,C2,C3 = sm2_crypt.encrypt(data)

    print("------------------------加密过程-----------------------------")
    # ret_message = ret_message + "------------------------加密过程-----------------------------" + '</br>\n'
    print("产生随机数 k = ", k)
    ret_message = ret_message + "<b>step3</b> 产生随机数 k = {}".format(k) + '</br>\n'
    print("计算椭圆曲线上的点 C1 = kG = (%s, %s)" % (C1[0:sm2_crypt.para_len], C1[sm2_crypt.para_len:2 * sm2_crypt.para_len]))
    ret_message = ret_message + "<b>step4</b> 计算椭圆曲线上的点 C1 = kG = ({}, {})".format(C1[0:sm2_crypt.para_len], C1[sm2_crypt.para_len:2 * sm2_crypt.para_len]) + '</br>\n'
    print("计算椭圆曲线上的点 kPB = (x2,y2) = (%s, %s)" % (x2, y2))  #PB为接收方B的公开钥
    ret_message = ret_message + "<b>step5</b> 计算椭圆曲线上的点 kPB = (x2,y2) = ({}, {})".format(x2, y2) + '</br>\n'
    print("计算t = KDF(x2||y2,klen) = ", t)
    ret_message = ret_message + "<b>step6</b> 计算t = KDF(x2||y2,klen) = {}".format(t) + '</br>\n'
    print("计算C2 = M XOR t = ", C2)
    ret_message = ret_message + "<b>step7</b> 计算C2 = M XOR t = {}".format(C2) + '</br>\n'
    print("计算C3 = SM3(x2||M||y2) = ", C3)
    ret_message = ret_message + "<b>step8</b> 计算C3 = SM3(x2||M||y2) = {}".format(C3) + '</br>\n'
    print("输出密文C = C1||C2||C3 = ", bytes.fromhex('%s%s%s' % (C1, C2, C3)))
    ret_message = ret_message + "<b>step9</b> 输出密文C = C1||C2||C3 = {}".format(bytes.fromhex('%s%s%s' % (C1, C2, C3))) + '</br>\n'
    #print(b"enc_data:" )
    #print(enc_data)
    #print("enc_data:%s" % enc_data)
    #print("enc_data_base64:%s" % base64.b64encode(bytes.fromhex(enc_data)))
    dec_data, x2, y2, t, u, C3, M = sm2_crypt.decrypt(enc_data)

    print("\n\n------------------------解密过程-----------------------------")
    ret_message = ret_message + "</br><center><h5>解密过程</h5></center>"
    # ret_message = ret_message + "1. 密文："
    print("计算pk*C1 = (%s,%s)" % (x2 , y2))  #pk为接受方B的秘密钥
    ret_message = ret_message + "<b>step1</b> 计算pk*C1 = ({}{})".format(x2 , y2) + '</br>\n'
    print("计算t = KDF(x2||y2,klen) = ", t)
    ret_message = ret_message + "<b>step2</b> 计算t = KDF(x2||y2,klen) = {}".format(t) + '</br>\n'
    print("计算M' = C2 XOR t = " , M)
    ret_message = ret_message + "<b>step3</b> 计算M' = C2 XOR t = {}".format(M) + '</br>\n'
    print("计算u = SM3(x2||M'||y2) = ", u)
    ret_message = ret_message + "<b>step4</b> 计算u = SM3(x2||M'||y2) = {}".format(u) + '</br>\n'
    print("比较u和C3， C3 = ", C3)
    ret_message = ret_message + "<b>step5</b> 比较u和C3， C3 = {}".format(C3) + '</br>\n'
    if (u == C3):
        print("解密结果：%s"% M)
        ret_message = ret_message + "<b>step6</b> 解密结果：{}".format(M) + '</br>\n'
        ret_message = ret_message + "<b>step7</b> 解密明文：{}".format(bytes.fromhex(M).decode()) + '</br>\n'
    else:
        print("解密失败")
        ret_message = ret_message + "<b>step6</b> 解密失败" + '</br>\n'

    assert data == dec_data
    print(ret_message)
    return ret_message

def test_sm2():
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

    sm2_crypt = sm2.CryptSM2(
        public_key=public_key, private_key=private_key)
    data = b"123"    #python对bytes类型的数据用带b前缀的单引号或双引号表示
    print(data)
    enc_data = sm2_crypt.encrypt(data)
    print(b"enc_data:" )
    print(enc_data)
    #print("enc_data:%s" % enc_data)
    #print("enc_data_base64:%s" % base64.b64encode(bytes.fromhex(enc_data)))
    dec_data = sm2_crypt.decrypt(enc_data)
    print(b"dec_data:" )
    print(dec_data)
    assert data == dec_data

    print("-----------------test sign and verify---------------")
    random_hex_str = func.random_hex(sm2_crypt.para_len)
    sign = sm2_crypt.sign(data, random_hex_str)
    print('sign:%s' % sign)
    verify = sm2_crypt.verify(sign, data)
    print('verify:%s' % verify)
    assert verify