from bioluigi.scheduled_external_program import ScheduledExternalProgramTask
import luigi

class Index(ScheduledExternalProgramTask):
    """Index a tabular format (VCF, TSV, etc.) using tabix utility"""
    input_file = luigi.Parameter()

    preset = luigi.ChoiceParameter(choices=['gff', 'bed', 'sam', 'vcf', 'psltbl'], positional=False)

    seq = luigi.IntParameter(positional=False)
    begin = luigi.IntParameter(positional=False)
    end = luigi.IntParameter(positional=False)
    skip_lines = luigi.IntParameter(positional=False, default=0)
    comment = luigi.Parameter(positional=False)

    def program_args(self):
        args = ['tabix']
        if self.preset:
            args.extend(['-p', self.preset])
        else:
            args.extend([
                '-s', self.seq,
                '-b', self.begin,
                '-e', self.end,
                '-c', self.comment,
                '-S', self.skip_lines])
        args.append(self.input_file)
        return args

    def output(self):
        return luigi.LocalTarget(self.input_file + '.tbi')
