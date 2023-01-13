import os
import re
import logging
import glob
import sys

from . import config
from .helpers import parseYamlDict
from .helpers import runSubprocess

class Fpm:
  """ Class to handle fpm invocations """
  def __init__(self):
    self.buildDir = os.path.join(config.ali_prefix, 'sw', config.architecture)
    self.forceBuild = ['--force'] if config.force_build else []
    self.packagePrefix = "o2-"
    self.targetDir = config.target_rpm_dir
    self.skipDeps = ['openmp', 'VecGeom', 'O2-customization']  # as sometimes there's mismatch between "requires" deps and modulefile

    # Create output dir
    if not os.path.exists(self.targetDir):
        os.makedirs(self.targetDir)

    arch_split = config.architecture.split('_')
    self.architecture = arch_split[1].replace('-', '_')
    self.release_suffix = arch_split[0]

    self.runtimeDepsDict = parseYamlDict(os.path.join(config.work_dir, 'runtime.' + self.release_suffix + '.yaml'))
    self.develDepsDict = parseYamlDict(os.path.join(config.work_dir, 'devel.' + self.release_suffix + '.yaml'))

    if config.tag_version:
        self.release_suffix += '_' + config.release_tag.replace('/', '_')

  def run(self, name, version, deps, devel_deps, extra_deps, RPMS_GENERATED = []):
    """ Prepares arguments and executes fpm """
    fullVersion = version
    version = version.replace('local', '', 1)
    # Handle not standard versions, nightly, latest-o2-dataflow
    if 'latest' in version:
        iterationArg = ['--iteration', self.release_suffix]
    elif version.count('-') > 1:
        version_split = version.split('-')
        iterationArg = ['--iteration', version_split.pop() + '.' + self.release_suffix]
        if name == 'O2' and (version_split[0] == 'daily' or version_split[0] == 'nightly'):
            version_split.pop(0)
        version = '_'.join(version_split)
    else:
        version_split = version.split('-', 1)
        version = version_split[0]
        iterationArg = ['--iteration', version_split[1].replace('-', '_') + '.' + self.release_suffix]

    rpmType = 'dir'
    # prep dir arguments
    # `=.` is necessary so that the complete source dir path
    # is not replicated and the target dir consists of only
    # prefix + package name + dir
    package_dir = self.buildDir + "/" + name + "/" + fullVersion + "/"
    subdirs = ['bin', 'lib', 'lib64', 'etc', 'include', 'bin-safe', 'libexec', 'WebDID', 'share', 'plugins', 'cmake', 'sbin', 'icons', 'fonts']
    paths = []
    for subdir in subdirs:
        if os.path.exists(package_dir + subdir):
            if subdir == 'etc' and os.listdir(package_dir + subdir) == ['modulefiles', 'profile.d']:
                continue
            paths.append(package_dir + subdir + '=.')

    # if there are not dirs change RPM type to 'empty'
    if not paths:
        rpmType = 'empty'

    logging.info('Processing %s version %s:\n' \
                 ' - deps: %s\n - extra deps: %s\n - devel deps: %s\n' \
                 % (name, version, list(deps.items()), extra_deps, list({**devel_deps, **self.convertDepsToDevel(deps)}.items())))

    # Handle extra_deps
    extra_deps = [v for dep in extra_deps for v in ('--depends', dep.replace('local', '', 1))]

    # Handle install_path
    install_path = '/opt/o2/'
    if name == 'mesos':
        install_path = '/usr/'

    packageName = self.packagePrefix + name
    fpmCommand = ['fpm',
      '-s', rpmType,
      '-t', 'rpm',
      '--log', 'warn',
      *self.translateDepsToArgs(deps),
      *extra_deps,
      *self.forceBuild,
      '-p', self.targetDir,
      '--architecture', self.architecture,
      '--prefix', install_path,
      '-n', packageName,
      '--version', version,
      *iterationArg,
      '--no-rpm-auto-add-directories',
      '--template-scripts',
      '--after-install', os.path.join(config.work_dir, 'after_install_template.sh'),
      '--after-remove', os.path.join(config.work_dir, 'after_remove_template.sh'),
      '--vendor', 'ALICE FLP',
      '--url', 'https://alice-flp.docs.cern.ch',
      '--maintainer', 'Adam Wegrzynek <adam.wegrzynek@cern.ch>',
      '--license', 'GPL-3.0']

    if paths:
        fpmCommand.extend(['--exclude=*/modulefiles', '--exclude=*/profile.d', '--exclude=*/info/dir', '--exclude=*/version'])
        fpmCommand.extend(paths)

    develPackageName = packageName + '-devel'
    fpmCommandDevel = ['fpm',
      '-s', 'empty',
      '-t', 'rpm',
      '--log', 'warn',
      '--architecture', self.architecture,
      '--prefix', '/opt/o2/',
      '-n', develPackageName,
      '--version', version,
      '-p', self.targetDir,
      *iterationArg,
      '--template-scripts',
      '--after-install', os.path.join(config.work_dir, 'after_install_template.sh'),
      '--after-remove', os.path.join(config.work_dir, 'after_remove_template.sh'),
      *self.translateDevelDepsToArgs(deps),
      *self.translateDevelDepsToArgs(devel_deps),
      *self.translateDepsToArgs(self.convertDepsToDevel(deps))
    ]

    if not config.dry_run:
      self.generateRpm(packageName, fpmCommand, RPMS_GENERATED)
      if config.devel:
          self.generateRpm(develPackageName, fpmCommandDevel, RPMS_GENERATED)
    else:
      print(*fpmCommand)
      if config.devel:
          print(*fpmCommandDevel)
      return ''

  # Remove system deps and append -devel to names
  def convertDepsToDevel(self, deps):
        return {name+'-devel':version for name, version in deps.items() if version != 'from_system'}

  # Run subprocess to generate RPM
  def generateRpm(self, name, command, RPMS_GENERATED):
      logging.info('Generating RPM: %s', name)
      ret = runSubprocess(command, failOnError=False)
      if not ret:
          logging.warn('Generation of the RPM skipped')
      else:
          # try to parse the generated RPM path from the fpm output
          match = re.search(':path=>\"(.*)\"}', ret)
          generatedRpmPath = match.group(1) if match else ''
          RPMS_GENERATED.append(generatedRpmPath)

  # Convert map name:version to fpm compatible command line params
  def translateDevelDepsToArgs(self, deps):
    depsArg = []
    for name, version in deps.items():
        if name not in self.skipDeps:
            if name in self.develDepsDict:
                for dep in self.develDepsDict.get(name):
                    depsArg.extend(['--depends', dep])
            else:
                depsArg.extend(['--depends', self.packagePrefix + name])
    return depsArg

  # Convert map name:version to fpm compatible command line params
  def translateDepsToArgs(self, deps):
    """ Prepares dependency arguments for fpm """
    depsArg = []
    for depName, depVersion in deps.items():
      if depName not in self.skipDeps:
        if (depVersion != "from_system"):
          depVersion = self.stripDashes(depVersion)

          # Handle "nightly", "daily" prefixes in O2
          if depName == 'O2':
            version_split = depVersion.split('_')
            if version_split[0] == 'daily' or version_split[0] == 'nightly':
              version_split.pop(0)
              depVersion = version = '_'.join(version_split)

          depsArg.extend(['--depends', self.packagePrefix + depName + ' >= ' + depVersion])
        else:  # coming from system, get name from dict
          if depName not in self.runtimeDepsDict:
            logging.critical('Could not find system dependency: %s \nDoes it suppose to come from aliBuild?' % (depName))
            sys.exit(1)
          for dep in self.runtimeDepsDict.get(depName):
            depsArg.extend(['--depends', dep])
    return depsArg

  def stripDashes(self, version):
      """ Replaces last dash with underscore, execpt last one """
      version = version.replace('local', '', 1)
      if version.count('-') > 1:
          version_split = version.split('-')
          release = version_split.pop()
          return '_'.join(version_split) + '-' + release
      else:
          return version

  def validateRpms(self):
      """ Validates the generated RPMs by running a dry yum install """

      # get the actual RPM paths to pass to yum and avoid subprocess using shell
      rpmPaths = glob.glob(os.path.join(config.target_rpm_dir, '*.rpm'))
      if rpmPaths == []:
          logging.error("No RPMs found under %s, exiting", config.target_rpm_dir)
          return
      logging.info("Validating the RPMs under %s (will ask for sudo))", config.target_rpm_dir)
      logging.debug("RPMs: \n%s", '\n'.join(rpmPaths))
      yumCommand = ['sudo', 'yum', '-y', 'install',
                    *rpmPaths,
                    '--setopt', 'tsflags=test',
                    '--setopt', 'skip_missing_names_on_install=False']
      if config.dry_run:
          print(*yumCommand)
      else:
          runSubprocess(yumCommand)
