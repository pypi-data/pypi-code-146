import traceback, time
from retry import retry
from typing import List, Tuple, Dict, Optional, Callable
from ddd_objects.domain.exception import OperationError
from ddd_objects.lib import get_random_string
from .repository import CommandRepository
from .value_obj_ext import (
    PipelineOutput,
    PipelineIndicator,
    PipelineContext,
)
from .value_obj import Name, Command, Number, CommandPriority, CommandID
from .entity_ext import (
    PipelineActionOutput,
    _PipelineStage
)
from .entity import CommandHost, CommandRequest, CommandSettingDetail, CommandItem
from ..settings import logger as _logger



class CyclePipelineTemplate:
    def __init__(
        self, 
        stages:List[_PipelineStage], 
        context: PipelineContext,
        output_fn: Optional[Callable]=None,
    ) -> None:
        self.__stages = stages
        self.__stage_idx_map = {s.stage_name:i for i,s in enumerate(stages)}
        self.__curr_stage_idx = -1
        self.__stage_num = len(stages)
        self.__output_fn = output_fn
        self.context = context
        self.indicator = PipelineIndicator()
        self.status = {}
    

    def __next_stage(self)->Tuple[str, Callable, bool]:
        self.__curr_stage_idx = (self.__curr_stage_idx+1)%self.__stage_num
        stage = self.__stages[self.__curr_stage_idx]
        return stage.stage_name, stage.action, stage.allow_failure
    

    def __jump_to(self, stage:Name):
        stage_idx = self.__stage_idx_map[stage.get_value()]
        self.__curr_stage_idx = (stage_idx-1)%self.__stage_num


    def run(self):
        indicator = self.indicator
        if indicator.is_wait() or indicator.is_over():
            pass

        elif indicator.is_pass():
            stage, func, allow_failure = self.__next_stage()
            self.status = {
                'stage': stage,
                'action': func,
                'context': self.context,
                'indictor': self.indicator,
                'allow_failure': allow_failure
            }

        elif indicator.is_run() or indicator.is_run_again():
            if indicator.is_run():
                stage, func, allow_failure = self.__next_stage()
                self.status['stage'] = stage
                self.status['action'] = func
                self.status['allow_failure'] = allow_failure
            else:
                func = self.status['action']
                allow_failure = self.status['allow_failure']
                stage = self.status['stage']
            try:
                output:PipelineActionOutput = func(self.context)
                self.context = output.context
                self.indicator = output.indicator
                self.output = output.output
                jump_stage = output.jump_stage
                if jump_stage is not None:
                    self.__jump_to(jump_stage)
                self.status = {
                    'stage': stage,
                    'action': func,
                    'context': self.context,
                    'indictor': self.indicator,
                    'allow_failure': allow_failure,
                    'output': self.output
                }
            except:
                if not allow_failure:
                    raise OperationError(traceback.format_exc())
                else:
                    self.indicator.set_run_again()
        return self.status

    def is_over(self):
        return self.indicator.is_over()

    def get_output(self, x=None):
        if self.__output_fn is None:
            return self.output
        else:
            return self.__output_fn(self.output, x)

    def run_until_complete(self, timeout=100, interval=1):
        x = []
        for i in range(timeout):
            status = self.run()
            if self.output:
                # _logger.debug(f'pipeline status: {status}')
                x.append(self.output)
            if self.is_over():
                return self.get_output(x)
            time.sleep(interval)
        raise OperationError(f'Timeout ({timeout}s) when running loop')



class PipelineGenerator:

    def generate_pipeline(self):
        raise NotImplementedError

    def set_output(self, output: Optional[PipelineOutput]):
        raise NotImplementedError

    def _set_run_again_output(self, context):
        return PipelineActionOutput(
            PipelineContext(context),
            PipelineIndicator().set_run_again()
        )
    def _set_run_next_output(self, context):
        return PipelineActionOutput(PipelineContext(context))

    def _set_over_output(self, context, output=None):
        return PipelineActionOutput(
            PipelineContext(context),
            PipelineIndicator().set_over(),
            output=output
        )

    def _set_jump_output(self, context, action_name):
        return PipelineActionOutput(
            PipelineContext(context),
            PipelineIndicator(),
            Name(action_name)
        )

