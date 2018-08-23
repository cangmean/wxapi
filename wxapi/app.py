import requests
import hashlib
import logging

from .utils import to_bytes, make_sha1_hash
from .urls import WXUrl
from .errors import ParamError


logger = logging.getLogger(__name__)


class WXApi(object):

    def __init__(self, app_id, secret):
        """ 初始化
        """
        self.app_id = app_id
        self.secret = secret
    
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
            res = requests.get(WXUrl.TOKEN_URL, params=payloads)
            if res.status_code == 200:
                return res.json()
        except Exception as e:
            logger.error(str(e))
    
    def _make_qrcode_payloads(self, scene_id=None, scene_str=None, expires=None):
        """ 二维码负载"""
        if scene_id and expires:
            action_name = 'QR_SCENE'
        elif scene_str and expires:
            action_name = 'QR_STR_SCENE'
        elif scene_id and not expires:
            action_name = 'QR_LIMIT_SCENE'
        elif scene_str and not expires:
            action_name = 'QR_LIMIT_STR_SCENE'
        else:
            action_name = None
        
        if not action_name:
            raise ParamError('scene_id 或 scene_str 不能为空')
        
        payloads = {
            'action_name': action_name,
            'action_info': {'scene': {}}
        }
        scene = payloads['action_info']['scene']

        if 'LIMIT' in action_name:
            payloads['expire_second'] = expires
        
        if 'STR' in action_name:
            scene['scene_str'] = scene_str
        else:
            scene['scene_id'] = scene_id
        
        return payloads
    
    def make_qrcode(self, token, **kwargs):
        """ 生成二维码
        """
        payloads = self._make_qrcode_payloads(**kwargs)
        res = requests.post(WXUrl.QRCODE_URL.format(token), json=payloads)
        if res.status_code == 200:
            return res.json()
