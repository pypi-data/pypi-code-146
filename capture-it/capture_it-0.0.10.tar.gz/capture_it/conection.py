# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from netmiko import ConnectHandler
import paramiko, traceback
import pandas as pd
from time import sleep
from nettoolkit import STR, IO, IP, LOG
from facts_finder.database import append_to_xl
from facts_finder import evaluate

# -----------------------------------------------------------------------------

BAD_CONNECTION_MSG = ': BAD CONNECTION DETECTED, TEARED DOWN'
cisco_banner ="""
! ---------------------------------------------------------------------------- !
! This output is generated using capture_it utility.
! Script written by : Aliasgar Hozaifa Lokhandwala (aholo2000@gmail.com)
! Write an email if any errors found.
! ---------------------------------------------------------------------------- !
"""
juniper_banner = """
# ---------------------------------------------------------------------------- #
# This output is generated using capture_it utility.
# Script written by : Aliasgar Hozaifa Lokhandwala (aholo2000@gmail.com)
# Write an email if any errors found.
# ---------------------------------------------------------------------------- #
"""
# -----------------------------------------------------------------------------
# Device Type Detection (1st Connection)
# -----------------------------------------------------------------------------
class DeviceType:
	"""'Defines Device type ( 'cisco_ios', 'arista_eos', 'juniper_junos')

	Args:
		dev_ip (str): ip address of device
		un (str): username to login to device
		pw (str): password to login to device
	
	Properties:
		dtype (str): device type (default/or exception will return 'cisco_ios')
	"""    	

	# INITIALIZER - DEVICE TYPE
	def __init__(self, dev_ip, un, pw):
		"""initialize object with given ip and credentials

		Args:
			dev_ip (str): ip address of device
			un (str): username to login to device
			pw (str): password to login to device
		"""    		
		'''class initializer'''
		self.device_types = {'cisco': 'cisco_ios',
						'arista': 'arista_eos',
						'juniper': 'juniper_junos'}
		self.dtype = self.__device_make(dev_ip, un, pw)

	# device type
	@property
	def dtype(self):
		"""device type
		* 'cisco': 'cisco_ios',
		* 'arista': 'arista_eos',
		* 'juniper': 'juniper_junos'

		Returns:
			str: device type
		"""    		
		return self.device_type

	# set device type
	@dtype.setter
	def dtype(self, devtype='cisco'):
		self.device_type = self.device_types.get(devtype, 'cisco_ios')
		return self.device_type

	# device make retrival by login
	def __device_make(self, dev_ip, un, pw):
		with paramiko.SSHClient() as ssh:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				ssh.connect(dev_ip, username=un, password=pw)
			except (paramiko.SSHException, 
					paramiko.ssh_exception.AuthenticationException, 
					paramiko.AuthenticationException
					) as e:
				pass
			with ssh.invoke_shell() as remote_conn:
				remote_conn.send('\n')
				sleep(1)
				remote_conn.send('ter len 0 \nshow version\n')
				sleep(2)
				output = remote_conn.recv(5000000).decode('UTF-8').lower()
				for k, v in self.device_types.items():
					if STR.found(output, k): 
						return k

# -----------------------------------------------------------------------------
# connection Object (2nd Connection)
# -----------------------------------------------------------------------------