def combine_commands(
    commands: List[CommandSettingDetail],
    code: Optional[str] = None
)->Tuple[List[CommandSettingDetail], Number, str]:
    timeout = Number(sum([c.timeout.get_value() for c in commands]))
    commands = [c.command.get_value() for c in commands]
    if code is None:
        code = get_random_string(10)
    tmpfile = get_random_string(10)
    commands.extend([f'echo $?>/tmp/{code} || echo $?>/tmp/{code}', 'sleep 600', f'rm /tmp/{code} &'])
    command_str = ' && '.join(commands)
    command = f"echo '{command_str}'>{tmpfile}"
    return [
        CommandSettingDetail(Command(command)),
        CommandSettingDetail(Command(f'nohup /bin/bash {tmpfile} >/dev/null 2>&1')),
        CommandSettingDetail(Command(f'rm {tmpfile}'))
    ], timeout, code

def get_check_commands(code: str)->List[CommandSettingDetail]:
    commands = [
        CommandSettingDetail(Command(f'cat /tmp/{code}'))
    ]
    return commands


@retry(tries=2, delay=0.5)
def send_request(command_repo: CommandRepository, request: CommandRequest):
    return command_repo.send_request(request)


@retry(tries=2, delay=0.5)
def find_item(command_repo: CommandRepository, request_id: CommandID)->CommandItem:
    return command_repo.find_item(request_id)
 
    
