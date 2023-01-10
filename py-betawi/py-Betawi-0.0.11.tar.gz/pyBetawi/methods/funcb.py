from geezlibs.types import CallbackQuery, Message


class FuncBot(object):
    async def approve_pmpermit(
        self,
        cb,
        user_ids,
        OLD_MSG,
    ):
        from ..dB.pmpermit_db import approve_user, is_approved

        
        if isinstance(cb, CallbackQuery):
            if is_approved(user_ids):
                await cb.answer("Pengguna Ini Sudah Ada Di Database.", show_alert=True)
                return
            approve_user(user_ids)
            await cb.edit_message_text("Pesan Anda Diterima Tod")
            if str(user_ids) in OLD_MSG:
                await OLD_MSG[str(user_ids)].delete()
        elif isinstance(cb, Message):
            if is_approved(user_ids):
                await cb.edit("Pengguna Ini Sudah Ada Di Database.", show_alert=True)
                return
            approve_user(user_ids)
            await cb.edit("Pesan Anda Diterima Tod")
            if str(user_ids) in OLD_MSG:
                await OLD_MSG[str(user_ids)].delete()
        
    async def disapprove_pmpermit(
        self,
        cb,
        user_ids,
    ):
        from ..dB.pmpermit_db import disapprove_user, is_approved
        
        if isinstance(cb, CallbackQuery):
            if not is_approved(user_ids):
                return await cb.answer("Pengguna Ini Tidak Ada Di Database")
            disapprove_user(user_ids)
            await cb.edit_message_text("Pesan Anda Ditolak Tod")
        elif isinstance(cb, Message):
            if not is_approved(user_ids):
                return await cb.edit("Pengguna Ini Tidak Ada Di Database")
            disapprove_user(user_ids)
            await cb.edit("Pesan Anda Ditolak Tod")