class conn(object):
	"""Initiate an active connection.  
	use it with context manager to execute necessary commands on to it.

	Args:
		ip (str): ip address of device to establish ssh connection with
		un (str): username to login to device
		pw (str): user password to login to device
		en (str): enable password (For cisco)
		delay_factor (int): connection stability factor
		devtype (str, optional): device type from DeviceType class. Defaults to ''.
		hostname (str, optional): hostname of device ( if known ). Defaults to ''.

	Properties:
		hn (str): hostname
		devvar (dict) : {'ip':ip, 'host':hostname}
		devtype (str) : device type ('cisco_ios', 'arista_eos', 'juniper_junos')
	"""    	
	# Connection Initializer
	def __init__(self, 
		ip, 
		un, 
		pw, 
		en, 
		delay_factor, 
		devtype='', 
		hostname='', 
		):
		"""initiate a connection object

			Args:
			ip (str): ip address of device to establish ssh connection with
			un (str): username to login to device
			pw (str): user password to login to device
			en (str): enable password (For cisco)
			delay_factor (int): connection stability factor
			devtype (str, optional): device type from DeviceType class. Defaults to ''.
			hostname (str, optional): hostname of device ( if known ). Defaults to ''.
		"""		
		self.conn_time_stamp = LOG.time_stamp()
		self._devtype = devtype 						# eg. cisco_ios
		self._devvar = {'ip': ip, 'host': hostname }	# device variables
		self.__set_local_var(un, pw, en)				# setting 
		self.banner = juniper_banner if self.devtype == 'juniper_junos' else cisco_banner
		self.delay_factor = delay_factor
		self.clsString = f'Device Connection: \
{self.devtype}/{self._devvar["ip"]}/{self._devvar["host"]}'
		self.__connect
		self.devvar = self._devvar

	# context load
	def __enter__(self):
		if self.connectionsuccess:
			self.__set_hostname
			self.clsString = f'Device Connection: \
{self.devtype}/{self._devvar["ip"]}/{self._devvar["host"]}'
		return self      # ip connection object

	# cotext end
	def __exit__(self, exc_type, exc_value, tb):
		self.__terminate
		if exc_type is not None:
			traceback.print_exception(exc_type, exc_value, tb)

	# representation of connection
	def __repr__(self):
		return self.clsString

	@property
	def clsStr(self):
		return self.clsString
	@clsStr.setter
	def clsStr(self, s):
		self.clsString = s

	# RETURN --- > DEVICETYPE
	@property
	def devtype(self):
		"""device type
		* 'cisco': 'cisco_ios',
		* 'arista': 'arista_eos',
		* 'juniper': 'juniper_junos'

		Returns:
			str: device type
		"""    
		return self._devtype

	# RETURN --- > DEVICE HOSTNAME
	@property
	def hn(self):
		"""device hostname

		Returns:
			str: device hostname
		"""    
		# return self._hn
		return self._devvar['host']

	# set connection var|properties
	def __set_local_var(self, un, pw, en):
		'''Inherit User Variables'''
		self._devvar['username'] = un
		self._devvar['password'] = pw
		self._devvar['secret'] = en
		if self._devtype == '':
			self._devtype = DeviceType(self._devvar['ip'], 
				self._devvar['username'], self._devvar['password']
				).device_type 
		self._devvar['device_type'] = self._devtype

	# establish connection
	@property
	def __connect(self):
		try:
			self.net_connect = ConnectHandler(**self._devvar) 
			self.connectionsuccess = True			
		except:
			self.connectionsuccess = False

		if self.connectionsuccess:
			self._devvar['host'] = STR.hostname(self.net_connect)
			self._hn = self._devvar['host']
			if any( [
				self._devvar['device_type'].lower() == 'cisco_ios'
				] ):
				for tries in range(3):
					try:
						self.net_connect.enable(cmd="enable")
						break
					except:
						print(f"{self._devvar['host']} - enable failed on attemp {tries}")
						continue

	# set connection hostname property
	@property
	def __set_hostname(self):
		self._devvar['host'] = STR.hostname(self.net_connect)

	# terminate/disconnect session
	@property
	def __terminate(self):
		try:
			self.net_connect.disconnect()
		except:
			pass


# -----------------------------------------------------------------------------
# Command Execution on a conn(connection) object, store to file
# -----------------------------------------------------------------------------

