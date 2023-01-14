import logging
from time import time
from typing import Dict, Any

import aiohttp
import jsons

from plugp100.domain.tapo_exception import TapoException
from plugp100.tapo_protocol.encryption import helpers
from plugp100.tapo_protocol.encryption.key_pair import KeyPair
from plugp100.tapo_protocol.encryption.tp_link_cipher import TpLinkCipher, TpLinkCipherCryptography
from plugp100.tapo_protocol.methods import taporequest, SecurePassthroughMethod, HandshakeMethod, LoginDeviceMethod
from plugp100.tapo_protocol.methods.set_device_info_method import SetDeviceInfoMethod
from plugp100.tapo_protocol.params import DeviceInfoParams, HandshakeParams, LoginDeviceParams
from plugp100.utils.http_client import AsyncHttp

logger = logging.getLogger(__name__)


class TapoProtocolClient:

    def __init__(self, address: str, username: str, password: str, session: aiohttp.ClientSession = None):
        self.username = username
        self.password = password
        self.url = f"http://{address}/app"
        self.http = AsyncHttp(aiohttp.ClientSession() if session is None else session)
        self.key_pair: KeyPair = None
        self.tp_link_cipher: TpLinkCipher = None
        self.cookie_token: str = ""
        self.token: str = ""

        logger.debug(f"Device url is: {self.url}")

    async def login(self):
        await self._handshake()
        await self._login_request(self.username, self.password)

    async def set_device_state(self, state: DeviceInfoParams, terminal_uuid: str) -> Dict[str, Any]:
        device_info_method = SetDeviceInfoMethod(state.as_dict())
        device_info_method.set_request_time_milis(time())
        device_info_method.set_terminal_uuid(terminal_uuid)
        logger.debug(f"Device info method: {jsons.dumps(device_info_method)}")
        return await self.send_tapo_request(device_info_method)

    async def send_tapo_request(self, method: taporequest.TapoRequest) -> Dict[str, Any]:
        logger.debug(f"Method request: {jsons.dumps(method)}")
        dim_encrypted = self.tp_link_cipher.encrypt(jsons.dumps(method))
        logger.debug(f"Method request encrypted: {dim_encrypted}")

        secure_passthrough_method = SecurePassthroughMethod(dim_encrypted)
        logger.debug(f"Secure passthrough method: {secure_passthrough_method}")
        request_body = jsons.loads(jsons.dumps(secure_passthrough_method))
        logger.debug(f"Request body: {request_body}")

        response = await self.http.async_make_post_cookie(f"{self.url}?token={self.token}", request_body,
                                                          {'TP_SESSIONID': self.cookie_token})
        resp_dict: dict = await response.json(content_type=None)
        logger.debug(f"Device responded with: {resp_dict}")

        self._validate_response(resp_dict)

        decrypted_inner_response = jsons.loads(
            self.tp_link_cipher.decrypt(
                resp_dict['result']['response']
            ))
        logger.debug(f"Device inner response: {decrypted_inner_response}")
        self._validate_response(decrypted_inner_response)

        return decrypted_inner_response['result'] if 'result' in decrypted_inner_response else {}

    async def _handshake(self):
        logger.debug("Will perform handshaking...")

        logger.debug("Generating keypair")
        self.key_pair = KeyPair.create_key_pair()

        handshake_params = HandshakeParams(self.key_pair.get_public_key())
        logger.debug(f"Handshake params: {jsons.dumps(handshake_params)}")

        handshake_method = HandshakeMethod(handshake_params)
        logger.debug(f"Handshake method: {jsons.dumps(handshake_method)}")

        request_body = jsons.dump(handshake_method)
        logger.debug(f"Request body: {request_body}")

        response = await self.http.async_make_post(self.url, json=request_body)
        resp_dict = await response.json(content_type=None)
        logger.debug(f"Device responded with: {resp_dict}")
        self._validate_response(resp_dict)
        self.cookie_token = response.cookies.get('TP_SESSIONID').value
        logger.debug(f"Got TP_SESSIONID token: ...{self.cookie_token[5:]}")

        logger.debug("Decoding handshake key...")
        handshake_key = resp_dict['result']['key']
        self.tp_link_cipher = TpLinkCipherCryptography.create_from_keypair(handshake_key, self.key_pair)

    async def _login_request(self, username: str, password: str):
        logger.debug(f"Will login using username '{username[5:]}...'")
        digest_username = helpers.sha1(username)
        logger.debug(f"Username digest: ...{digest_username[:5]}")

        login_device_params = LoginDeviceParams(
            helpers.base64encode(password),
            helpers.base64encode(digest_username)
        )

        l_ldp = jsons.dumps(login_device_params).replace(helpers.base64encode(password), "PASSWORD_REMOVED")
        logger.debug(f"Login device params: {l_ldp}")

        login_device_method = LoginDeviceMethod(login_device_params)
        login_device_method.set_request_time_milis(time())
        l_ldm = jsons.dumps(login_device_method).replace(helpers.base64encode(password), "PASSWORD_REMOVED")
        logger.debug(f"Login device method: {l_ldm}")

        ldm_encrypted = self.tp_link_cipher.encrypt(jsons.dumps(login_device_method))
        logger.debug(f"Login device method encrypted: {ldm_encrypted}")

        secure_passthrough_method = SecurePassthroughMethod(ldm_encrypted)
        logger.debug(f"Secure passthrough method: {jsons.dumps(secure_passthrough_method)}")
        request_body = jsons.loads(jsons.dumps(secure_passthrough_method))
        logger.debug(f"Request body: {request_body}")

        response = await self.http.async_make_post_cookie(self.url, request_body,
                                                          {'TP_SESSIONID': self.cookie_token})
        resp_dict: dict = await response.json(content_type=None)
        logger.debug(f"Device responded with: {resp_dict}")

        self._validate_response(resp_dict)

        decrypted_inner_response = jsons.loads(
            self.tp_link_cipher.decrypt(
                resp_dict['result']['response']
            )
        )

        logger.debug(f"Device inner response: {decrypted_inner_response}")

        self._validate_response(decrypted_inner_response)
        self.token = decrypted_inner_response['result']['token']

    def _validate_response(self, resp: dict):
        if 'error_code' not in resp:
            logger.warning("No error_code in the response!")
        else:
            if resp['error_code'] != 0:
                raise TapoException.from_error_code(resp['error_code'])
