from remotemanager.connection.computers.base import BaseComputer, \
    required, optional


class Example_Torque(BaseComputer):
    """
    example class for connecting to a remote computer using a torque scheduler
    """

    def __init__(self, **kwargs):

        if 'host' not in kwargs:
            kwargs['host'] = 'remote.address.for.connection'

        super().__init__(**kwargs)

        self.submitter = 'qsub'
        self.shebang = '#!/bin/bash'
        self.pragma = '#PBS'

        self.mpi = required('ppn')
        self.omp = required('omp')
        self.nodes = required('nodes')
        self.queue = required('-q')
        self.walltime = required('walltime')
        self.name = optional('-N')
        self.outfile = optional('-o')
        self.errfile = optional('-e')

        self.modules = ['python3']

    @property
    def ssh(self):
        """
        Returns (str):
            modified ssh string for Summer avoiding perl error
        """
        return 'LANG=C ' + super().ssh

    @property
    def postscript(self):

        return f"""
cd $PBS_O_WORKDIR
export OMP_NUM_THREADS={self.omp}
"""

    def resources_block(self, **kwargs):

        self.update_resources(**kwargs)

        if not self.valid:
            raise RuntimeError(f'missing required arguments: {self.missing}')

        outfile = self.outfile.value or f'{self.name}-stdout'
        errfile = self.errfile.value or f'{self.name}-stderr'

        options = {'-N': self.name.value,
                   '-q': self.queue.value,
                   '-o': outfile,
                   '-e': errfile,
                   '-l': f'nodes={self.nodes.value}:'
                         f'ppn={self.mpi.value},'
                         f'walltime={self.walltime.value}'}

        return [f'{self.pragma} {k} {v}' for k, v in options.items()]


class Example_Slurm(BaseComputer):
    """
    example class for connecting to a remote computer using a slurm scheduler
    """

    def __init__(self, **kwargs):

        if 'host' not in kwargs:
            kwargs['host'] = 'remote.address.for.connection'

        super().__init__(**kwargs)

        self.submitter = 'sbatch'
        self.shebang = '#!/bin/bash'
        self.pragma = '#SBATCH'

        self.mpi = required('--ntasks')
        self.omp = required('--cpus-per-task')
        self.nodes = required('--nodes')
        self.queue = required('--queue')
        self.walltime = required('--walltime')
        self.jobname = optional('--job-name')
        self.outfile = optional('--output')
        self.errfile = optional('--error')

        self.modules = ['python3']
