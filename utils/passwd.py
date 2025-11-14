import base64
import hashlib
from binascii import Error

import rsa

from config import global_config

public_pem = b"""
-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBALPNGU54Ax0onD8lOkS0bV1IPyVeX64empGFyJgCK9TQ8jJDZU+DHwH6
os1uLHgel05Ci3coI5Neqqic/Z8lqwjQOee5SqX03O4pKJK25XFJCXJpWVyfGWsy
MeXYHTzyZI2+HdE8H0H3k0g3MhBLyPYSVlPNuU69tJ93ZgMNobJnAgMBAAE=
-----END RSA PUBLIC KEY-----
"""  # 公钥

private_pem = b"""
-----BEGIN RSA PRIVATE KEY-----
MIICYQIBAAKBgQCzzRlOeAMdKJw/JTpEtG1dSD8lXl+uHpqRhciYAivU0PIyQ2VP
gx8B+qLNbix4HpdOQot3KCOTXqqonP2fJasI0DnnuUql9NzuKSiStuVxSQlyaVlc
nxlrMjHl2B088mSNvh3RPB9B95NINzIQS8j2ElZTzblOvbSfd2YDDaGyZwIDAQAB
AoGAdAO/83jOkY71mmz79v7wnkMSs5r8Y85Nb96B+0tTWuNjk3kXMsHpTQ6a47DW
Mr+SY6XedYlJwzpPJbL+Dwq3rQu5rvjMenMCaupLaXCe6JCFKeiFOmOYRUh3kmoW
umZ6TaArnM/FuITL4M9jP9j+NIKk+cAQw6K9NSFgXAguKekCRQDS7uy23BZdXlMZ
cgwD45OPQrdStzRg5/J/NvgkxpqU3ZTVSleLmgII8PFYKQ6wZPkkMpHap4WcEk1u
XmQYKfSHM3lPgwI9ANo3ZACvyX/+/e8RNlRnI65X7RGoJkTjNkDekkVSIk8gGL9U
4N1kwuAcTdK06HE4uL+fFyQqo3ENLyWYTQJFALgO+onZ5L4Wh8bFaMyf8evpmJRZ
/x+sZkMx0TguAUdzTuMLWvcbLTlmHgMC2Kl9gpVedz1oPsNgiSaMwSUAvzqW5P1H
Ajxh/fnEbSw5dFKoJryVDnPxeL6W7UGyMa5NVyWsR4PssGcslHseMH9qkItKEb9I
CMa+Fj0YGqWmwNrpMQkCRQCJPErPjS/R+oNOyMlnqPMNm7TgBgQAZc4m95RVaf0F
SLWgfuipX8atSuKsitaxikgWZRa4lQprdx0Y3GPRJul+6XCAlw==
-----END RSA PRIVATE KEY-----
"""  # 私钥


def get_password_hash(password: str) -> str:
    """加密明文密码"""
    md5_dict = hashlib.md5()
    md5_dict.update((password + global_config["md5-salt"]).encode("utf-8"))
    return md5_dict.hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    """验证明文密码 与 加密后的密码 是否一致"""
    ciphertext = get_password_hash(password)
    print(ciphertext, hashed_password, password)
    return bool(ciphertext == hashed_password)


def generate_rsa_key():
    """生成公钥、私钥  - https://www.cnblogs.com/wangyingblock/p/15908056.html"""
    public_key, private_key = rsa.newkeys(1024)  # 生成公钥和私钥

    public = public_key.save_pkcs1()  # 转换格式
    private = private_key.save_pkcs1()  # 转换格式

    with open("../public.pem", mode="wb") as f:  # 存储
        f.write(public)
    with open("../private.pem", mode="wb") as f:  # 存储
        f.write(private)


def rsa_encrypt_password(plaintext):
    """rsa加密(base64转码) - https://www.cnblogs.com/wangyingblock/p/15908056.html"""
    return base64.b64encode(
        rsa.encrypt(plaintext.encode("utf-8"), rsa.PublicKey.load_pkcs1(public_pem))
    )


def rsa_decrypt_password(ciphertext):
    """rsa加密(base64解码) - https://www.cnblogs.com/wangyingblock/p/15908056.html"""
    return rsa.decrypt(
        base64.b64decode(ciphertext), rsa.PrivateKey.load_pkcs1(private_pem)
    ).decode("utf-8")


if __name__ == "__main__":
    # print(get_password_hash("123456"))

    generate_rsa_key()
    # encrypt = rsa_encrypt_password('123456')
    # print(encrypt)
    decrypt = rsa_decrypt_password(
        "PJtMtzjGp26JR9raXzGwLkgRRtCWg5zVQjOQQ10j70J/PuMXMriDLcbIAsIsx1thEMVsAA/GP3GOTGGEFOVMZzV8mlW5bXJw9kyWSuhNlCHax/1LEa+sggiOEoF5vZ+TQuiKqtaTqGm7G7Mj1lY4v859KpBKW1Utb9J7fOY7qUE="
    )
    print(decrypt)  # 使用之前必须先解码
