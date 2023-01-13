from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from shareplum import Office365
from ...exceptions import BadSharepointAuth as SpErr
import io, requests


class SharePoint():
    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password
        self.auth_cookie = None


    # login: Login to sharepoiknt
    def login(self, path) -> requests.cookies.RequestsCookieJar:
        try:
            authcookie = Office365(path, username=self.__username, password=self.__password).GetCookies()
        except Exception:
            raise SpErr(self.__username, self.__password, path)
        else:
            self.auth_cookie = authcookie
            return authcookie


    # access_file(path): Sharepoint authentication to access 'path'
    def access_file(self, path: str) -> ClientContext:
        ctx_auth = AuthenticationContext(path)
        if (ctx_auth.acquire_token_for_user(self.__username, self.__password)):
            ctx = ClientContext(path, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()
            return ctx
            print("Authentication successful")
        else:
            raise SpErr(self.__username, self.__password, path)


    # retrive_file_bytes(ctx, file_path): Retrives the file at 'path' from 'ctx'
    def retrieve_file_bytes(self, ctx: ClientContext, path: str) -> io.BytesIO:
        response = File.open_binary(ctx, path)
        bytes_file_obj = io.BytesIO()
        bytes_file_obj.write(response.content)
        bytes_file_obj.seek(0)
        return bytes_file_obj


    # open_file_bytes(path): Opens the file at 'path' as bytes
    def open_file_bytes(self, path: str) -> io.BytesIO:
        ctx = self.access_file(path)
        return self.retrieve_file_bytes(ctx, path)
