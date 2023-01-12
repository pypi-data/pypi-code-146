import luigi

from ..scheduled_external_program import ScheduledExternalProgramTask

luigi.namespace('bioluigi.mirbooking', scope=__name__)

class Mirbooking(ScheduledExternalProgram):
    """
    Solve the microtargetome equilibrium given a set of targets RNAs and
    microRNAs
    """
    input_file = luigi.Parameter()
    targets_file = luigi.Parameter()
    mirnas_file = luigi.Parameter()

    cutoff = luigi.FloatParameter(default=100)

    def program_environment(self):
        env = super(Mirbooking, self).program_environment()
        env.update({'OMP_NUM_THREADS': self.cpus})
        return env

    def program_args(self):
        return ['mirbooking',
                '--targets', self.targets_file,
                '--mirnas',  self.mirnas_file,
                '--input',   self.input_file,
                '--cutoff',  self.cutoff]
