import requests
import hashlib
from .utils import to_bytes, make_sha1_hash
from .config import WxUrl
import logging


logger = logging.getLogger(__name__)


class WxClient(object):

    def __init__(self, app_id, secret):
        """ 初始化
        """
        self.app_id = app_id
        self.secret = secret
        self.wx_url = WxUrl()
    
    def configure_wx_server(
        self, token, signature,
        timestamp, nonce, echostr
    ):
        """
        配置微信服务器
        """
        args = [token, timestamp, nonce]
        args = sorted(args)
        text = ''.join(args)
        sha1_hash = make_sha1_hash(text)
        if sha1_hash == signature:
            return echostr
    
    def get_access_token(self):
        """ 获取微信接口access_token"""
        payloads = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.secret,
        }
        try:
            req = requests.get(self.wx_url.TOKEN_URL, params=payloads)
            if req.status_code == 200:
                return req.json()
        except Exception as e:
            logger.error(str(e))