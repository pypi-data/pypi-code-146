import re
import discord.ui
from enum import Enum
from discord.utils import MISSING
import warnings
import logging
import re

logger = logging.getLogger('beymax.ui')

DISCORD_MODAL_TITLE_LIMIT = 45

async def null_callback(*args, **kwargs):
	pass

def add_component_to_callback(component, func):
	async def callback(*args, **kwargs):
		return await func(component, *args, **kwargs)
	return callback

class Button(discord.ui.Button):
	"""
	Callback should have signature 
	"""
	def __init__(self, label : str, *, callback_or_url = None, custom_id : str = None, disabled: bool = False, style:discord.ButtonStyle = discord.ButtonStyle.secondary, emoji = None, row: int = None, call_with_component=False):
		super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=callback_or_url if isinstance(callback_or_url, str) else None, emoji=emoji, row=row)
		if callback_or_url is None:
			self.callback = null_callback
		elif not isinstance(callback_or_url, str):
			if call_with_component:
				callback_or_url = add_component_to_callback(self, callback_or_url)
			self.callback = callback_or_url
		
		

class Select(discord.ui.Select):
	def __init__(self, placeholder: str, *, callback = None, custom_id: str = MISSING, min_values: int = 1, max_values: int = 1, options=MISSING, disabled: bool = False, row: int = False, call_with_component=True):
		super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, options=options, disabled=disabled, row=row)
		if callback is None:
			self.callback = null_callback
		else:
			if call_with_component:
				callback = add_component_to_callback(self, callback)
			self.callback = callback

class UserSelect(discord.ui.UserSelect):
	def __init__(self, placeholder: str, *, callback = None, custom_id: str = MISSING, min_values: int = 1, max_values: int = 1, disabled: bool = False, row: int = False, call_with_component=True):
		super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, disabled=disabled, row=row)
		if callback is None:
			self.callback = null_callback
		else:
			if call_with_component:
				callback = add_component_to_callback(self, callback)
			self.callback = callback

class RoleSelect(discord.ui.RoleSelect):
	def __init__(self, placeholder: str, *, callback = None, custom_id: str = MISSING, min_values: int = 1, max_values: int = 1, disabled: bool = False, row: int = False, call_with_component=True):
		super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, disabled=disabled, row=row)
		if callback is None:
			self.callback = null_callback
		else:
			if call_with_component:
				callback = add_component_to_callback(self, callback)
			self.callback = callback


class MentionableSelect(discord.ui.MentionableSelect):
	def __init__(self, placeholder: str, *, callback = None, custom_id: str = MISSING, min_values: int = 1, max_values: int = 1, disabled: bool = False, row: int = False, call_with_component=True):
		super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, disabled=disabled, row=row)
		if callback is None:
			self.callback = null_callback
		else:
			if call_with_component:
				callback = add_component_to_callback(self, callback)
			self.callback = callback

class ChannelSelect(discord.ui.ChannelSelect):
	def __init__(self, placeholder: str, *, callback = None, custom_id: str = MISSING, min_values: int = 1, max_values: int = 1, channel_types=MISSING, disabled: bool = False, row: int = False, call_with_component=True):
		super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, channel_types=channel_types, disabled=disabled, row=row)
		if callback is None:
			self.callback = null_callback
		else:
			if call_with_component:
				callback = add_component_to_callback(self, callback)
			self.callback = callback

class SelectType(Enum):
	User = UserSelect
	Role = RoleSelect
	Mentionable = MentionableSelect
	Channel = ChannelSelect

class TextInput(discord.ui.TextInput):
	def __init__(self, label:str, *, callback = None, style = discord.TextStyle.short, custom_id = MISSING, placeholder=None, default=None, required=True, min_length=None, max_length=None, row=None, call_with_component=True, regex=None, validator=None):
		super().__init__(label=label, style=style, custom_id=custom_id, placeholder=placeholder, default=default, required=required, min_length=min_length, max_length=max_length, row=row)
		if callback is None:
			self.callback = null_callback
		else:
			if call_with_component:
				callback = add_component_to_callback(self, callback)
			self.callback = callback
		self.validator = None
		if not (regex is None or validator is None):
			raise ValueError("Cannot specify both a regex and validator")
		if regex is not None:
			if isinstance(regex, str):
				regex = re.compile(regex)
			self.validator = lambda value:regex.match(value) is not None
		elif validator is not None:
			self.validator = validator