class HeavyCommandPipelineGenerator(PipelineGenerator):
    def __init__(
        self, 
        command_repo: CommandRepository,
        hosts: List[CommandHost],
        commands: List[CommandSettingDetail],
        priority: CommandPriority=CommandPriority(3),
        check_interval: float=5,
        timeout: float=50,
        allow_failure_num: int=10,
    ) -> None:
        self.context = PipelineContext(
            {
                'command_repo': command_repo,
                'hosts': hosts,
                'commands': commands,
                'priority': priority,
                'check_interval': check_interval,
                'timeout': timeout,
                'allow_failure_num': allow_failure_num,
                'failure_num': 0
            }
        )


    def send_request(self, context:PipelineContext):
        context = context.get_value()
        if 'end_time' not in context:
            context['end_time'] = time.time()+context['timeout']
        commands:List[CommandSettingDetail] = context['commands']
        request_id = context.get('request_id', None)
        if request_id:
            return self._set_run_next_output(context)
        send_ips = context.get('send_ips', None)
        hosts = [h for h in context['hosts'] if h.ip in send_ips] \
                if send_ips is not None \
                else context['hosts']
        if hosts:
            commands, timeout, context['code'] = combine_commands(commands, context.get('code', None))
            request = CommandRequest(
                commands=commands,
                hosts=hosts,
                context=None,
                priority=context['priority'],
                timeout=Number(3)
            )
            _logger.debug(f'send_request: {request}')
            context['request_id'] = send_request(
                context['command_repo'], request
            ) if hosts else None
        return self._set_run_next_output(context)
        

    def check_response(self, context:PipelineContext):
        context = context.get_value()
        request_id = context['request_id']
        if not request_id:
            return self._set_run_next_output(context)
        item = find_item(context['command_repo'], request_id)
        _logger.debug(f'check_response: {item}')
        if item.details:
            check_progress_obj = [r for r in item.details if r.status.is_succeed()]
            context['send_ips'] = [r.ip for r in item.details if r not in check_progress_obj]
            if 'check_ips' in context:
                context['check_ips'].extend([r.ip for r in check_progress_obj])
            else:
                context['check_ips'] = [r.ip for r in check_progress_obj]
                context['request_id'] = None
        elif item.status.is_failed():
            context['failure_num'] += 1
            if context['failure_num']>context['allow_failure_num']:
                raise OperationError(f'Command item is failed: {item}')
            else:
                _logger.error(f'Command item is failed: {item}')
                context['request_id'] = None
        return self._set_run_next_output(context)


    def send_check_request(self, context:PipelineContext):
        context = context.get_value()
        request_id = context.get('check_request_id', None)
        check_ips = context.get('check_ips')
        if request_id or not check_ips:
            return self._set_run_next_output(context)
        hosts = [h for h in context['hosts'] if h.ip in check_ips]
        commands = get_check_commands(context['code'])
        request = CommandRequest(commands=commands,
                                hosts=hosts,
                                context=None,
                                priority=context['priority'],
                                timeout = Number(3))
        _logger.debug(f'send_check_request: {request}')
        context['check_request_id'] = send_request(context['command_repo'],request
                                    ) if hosts else None
        return self._set_run_next_output(context)
    

    def find_check_response(self, context:PipelineContext):
        context = context.get_value()
        request_id = context.get('check_request_id', None)
        if not request_id:
            return self._set_run_next_output(context)
        item = find_item(context['command_repo'], request_id)
        _logger.debug(f'find_check_response: {item}')
        if item.details:
            completed_obj = [r for r in item.details if r.status.is_succeed()]
            ret_resp = []
            for r in completed_obj:
                if r.stdout.get_value().strip()!='0':
                    r.status.set_failed()
                ret_resp.append(r)
            context['check_ips'] = [ip for ip in context['check_ips'] 
                            if ip not in [r.ip for r in completed_obj]]
            context['check_request_id'] = None
            item.details = ret_resp
            return PipelineActionOutput(
                context=PipelineContext(context),
                indicator=PipelineIndicator(),
                output=item
            )
        elif item.status.is_failed():
            context['failure_num'] += 1
            if context['failure_num']>context['allow_failure_num']:
                raise OperationError(f'Fail to check progress: {item.exception.get_value()}')
            else:
                _logger.error(f'Fail to check progress: {item.exception.get_value()}')
                context['check_request_id'] = None
            return self._set_run_next_output(context)
        else:
            return self._set_run_next_output(context)

    def sleep(self, context: PipelineContext):
        context = context.get_value()
        if time.time()>context['end_time']:
            raise OperationError(f'Timeout when execute command {context["commands"]}')
        if 'check_time' not in context:
            context['check_time'] = time.time()
        
        if time.time()>context['check_time']:
            if 'check_ips' not in context or 'send_ips' not in context:
                _logger.debug('check ips and send ips not in context keywords')
                context['check_time'] += context['check_interval']
                return self._set_run_next_output(context)
            elif context['check_ips']==[] and context['send_ips']==[]:
                _logger.debug('pipeline can be over')
                return self._set_over_output(context)
            elif context['send_ips']==[]:
                context['check_time'] += context['check_interval']
                return self._set_jump_output(context, 'send_check_request')
            else:
                _logger.debug(f"check ips:{context['check_ips']}, send ips: {context['send_ips']}")
                context['check_time'] += context['check_interval']
                return self._set_run_next_output(context)
        else:
            _logger.debug('pipeline is in sleep')
            return self._set_run_again_output(context)

    def get_output(self, output, x:List[CommandItem])->CommandItem:
        # x is all output from pipeline
        resp = []
        for item in x:
            resp.extend(item.details)
        item = x[-1]
        item.details = resp
        return item

    
    def generate_pipeline(self):
        stages = [
            _PipelineStage(stage_name='send_request', action=self.send_request),
            _PipelineStage(stage_name='check_response', action=self.check_response),
            _PipelineStage(stage_name='send_check_request', action=self.send_check_request),
            _PipelineStage(stage_name='find_check_response', action=self.find_check_response),
            _PipelineStage(stage_name='sleep', action=self.sleep)
        ]
        return CyclePipelineTemplate(stages, self.context, self.get_output)
