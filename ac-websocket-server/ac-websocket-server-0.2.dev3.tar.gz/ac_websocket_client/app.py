#!/usr/bin/env python

'''Assetto Corsa Websockets App'''

import asyncio
from datetime import datetime
import json
import re
import sys
import tkinter as tk
from tkinter import ttk
from typing import Optional
import websockets

from ac_websocket_client import DEBUG
from ac_websocket_client.objects import *
from ac_websocket_server.protocol import Protocol


class App(tk.Tk):
    '''Wrapper class for Tk app'''

    UPDATE_INTERVAL = 1/120

    def __init__(self, loop, url=None):
        super().__init__()

        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.stop_ui)

        self.consumer_queue = asyncio.Queue()
        self.producer_queue = asyncio.Queue()

        self.is_connected = False
        self.is_registered = False
        self.is_started = False
        self.is_tracking = False

        self.drivers = {}
        self.entries = {}

        self.url = url
        self.websocket = None

        self.acws_connect_button = tk.StringVar(value='Connect')
        self.ac_game_button = tk.StringVar(value='Start Game')
        self.ac_lobby_button = tk.StringVar(value='(Re)register')
        self.tracker_button = tk.StringVar(value='Start Tracker')
        self.toggle_grid_button = tk.StringVar(value='Show Active')

        self.acws_traffic_light: Optional[TrafficLight] = None
        self.ac_game_traffic_light: Optional[TrafficLight] = None
        self.ac_lobby_traffic_light: Optional[TrafficLight] = None
        self.tracker_traffic_light: Optional[TrafficLight] = None
        self.driver_saved_traffic_light: Optional[TrafficLight] = None
        self.console_sent_traffic_light: Optional[TrafficLight] = None

        self.url_entry = tk.StringVar()

        self.game_name_entry = tk.StringVar()
        self.game_timestamp_entry = tk.StringVar()
        self.registered_entry = tk.StringVar()
        self.track_entry = tk.StringVar()
        self.cars_entry = tk.StringVar()
        self.session_entry = tk.StringVar()

        self.tracker_timestamp_entry = tk.StringVar()

        self.console_command_button = tk.StringVar(value='Send')
        self.console_command_entry = tk.StringVar()

        if self.url:
            self.url_entry.set(self.url)

        self.tasks = []

        self._create_ui()

    def _create_ui(self):
        '''Build the UI elements'''

        self.title(APP_TITLE)
        self.config(bg='lightgray')
        self.columnconfigure(0, weight=1)

        # ACWS Frame
        self.rowconfigure(0, weight=1)
        acws_frame = GriddedFrame(grid_row=0, grid_col=0, height_by=0.5)
        acws_frame.configure_columns(1, 1, 4, 1, 1)

        GriddedLabel(acws_frame, grid_row=0, grid_col=0, width=8,
                     text="ACWS")
        GriddedLabel(acws_frame, grid_row=0, grid_col=1, width=8,
                     text="url:")
        connect_entry = GriddedEntry(acws_frame, grid_row=0, grid_col=2,
                                     textvariable=self.url_entry)
        connect_entry.bind('<Return>', self._toggle_connection_event)
        GriddedButton(acws_frame, grid_row=0, grid_col=3,
                      textvariable=self.acws_connect_button,
                      command=lambda: self.loop.create_task(self._toggle_connection()))
        self.acws_traffic_light = TrafficLight(acws_frame, row=0, column=4)

        # AC Frame
        self.rowconfigure(1, weight=4)
        ac_frame = GriddedFrame(grid_row=1, grid_col=0, height_by=2.5)
        ac_frame.configure_columns(1, 1, 4, 1, 1)

        GriddedLabel(ac_frame, grid_row=0, grid_col=0, width=8, text="Game")

        GriddedLabel(ac_frame, grid_row=0, grid_col=1,
                     width=8, text="started:")
        GriddedEntry(ac_frame, grid_row=0, grid_col=2,
                     textvariable=self.game_timestamp_entry, state=tk.DISABLED)

        GriddedLabel(ac_frame, grid_row=1, grid_col=1,
                     width=8, text="registered:")
        GriddedEntry(ac_frame, grid_row=1, grid_col=2,
                     textvariable=self.registered_entry, state=tk.DISABLED)

        GriddedLabel(ac_frame, grid_row=2, grid_col=1, width=8, text="name:")
        GriddedEntry(ac_frame, grid_row=2, grid_col=2,
                     textvariable=self.game_name_entry, state=tk.DISABLED)

        GriddedLabel(ac_frame, grid_row=3, grid_col=1, width=8, text="track:")
        GriddedEntry(ac_frame, grid_row=3, grid_col=2,
                     textvariable=self.track_entry, state=tk.DISABLED)

        GriddedLabel(ac_frame, grid_row=4, grid_col=1, width=8, text="cars:")
        GriddedEntry(ac_frame, grid_row=4, grid_col=2,
                     textvariable=self.cars_entry, state=tk.DISABLED)

        GriddedLabel(ac_frame, grid_row=5, grid_col=1,
                     width=8, text="session:")
        GriddedEntry(ac_frame, grid_row=5, grid_col=2,
                     textvariable=self.session_entry, state=tk.DISABLED)

        GriddedButton(ac_frame, grid_row=0, grid_col=3,
                      textvariable=self.ac_game_button,
                      command=lambda: self.loop.create_task(self._toggle_game()))
        self.ac_game_traffic_light = TrafficLight(ac_frame, row=0, column=4)

        GriddedButton(ac_frame, grid_row=1, grid_col=3,
                      textvariable=self.ac_lobby_button,
                      command=lambda: self.loop.create_task(self._toggle_registration()))
        self.ac_lobby_traffic_light = TrafficLight(ac_frame, row=1, column=4)

        # Tracker Frame
        self.rowconfigure(2, weight=1)
        tracker_frame = GriddedFrame(grid_row=2, grid_col=0, height_by=0.5)
        tracker_frame.configure_columns(1, 1, 4, 1, 1)

        GriddedLabel(tracker_frame, grid_row=0,
                     grid_col=0, width=8, text="Tracker")

        GriddedLabel(tracker_frame, grid_row=0,
                     grid_col=1, width=8, text="started:")
        GriddedEntry(tracker_frame, grid_row=0, grid_col=2,
                     textvariable=self.tracker_timestamp_entry, state=tk.DISABLED)

        GriddedButton(tracker_frame, grid_row=0, grid_col=3,
                      textvariable=self.tracker_button,
                      command=lambda: self.loop.create_task(self._toggle_tracker()))
        self.tracker_traffic_light = TrafficLight(
            tracker_frame, row=0, column=4)

        # Drivers Frame
        self.rowconfigure(3, weight=4)
        driver_frame = GriddedFrame(grid_row=3, grid_col=0, height_by=3)
        driver_frame.configure_columns(1, 1, 1, 1, 1, 1, 1)

        GriddedLabel(driver_frame, grid_row=0,
                     grid_col=0, width=8, text="Grid")

        GriddedButton(driver_frame, grid_row=0, grid_col=2,
                      textvar=self.toggle_grid_button, width=10,
                      command=lambda: self.loop.create_task(self._toggle_grid()))
        GriddedButton(driver_frame, grid_row=0, grid_col=3,
                      text='Order 1..n', width=10,
                      command=lambda: self.loop.create_task(self._toggle_grid()))
        GriddedButton(driver_frame, grid_row=0, grid_col=4,
                      text='Order n..1', width=10,
                      command=lambda: self.loop.create_task(self._toggle_grid()))
        GriddedButton(driver_frame, grid_row=0, grid_col=5,
                      text='Apply', width=10,
                      command=lambda: self.loop.create_task(self._toggle_grid()))
        GriddedButton(driver_frame, grid_row=0, grid_col=6,
                      text='Save', width=10,
                      command=lambda: self.loop.create_task(self._toggle_grid()))
        self.driver_saved_traffic_light = TrafficLight(
            driver_frame, row=0, column=7)
        self.driver_saved_traffic_light.gray()

        self.driver_tree = GriddedTreeview(driver_frame, 1, 0, grid_span=8)
        self.driver_tree.add_columns('Name', 'GUID', 'Car', 'Ballast',
                                     'Restrictor', 'Position', 'Connected')
        self.driver_tree.set_widths(190, 80, 190, 80, 80, 80, 80)

        # Console Frame
        self.rowconfigure(4, weight=4)
        console_frame = GriddedFrame(grid_row=4, grid_col=0, height_by=3)
        console_frame.configure_columns(1, 1, 4, 1, 1)

        GriddedLabel(console_frame, grid_row=0, grid_col=0, width=8,
                     text="Console")
        GriddedLabel(console_frame, grid_row=0, grid_col=1, width=8,
                     text="command:")
        command_entry = GriddedEntry(console_frame, grid_row=0, grid_col=2,
                                     textvariable=self.console_command_entry)
        command_entry.bind('<Return>', self._send_command_event)

        GriddedButton(console_frame, grid_row=0, grid_col=3,
                      textvariable=self.console_command_button,
                      command=lambda: self.loop.create_task(self._send_command()))
        self.console_sent_traffic_light = TrafficLight(
            console_frame, row=0, column=4)
        self.console_sent_traffic_light.gray()

        listbox = GriddedListbox(
            console_frame, grid_row=1, grid_col=0, grid_span=5)

        self.tasks.append(self.loop.create_task(self._monitor(listbox)))

        if DEBUG:
            self.update()
            self._debug_ui(self, 0)

    def _debug_ui(self, w, depth=0):
        '''Print debug information on UI'''
        print('  ' * depth + f'{w.winfo_class()} w={str(w.winfo_width())}/{str(w.winfo_reqwidth())} h={str(w.winfo_height())}/{str(w.winfo_reqheight())} x/y=+{str(w.winfo_x())}+{str(w.winfo_y())}')
        for i in w.winfo_children():
            self._debug_ui(i, depth+1)

    async def _handler(self, websocket):
        '''Handle websocket tasks'''
        consumer_task = asyncio.create_task(self._handler_consumer(websocket))
        producer_task = asyncio.create_task(self._handler_producer(websocket))
        _done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

    async def _handler_consumer(self, websocket):
        '''Handle messages received from websocket'''
        async for msg in websocket:
            await self.consumer_queue.put(msg)

    async def _handler_producer(self, websocket):
        '''Handle messages received to send on websocket'''
        while True:
            try:
                message = await self.producer_queue.get()
                await websocket.send(message)
                await self.consumer_queue.put(Protocol.success(msg=f'Sent ==> {message}'))
            except Exception:
                print('\n> Connection Closing', file=sys.stderr)
                return

    async def _monitor(self, listbox: tk.Listbox):
        '''Monitor incoming messages and send to connection listbox'''
        while True:
            try:
                input_line = json.loads(await self.consumer_queue.get())

                output_fmt = {'fg': 'Black'}
                output_lines = ''

                if error_msg := input_line.get('error', None):

                    if error_msg['msg'] == 'ERROR,INVALID SERVER,CHECK YOUR PORT FORWARDING SETTINGS':
                        self.is_registered = False
                        self.ac_lobby_traffic_light.red()

                    output_fmt = {'fg': 'Red'}
                    output_lines = json.dumps(error_msg, indent=4)

                if success_msg := input_line.get('data', None):

                    if driver_msg := success_msg.get('driver', None):
                        if guid := driver_msg.get('guid', None):
                            if driver_joining := driver_msg.get('msg', None):
                                slot = driver_msg['slot']
                                self.entries[slot]['guid'] = guid
                                self.entries[slot]['drivername'] = driver_msg['name']
                                if 'joining' in driver_joining:
                                    self.drivers[guid] = driver_msg
                                    self.entries[slot]['connected'] = 'Yes'
                                    self._show_drivers()
                                else:
                                    self.entries[slot]['connected'] = 'No'
                                    del self.drivers[guid]
                                    self._show_drivers()

                    if session_msg := success_msg.get('lobby', None):
                        if session_msg['connected']:
                            self.is_registered = True
                            self.registered_entry.set(
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            self.ac_lobby_traffic_light.green()
                        else:
                            self.is_registered = False
                            self.registered_entry.set('')
                            self.ac_lobby_traffic_light.red()

                    if server_msg := success_msg.get('server', None):
                        if name := server_msg.get('name', None):
                            self.game_name_entry.set(name)
                        if timestamp := server_msg.get('timestamp', None):
                            self.game_timestamp_entry.set(timestamp)
                        self.track_entry.set(server_msg['track'])
                        self.cars_entry.set(server_msg['cars'])
                        if entries := server_msg.get('entries'):
                            for entry in entries:
                                slot = int(re.sub(r'\D', '', entry))
                                self.entries[slot] = entries[entry]
                                self.entries[slot]['connected'] = 'No'
                        self._show_entries()

                    if generic_msg := success_msg.get('msg', None):
                        if generic_msg == 'Stracker started':
                            self.tracker_traffic_light.green()
                        if generic_msg == 'Assetto Corsa server started':
                            self.ac_game_traffic_light.green()
                        if generic_msg == 'Assetto Corsa server stopped':
                            self.ac_game_traffic_light.red()

                    if session_msg := success_msg.get('sessions', None):
                        self.session_entry.set(
                            session_msg['type'] + ' ' + str(session_msg['laps']) + ' laps OR ' + str(session_msg['time']) + ' minutes')

                    output_fmt = {'fg': 'Green'}
                    output_lines = json.dumps(success_msg, indent=4)

                output_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                for output_line in output_lines.split('\n'):
                    listbox.insert(
                        tk.END, f'{output_timestamp}: {output_line}\n')
                    listbox.itemconfig(tk.END, output_fmt)
                listbox.yview(tk.END)

            except Exception as err:
                print(
                    f'Exception: "{err}" caught when processing:\n{input_line}')

    def _send_command_event(self, event):
        '''Send command to ACWS server'''
        self.loop.create_task(self._send_command())

    async def _send_command(self):
        '''Send command to ACWS server'''

        if self.is_connected:
            if command := self.console_command_entry.get():
                await self.consumer_queue.put(Protocol.success(msg=f'Sending ==> {command}'))
                await self.websocket.send(command)
        else:
            await self.consumer_queue.put(Protocol.error(msg='Not connected to ACWS server'))

    def _show_drivers(self):
        # pylint: disable=consider-using-dict-items

        self.toggle_grid_button.set('Show Entries')
        self.driver_tree.delete(*self.driver_tree.get_children())
        for key in self.drivers:
            self.driver_tree.insert('', tk.END,
                                    values=(self.drivers[key]['name'],
                                            self.drivers[key]['guid'],
                                            self.drivers[key]['car'],
                                            self.drivers[key]['ballast'],
                                            self.drivers[key]['restrictor'],
                                            'n/a', 'Yes'))

    def _show_entries(self):
        # pylint: disable=consider-using-dict-items

        self.toggle_grid_button.set('Show Drivers')
        self.driver_tree.delete(*self.driver_tree.get_children())
        for key in self.entries:
            self.driver_tree.insert('', tk.END,
                                    values=(self.entries[key]['drivername'],
                                            self.entries[key]['guid'],
                                            self.entries[key]['model'],
                                            self.entries[key]['ballast'],
                                            self.entries[key]['restrictor'],
                                            str(key + 1),
                                            self.entries[key]['connected']))

    async def start_ui(self, interval=UPDATE_INTERVAL):
        '''Start a the update of the UI'''
        while True:
            self.update()
            await asyncio.sleep(interval)

    def stop_ui(self):
        '''Cleanup all tasks'''
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()

    def _toggle_connection_event(self, event):
        '''Connect to the websocket server'''
        self.loop.create_task(self._toggle_connection())

    async def _toggle_connection(self, url=None):
        '''Connect to the websocket server'''

        if not url:
            url = self.url_entry.get()

        if not url:
            url = self.url

        if self.is_connected:
            await self.websocket.close()
            return

        try:
            async with websockets.connect(url) as websocket:
                self.url = url
                self.url_entry.set(url)
                self.title(f'{APP_TITLE} - Connected to {url}')
                self.acws_connect_button.set('Disconnect')
                self.acws_traffic_light.green()
                self.is_connected = True
                self.websocket = websocket
                await self.producer_queue.put('server info')
                await self._handler(websocket)
                await self.consumer_queue.put(Protocol.success(msg=f'Disconnecting from {url}'))
                self.is_connected = False
                self.title(f'{APP_TITLE}')
                self.acws_connect_button.set('Connect')
                self.acws_traffic_light.red()
        except OSError as error:
            await self.consumer_queue.put(Protocol.error(msg=str(error)))

    async def _toggle_game(self):
        '''Start the game'''

        if self.is_connected:
            if not self.is_started:
                await self.websocket.send('server start')
                self.is_started = True
                self.ac_game_button.set('Stop Game')
            else:
                await self.websocket.send('server stop')
                self.is_started = False
                self.ac_game_button.set('Start Game')
                self.ac_game_traffic_light.red()
        else:
            await self.consumer_queue.put(Protocol.error(msg='Not connected to ACWS server'))

    async def _toggle_grid(self):

        if 'Show Drivers' in self.toggle_grid_button.get():
            self._show_drivers()
        else:
            self._show_entries()

    async def _toggle_registration(self):
        '''(Re)-register in lobby'''

        if self.is_connected:
            await self.websocket.send('lobby restart')
        else:
            await self.consumer_queue.put(Protocol.error(msg='Not connected to ACWS server'))

    async def _toggle_tracker(self):
        '''Toggle tracker'''

        if self.is_connected:
            if not self.is_tracking:
                await self.websocket.send('tracker start')
                self.is_tracking = True
                self.tracker_button.set('Stop Tracker')
            else:
                await self.websocket.send('tracker stop')
                self.is_tracking = False
                self.tracker_button.set('Start Tracker')
                self.tracker_traffic_light.red()
        else:
            await self.consumer_queue.put(Protocol.error(msg='Not connected to ACWS server'))