class BaseView(object):

	def timeout_handler(self, func):
		async def on_timeout():
			return await func(self)

		self.on_timeout = on_timeout

	async def on_error(self, interaction, error, item=None):
		logger.error("Unhandled exception from UI element", exc_info=True)
		await interaction.client.trace()


	def button(self, label : str, *, custom_id : str = None, disabled: bool = False, style:discord.ButtonStyle = discord.ButtonStyle.secondary, emoji = None, row: int = None, call_with_component=False):

		def wrapper(func):
			btn = Button(
				label=label,
				callback_or_url=func,
				custom_id=custom_id,
				disabled=disabled,
				style=style,
				emoji=emoji,
				row=row,
				call_with_component=call_with_component
			)

			self.add_item(btn)

			return btn

		return wrapper

	def select(self, placeholder: str, *, custom_id: str = MISSING, min_values: int = 1, max_values: int = 1, options=MISSING, channel_types=MISSING, disabled: bool = False, row: int = None, call_with_component=True):

		def wrapper(func):
			if isinstance(options, SelectType):
				if options == SelectType.Channel:
					# channel selector needs special handling because of channel_types argument
					slct = ChannelSelect(
						placeholder=placeholder,
						callback=func,
						custom_id=custom_id,
						min_values=min_values,
						max_values=max_values,
						channel_types=channel_types,
						disabled=disabled,
						row=row,
						call_with_component=call_with_component
					)
				else:
					# option value is a selector type
					slct = options.value(
						placeholder=placeholder,
						callback=func,
						custom_id=custom_id,
						min_values=min_values,
						max_values=max_values,
						disabled=disabled,
						row=row,
						call_with_component=call_with_component
					)
			else:
				slct = Select(
					placeholder=placeholder,
					callback=func,
					custom_id=custom_id,
					min_values=min_values,
					max_values=max_values,
					options=options,
					disabled=disabled,
					row=row,
					call_with_component=call_with_component
				)
			if channel_types is not MISSING and options != SelectType.Channel:
				raise TypeError("Provided channel_types to a select which was not of type ChannelSelect")
			self.add_item(slct)
			return slct

		return wrapper
	
	def add_select(self, placeholder: str, *, custom_id: str = MISSING, min_values: int = 1, max_values: int = 1, options=MISSING, channel_types=MISSING, disabled: bool = False, row: int = None):
		return self.select(
			placeholder=placeholder,
			custom_id=custom_id,
			min_values=min_values,
			max_values=max_values,
			options=options,
			channel_types=channel_types,
			disabled=disabled,
			row=row
		)(null_callback)

	def textinput(self, label:str, *, style = discord.TextStyle.short, custom_id = MISSING, placeholder=None, default=None, required=True, min_length=None, max_length=None, row=None, call_with_component=True, regex=None, validator=None):

		def wrapper(func):
			text = TextInput(
				label=label,
				callback=func,
				style=style,
				custom_id=custom_id,
				placeholder=placeholder,
				default=default,
				required=required,
				min_length=min_length,
				max_length=max_length,
				row=row,
				call_with_component=call_with_component,
				regex=regex,
				validator=validator
			)

			self.add_item(text)
			return text

		return wrapper
	
	def add_textinput(self, label:str, *, style = discord.TextStyle.short, custom_id = MISSING, placeholder=None, default=None, required=True, min_length=None, max_length=None, row=None, regex=None, validator=None):
		return self.textinput(
			label=label,
			style=style,
			custom_id=custom_id,
			placeholder=placeholder,
			default=default,
			required=required,
			min_length=min_length,
			max_length=max_length,
			row=row,
			regex=regex,
			validator=validator
		)(null_callback)

	