class COMMAND():
	"""CAPTURE OUTPUT FOR GIVEN COMMAND - RETURN CONTROL/OUTPUT 

	Args:
		conn (conn): connection object
		cmd (str): a command to be executed
		path (str): path where output to be stored


	Properties:
		cmd (str): command executed
		commandOP, output (str) - command output
		fname (filename): full filename with path where output stored
	"""    	

	# INITIALIZE class vars
	def __init__(self, conn, cmd, path, parsed_output):
		"""[summary]

		Args:
			conn (conn): connection object
			cmd (str): a command to be executed
			path (str): path where output to be stored
		"""    		
		self.conn = conn
		self.cmd = cmd
		self.path = path
		self.parsed_output = parsed_output
		self._commandOP(conn)


	def op_to_file(self, cumulative=False):
		"""store output of command to file, cumulative (True,False,both) to store output in a single file, individual files, both

		Args:
			cumulative (bool, optional): True,False,both. Defaults to False.

		Returns:
			str: file name where output get stored
		"""    		
		if cumulative:
			self.cumulative_filename = self.add_to_file(self.commandOP)    # add to file
			self.fname = self.cumulative_filename
			print(self.cmd, ">> ", self.fname)
		else:
			self.fname = self.send_to_file(self.commandOP)    # save to file
			print(self.cmd, ">> ", self.fname)
		if isinstance(cumulative, str) and cumulative=='both':
			self.fname = self.send_to_file(self.commandOP)    # save to file
		return self.fname

	# Representation of Command object
	def __repr__(self):
		return f'object: Output for \n{self.conn} \ncommand: {self.cmd}'

	# RETURNS ---> Command output
	@property
	def commandOP(self):
		'''command output'''
		return self.output

	# capture output from connection
	def _commandOP(self, conn):
		self.output = ''

		op = self.conn.net_connect.send_command(self.cmd, 
				read_timeout=20, 
				delay_factor=self.conn.delay_factor,
				use_textfsm=self.parsed_output,
				)

		# exclude missed ones
		if any([								
			STR.found(op,'Connection refused')
			]):                                 ### ADD More as needed ###
			print(" CONNECTION WAS REFUSED ")
			return None
		self.output = op

	# send output to textfile
	def send_to_file(self, output):
		"""send output to a text file

		Args:
			output (str): captured output

		Returns:
			str: filename where output got stored
		"""    		
		fname = STR.get_logfile_name(self.path, hn=self.conn.hn, cmd=self.cmd, ts=self.conn.conn_time_stamp)
		print('> '+fname)
		IO.to_file(filename=fname, matter=output)
		return fname

	# send output to textfile
	def add_to_file(self, output):
		"""add output to a text file

		Args:
			output (str): captured output

		Returns:
			str: filename where output got appended
		"""    		
		banner = self.banner if self.banner else ""
		rem = "#" if self.conn.devtype == 'juniper_junos' else "!"
		cmd_header = f"\n{rem}{'='*80}\n{rem} output for command: {self.cmd}\n{rem}{'='*80}\n\n"
		fname = STR.get_logfile_name(self.path, hn=self.conn.hn, cmd="", ts=self.conn.conn_time_stamp)
		IO.add_to_file(filename=fname, matter=banner+cmd_header+output)
		return fname

# -----------------------------------------------------------------------------
# Execution of Show Commands on a single device. 
# -----------------------------------------------------------------------------

