import base64
import binascii
from gmssl import sm2, func

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