class View(BaseView, discord.ui.View):
	async def textinput(self, label: str, *, style=discord.TextStyle.short, custom_id=MISSING, placeholder=None, default=None, required=True, min_length=None, max_length=None, row=None, call_with_component=True):
		warnings.warn("Discord Views do not yet support TextInput elements. This view may fail to display")
		return super().textinput(label, style=style, custom_id=custom_id, placeholder=placeholder, default=default, required=required, min_length=min_length, max_length=max_length, row=row, call_with_component=call_with_component)

class Modal(BaseView, discord.ui.Modal):
	def __init__(self, *args, on_validation_failed=None, **kwargs):
		super().__init__(*args, **kwargs)
		self._submission = None
		self._validate_fields = []
		self._on_validation_failed = on_validation_failed
		if len(self.title) > DISCORD_MODAL_TITLE_LIMIT:
			raise ValueError("Discord limits modal Titles to 45 characters")
	
	async def on_submit(self, interaction):
		for field in self._validate_fields:
			if not field.validator(field.value):
				if self._on_validation_failed is None:
					return await interaction.response.send_message(
						'Value for input "{}" did not match the expected format'.format(field.label),
						ephemeral=True
					)
				else:
					return await self._on_validation_failed(self, interaction)
		if self._submission is not None:
			return await self._submission(self, interaction)
		await interaction.response.send_message(
			"No handler set for modal. Your input has been discarded",
			ephemeral=True
		)
	
	def add_item(self, element):
		if isinstance(element, TextInput) and element.validator is not None:
			self._validate_fields.append(element)
		return super().add_item(element)
	
	def on_validation_failed(self, func):
		logger.info("Setting validation failure handler to {}".format(func))
		self._on_validation_failed = func
		return func
	
	def submit(self, func):
		self._submission = func
	
	async def select(self, placeholder: str, *, custom_id: str = MISSING, min_values: int = 1, max_values: int = 1, options=MISSING, channel_types=MISSING, disabled: bool = False, row: int = None, call_with_component=True):
		warnings.warn("Discord Modals do not yet support Select elements. This modal may fail to display")
		return super().select(placeholder, custom_id=custom_id, min_values=min_values, max_values=max_values, options=options, channel_types=channel_types, disabled=disabled, row=row, call_with_component=call_with_component)


class ModalChain(BaseView):
	def __init__(self, *args, title=None, **kwargs):
		self._submission = None
		self._modals = [Modal(*args, title=title, **kwargs)]
		self.title = title
		if len(self.title) > DISCORD_MODAL_TITLE_LIMIT:
			raise ValueError("Discord limits modal Titles to 45 characters")
	
	async def on_submit(self, interaction):
		if self._submission is not None:
			return await self._submission(self, interaction)
		await interaction.response.send_message(
			"No handler set for modal. Your input has been discarded",
			ephemeral=True
		)

	def add_item(self, element):
		try:
			self._modals[-1].add_item(element)
		except ValueError:
			logger.debug("Adding new modal to modal chain (new length {})".format(1+len(self._modals)))
			self._modals.append(Modal(title=self.title))
			return self.add_item(element)
	
	def render(self):
		for modal_pre, modal_post in zip(self._modals[:-1], self._modals[1:]):
			
			@modal_pre.submit
			async def present_view(m, i):
				view = View()
				@view.button('Next')
				async def interstitial(i2):
					await i2.response.send_modal(modal_post)
					await i.delete_original_response()
				# FIXME: is it desirable to edit the original message? (if i.message is not None: await i.response.edit_message)
				await i.response.send_message("Due to API limitations, you'll need to click this button to present the next set of menu options", view=view, ephemeral=True)
		
		self._modals[-1]._submission = self._submission

		return self._modals[0]

	
	def submit(self, func):
		self._submission = func
	
	async def select(self, placeholder: str, *, custom_id: str = MISSING, min_values: int = 1, max_values: int = 1, options=MISSING, channel_types=MISSING, disabled: bool = False, row: int = None, call_with_component=True):
		warnings.warn("Discord Modals do not yet support Select elements. This modal may fail to display")
		return super().select(placeholder, custom_id=custom_id, min_values=min_values, max_values=max_values, options=options, channel_types=channel_types, disabled=disabled, row=row, call_with_component=call_with_component)