class Execute_Device():
	"""Execute a device capture

	Args:
		ip (str): device ip
		auth (dict): authentication parameters
		cmds (list, set, tuple): set of commands to be executed.
		path (str): path where output to be stored
		cumulative (bool, optional): True,False,both. Defaults to False.
	"""    	

	def __init__(self, 
		ip, 
		auth, 
		cmds, 
		path, 
		cumulative, 
		forced_login, 
		parsed_output,
		parse_n_clean,
		):
		"""initialize execution

		Args:
			ip (str): device ip
			auth (dict): authentication parameters
			cmds (list, set, tuple): set of commands to be executed.
			path (str): path where output to be stored
			cumulative (bool, optional): True,False,both. Defaults to False.
		"""    		
		self.auth = auth
		self.cmds = cmds
		self.path = path
		self.cumulative = cumulative
		self.cumulative_filename = None
		self.forced_login = forced_login
		self.parsed_output = parsed_output
		self.parse_n_clean = parse_n_clean
		self.delay_factor, self.dev = None, None
		pinging = self.check_ping(ip)
		if forced_login or pinging:
			self.get_device_type(ip)
			try:
				self.dev.dtype
			except:
				print(f"DeviceType not detected for {ip}")
			if self.dev is not None and self.dev.dtype == 'cisco_ios': sleep(65)
			self.execute(ip)


	def check_ping(self, ip):
		"""check device reachability

		Args:
			ip (str): device ip

		Returns:
			int: delay factor if device reachable,  else False
		"""    		
		try:
			self.delay_factor = IP.ping_average (ip)/100 + 3
			# print(self.delay_factor)
			return self.delay_factor
		except:
			return False

	def get_device_type(self, ip):
		"""detect device type (cisco, juniper)

		Args:
			ip (str): device ip

		Returns:
			str: device type if detected, else None
		"""    		
		try:
			self.dev = DeviceType(dev_ip=ip, 
				un=self.auth['un'], 
				pw=self.auth['pw'])
			return self.dev
		except Exception as e:
			print(f'{ip}: {e}')
			return None

	def is_connected(self, c):
		"""check if connection is successful

		Args:
			c (conn): connection object

		Returns:
			conn: connection object if successful, otherwise None
		"""    		
		connection = True
		if STR.found(str(c), "FAILURE"): connection = None
		if c.hn == None or c.hn == 'dummy': connection = None
		return connection

	def execute(self, ip):
		"""login to given device(ip) using authentication parameters from uservar (u).
		if success start command captuers

		Args:
			ip (str): device ip
		"""    		
		with conn(	ip=ip, 
					un=self.auth['un'], 
					pw=self.auth['pw'], 
					en=self.auth['en'], 
					delay_factor=self.delay_factor,
					devtype=self.dev.dtype,
					) as c:
			if self.is_connected(c):
				cc = self.command_capture(c)
				self.cumulative_filename = cc.cumulative_filename
				if self.parsed_output: 
					xl_file = cc.write_facts()
				if self.parse_n_clean:
					cc.clean(xl_file, self.cumulative_filename)

	def command_capture(self, c):
		"""start command captures on connection object

		Args:
			c (conn): connection object
		"""    		
		cc = Captures(dtype=self.dev.dtype, 
			conn=c, 
			cmds=self.cmds, 
			path=self.path, 
			cumulative=self.cumulative,
			parsed_output=self.parsed_output
			)
		return cc

# -----------------------------------------------------------------------------
# Execution of Show Commands on a single device. 
# -----------------------------------------------------------------------------

class CLP():
	"""parent for Command processing

	Args:
		dtype (str): device type
		conn (conn): connection object
		path (str): path to store the captured output	
	"""    	
	def __init__(self, dtype, conn, path, parsed_output):
		"""Initialize object

		Args:
			dtype (str): device type
			conn (conn): connection object
			path (str): path to store the captured output	
		"""    		
		self.dtype = dtype
		self.conn = conn
		self.path = path
		self.parsed_output = parsed_output
		self.cumulative_filename = None
		self.parsed_cmd_df = {}
		self.cmd_exec_logs = []
		self.hn = self.conn.hn
		self.ip = self.conn.devvar['ip']
		self.configure(False)						# fixed disable as now

	def configure(self, config_mode=False):
		"""set configuration mode

		Args:
			config_mode (bool, optional): enable/disable config commands. Defaults to False.
		"""    		
		self._configure = config_mode

	def check_config_authorization(self, cmd):
		"""check if given command is allowed or not on this device.

		Args:
			cmd (str): command to be executed

		Returns:
			bool: True/False
		"""    		
		if not self._configure and 'config' == cmd.lstrip()[:6].lower():
			print(f"{self.hn} : Config Mode disabled, Exiting")
			return False
		return True

	def cmd_capture(self, cmd, cumulative=False, banner=False):
		"""start command capture for given command

		Args:
			cmd (str): command to be executed
			cumulative (bool, optional): True/False/both. Defaults to False.
			banner (bool, optional): set a banner property to object if given. Defaults to False.

		Returns:
			[type]: [description]
		"""    		
		self.cmd_exec_logs.append({'command':cmd})
		cmdObj = self._cmd_capture_raw(cmd, cumulative, banner)
		if cmdObj is not None:
			self._cmd_capture_parsed(cmd, cumulative, banner)
		return cmdObj

	def _cmd_capture_raw(self, cmd, cumulative=False, banner=False):
		try:
			cmdObj = COMMAND(conn=self.conn, cmd=cmd, path=self.path, parsed_output=False)
		except:
			print(f"{self.hn} : Error executing command {cmd}")
			self.cmd_exec_logs[-1]['raw'] = False
			return None
		try:
			cmdObj.banner = banner		
			file = cmdObj.op_to_file(cumulative=cumulative)
			self.cmd_exec_logs[-1]['raw'] = True
			if self.cumulative_filename is None:
				self.cumulative_filename = cmdObj.cumulative_filename
			return cmdObj
		except:
			print(f"{self.hn} : Error writing output for command {cmd}\n{cmdObj.output}")
			print(self.cmd_exec_logs)
			self.cmd_exec_logs[-1]['raw'] = False
			return False

	def _cmd_capture_parsed(self, cmd, cumulative=False, banner=False):
		try:
			cmdObj_parsed = COMMAND(conn=self.conn, cmd=cmd, path=self.path, parsed_output=True)
		except:
			print(f"{self.hn} : Error executing command - Parse Run {cmd}")
			self.cmd_exec_logs[-1]['parsed'] = False
			return None
		try:
			self.parsed_cmd_df[cmd] = pd.DataFrame(cmdObj_parsed.output)
			self.cmd_exec_logs[-1]['parsed'] = True
		except:
			print(f"{self.hn} : Error parsing output for command {cmd}")
			print(f"{self.hn} : data facts may not be available for command: {cmd}")
			self.cmd_exec_logs[-1]['parsed'] = False
			return False



class Captures(CLP):
	"""Capture output

	Args:
		dtype (str): device type
		conn (conn): connection object
		cmds (set, list, tuple): set of commands 
		path (str): path to store the captured output
		cumulative (bool, optional): True/False/both. Defaults to False.

	"""    	

	def __init__(self, dtype, conn, cmds, path, cumulative=False, parsed_output=False):
		"""Initiate captures

		Args:
			dtype (str): device type
			conn (conn): connection object
			cmds (set, list, tuple): set of commands 
			path (str): path to store the captured output
			cumulative (bool, optional): True/False/both. Defaults to False.
		"""    		
		super().__init__(dtype, conn, path, parsed_output)
		self.cmds = cmds
		self.op = ''
		self.cumulative = cumulative
		self.cumulative_filename = None
		self.grp_cmd_capture()


	def grp_cmd_capture(self):
		"""grep the command captures for each commands	
		Unauthorized command will halt execution.

		Returns:
			None: None
		"""    		
		banner = self.conn.banner
		for cmd  in self.cmds[self.dtype]:
			# try:
			if not self.check_config_authorization(cmd): 
				print(f"UnAuthorizedCommandDetected-{cmd}-EXECUTIONHALTED")
				return None
			cc = self.cmd_capture(cmd, self.cumulative, banner)
			# output = cc.commandOP #if cc else f": Error executing command {cmd}"
			try:
				output = cc.output
			except:
				output = f": Error executing command {cmd}"
			cmd_line = self.hn + ">" + cmd + "\n"
			self.op += cmd_line + "\n" + output + "\n\n"
			banner = ""


			# break

	def add_exec_logs(self):
		self.parsed_cmd_df['logs'] = pd.DataFrame(self.cmd_exec_logs)

	def write_facts(self):
		"""writes commands facts in to excel tab
		"""
		try:
			self.add_exec_logs()
			xl_file = self.path + self.conn.hn + ".xlsx"
			print(f"writing facts to excel: {xl_file}", end="\t")
			append_to_xl(xl_file, self.parsed_cmd_df, overwrite=True)
			print(f"...success!")
		except:
			print(f" ...failed!")
		return xl_file


	def clean(self, xl_file, cumulative_filename):
		"""cleans excel fact file. removes some unwanted and adds a few more details.  Creates a new Gene file.
		"""
		ev = evaluate(
			capture_log_file=cumulative_filename,
			capture_file=xl_file,
			cisco_var_column_mapper_file=None,
			cisco_int_column_mapper_file=None,
			juniper_column_mapper_file=None,
			)
		return ev