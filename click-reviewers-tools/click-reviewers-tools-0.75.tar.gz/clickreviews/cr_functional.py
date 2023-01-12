'''cr_functional.py: click functional'''
#
# Copyright (C) 2013-2015 Canonical Ltd.
# Copyright (C) 2021 UBports Foundation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import binascii
import os
import re
import subprocess

from apt import apt_pkg

from clickreviews.cr_common import ClickReview, open_file_read

# TODO: for QML apps, see if i18n.domain('%s') matches X-Lomiri-Gettext-Domain
#       compiled apps can use organizationName to match X-Lomiri-Gettext-Domain

# QML Import versions aligned with Ubuntu Touch framework releases
# Please keep this updated when Qt is upgraded and sorted alphabetically
QT_IMP_FRAMEWORKS = {
    'Qt.labs.folderlistmodel': [
        ('2.1', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'Qt.labs.platform': [
        ('1.0', 'ubuntu-sdk-16.04'),
    ],
    'Qt.labs.qmlmodels': [
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'Qt.labs.settings': [
        ('1.0', 'ubuntu-sdk-16.04'),
    ],
    'QtBlueTooth': [
        ('5.9', 'ubuntu-sdk-16.04'),
        ('5.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtCharts': [
        ('2.2', 'ubuntu-sdk-16.04.3'),
        ('2.3', 'ubuntu-sdk-16.04.5'),
    ],
    'QtGraphicalEffects': [
        ('1.0', 'ubuntu-sdk-16.04'),
        ('1.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtLocation': [
        ('5.9', 'ubuntu-sdk-16.04'),
        ('5.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtMultimedia': [
        ('5.9', 'ubuntu-sdk-16.04'),
        ('5.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtNfc': [
        ('5.12', 'ubuntu-sdk-16.04.6'),
    ],
    'QtPositioning': [
        ('5.9', 'ubuntu-sdk-16.04'),
        ('5.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQml': [
        ('2.3', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQml.Models': [
        ('2.3', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQml.StateMachine': [
        ('1.0', 'ubuntu-sdk-16.04'),
        ('1.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick': [
        ('2.9', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls.impl': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls.Fusion': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls.Fusion.impl': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls.Imagine': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls.Imagine.impl': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls.Material': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls.Material.impl': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls.Universal': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Controls.Universal.impl': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Dialogs': [
        ('1.2', 'ubuntu-sdk-16.04'),
        ('1.3', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Layouts': [
        ('1.3', 'ubuntu-sdk-16.04'),
        ('1.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.LocalStorage': [
        ('2.0', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Particles': [
        ('2.0', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Shapes': [
        ('1.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Templates': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.Window': [
        ('2.2', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtQuick.XmlListModel': [
        ('2.0', 'ubuntu-sdk-16.04'),
        ('2.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtSensors': [
        ('5.9', 'ubuntu-sdk-16.04'),
        ('5.11', 'ubuntu-sdk-16.04.5'),
    ],
    'QtTest': [
        ('1.2', 'ubuntu-sdk-16.04'),
        ('1.12', 'ubuntu-sdk-16.04.5'),
    ],
    'QtWebChannel': [
        ('1.0', 'ubuntu-sdk-16.04.5'),
    ],
    'QtWebEngine': [
        ('1.5', 'ubuntu-sdk-16.04'),
        ('1.7', 'ubuntu-sdk-16.04.1'),
        ('1.10', 'ubuntu-sdk-16.04.4'),
    ],
    'QtWebSockets': [
        ('1.1', 'ubuntu-sdk-16.04'),
    ],
    'QtWebView': [
        ('1.1', 'ubuntu-sdk-16.04.7'),
    ],
    'QtSystemInfo': [
        ('5.5', 'ubuntu-sdk-16.04'),
    ],

    # Additional modules not from Qt directly
    'QtQuick.Controls.Suru': [
        ('2.2', 'ubuntu-sdk-16.04'),
    ],
}

# A dictionary of Qt release series coupled with Ubuntu Touch framework
QT_MIN_FRAMEWORKS = {
    '5.9': 'ubuntu-sdk-16.04',
    '5.12': 'ubuntu-sdk-16.04.5',
}


class ClickReviewFunctional(ClickReview):
    '''This class represents click lint reviews'''
    def __init__(self, fn, overrides=None):
        ClickReview.__init__(self, fn, "functional", overrides=overrides)
        if not self.is_click and not self.is_snap1:
            return

        self.qml_files = []
        for i in self.pkg_files:
            if i.endswith(".qml"):
                self.qml_files.append(i)

        self._list_all_compiled_binaries()

    def check_applicationName(self):
        '''Check applicationName matches click manifest'''
        if not self.is_click and not self.is_snap1:
            return

        if self.manifest is None:
            return

        t = 'info'
        n = self._get_check_name('qml_applicationName_matches_manifest')
        s = "OK"
        link = None

        # find file with MainView in the QML
        mv = r'\s*MainView\s*(\s+{)?'
        pat_mv = re.compile(r'\n%s' % mv)
        qmls = dict()

        for i in self.qml_files:
            qml = open_file_read(i).read()
            if pat_mv.search(qml):
                qmls[i] = qml

        # LP: #1256841 - QML apps with C++ using QSettings shouldn't
        # typically set applicationName in the QML
        for i in self.pkg_bin_files:
            f = open(i, 'rb')
            data = str(binascii.b2a_qp(f.read()))
            f.close()
            if 'QSettings' in data:
                s = "OK (binary uses QSettings)"
                self._add_result(t, n, s)
                return

        if len(self.qml_files) == 0:
            s = "OK (not QML)"
            self._add_result(t, n, s)
            return
        elif len(qmls) == 0:
            s = "SKIP: could not find MainView in QML files"
            self._add_result(t, n, s)
            return

        pat_mvl = re.compile(r'^%s' % mv)
        pat_appname = re.compile(r'^\s*applicationName\s*:\s*["\']')

        ok = False
        appnames = dict()
        for k in qmls.keys():
            in_mainview = False
            for line in qmls[k].splitlines():
                if in_mainview and pat_appname.search(line):
                    appname = line.split(':', 1)[1].strip('"\' \t\n\r\f\v;')
                    appnames[os.path.relpath(k, self.unpack_dir)] = appname
                    if appname == self.click_pkgname:
                        ok = True
                        break
                elif pat_mvl.search(line):
                    in_mainview = True
                if ok:
                    break

        if len(appnames) == 0 or not ok:
            if len(self.pkg_bin_files) == 0:
                t = "warn"
                link = ('http://askubuntu.com/questions/417371/'
                        'what-does-functional-qml-applicationname-matches-'
                        'manifest-mean/417372')

            if len(appnames) == 0:
                s = "could not find applicationName in: %s" % \
                    ", ".join(sorted(list(map(
                        lambda x: os.path.relpath(x, self.unpack_dir), qmls))))
            else:  # not ok
                s = "click manifest name '%s' not found in: " % \
                    self.click_pkgname + "%s" % \
                    ", ".join(sorted(list(map(
                        lambda x: "%s ('%s')" % (x, appnames[x]), appnames))))

            if len(self.pkg_bin_files) == 0:
                s += ". Application may not work properly when confined."
            else:
                s += ". May be ok (detected as compiled application)."

        self._add_result(t, n, s, link)

    def check_qtwebkit(self):
        '''Check that QML applications don't use QtWebKit'''
        if not self.is_click and not self.is_snap1:
            return

        t = 'info'
        n = self._get_check_name('qml_application_uses_QtWebKit')
        s = "OK"
        link = None

        qmls = []
        pat_mv = re.compile(r'\n\s*import\s+QtWebKit')
        for i in self.qml_files:
            qml = open_file_read(i).read()
            if pat_mv.search(qml):
                qmls.append(os.path.relpath(i, self.unpack_dir))

        if len(qmls) > 0:
            t = 'warn'
            s = "Found files that use unsupported QtWebKit (should use " + \
                "UbuntuWebview (Ubuntu.Components.Extras.Browser >= " + \
                "0.2) or Oxide instead): %s" % " ,".join(qmls)
            link = ("http://askubuntu.com/questions/417342/what-does-"
                    "functional-qml-application-uses-qtwebkit-mean/417343")

        self._add_result(t, n, s, link)

        t = 'info'
        n = self._get_check_name('qml_application_uses_UbuntuWebView_0.2')
        s = "OK"
        link = None

        if self.manifest is not None and \
                self.manifest['framework'] == "ubuntu-sdk-13.10":
            s = "SKIPPED (Oxide not available in ubuntu-sdk-13.10)"
        else:
            qmls = []
            pat_mv = re.compile(r'\n\s*import\s+Ubuntu\.Components\.Extras\.'
                                r'Browser\s+0\.1\s*\n')
            for i in self.qml_files:
                qml = open_file_read(i).read()
                if pat_mv.search(qml):
                    qmls.append(os.path.relpath(i, self.unpack_dir))

            if len(qmls) > 0:
                t = 'warn'
                s = "Found files that use unsupported QtWebKit via " + \
                    "'Ubuntu.Components.Extras.Browser 0.1' (should use " + \
                    "Ubuntu.Components.Extras.Browser >= 0.2 or " + \
                    "Oxide instead): %s" % " ,".join(qmls)
                link = ("http://askubuntu.com/questions/417342/what-does-"
                        "functional-qml-application-uses-qtwebkit-mean/417343")

        self._add_result(t, n, s, link)

    def check_friends(self):
        '''Check that QML applications don't use deprecated Friends API'''
        if not self.is_click and not self.is_snap1:
            return

        t = 'info'
        n = self._get_check_name('qml_application_uses_friends')
        s = "OK"
        link = None

        qmls = []
        pat_mv = re.compile(r'\n\s*import\s+Friends')
        for i in self.qml_files:
            qml = open_file_read(i).read()
            if pat_mv.search(qml):
                qmls.append(os.path.relpath(i, self.unpack_dir))

        if len(qmls) > 0:
            t = 'error'
            s = "Found files that use deprecated Friends API: %s" % \
                " ,".join(qmls)
            link = ("http://askubuntu.com/questions/497551/what-does-"
                    "functional-qml-application-uses-friends-mean")

        self._add_result(t, n, s, link)

    def _validate_qml_import_versions(self, frameworks, qml):
        '''Validate a QML import version against available frameworks'''
        pat_imp = re.compile(r'^\s*import (Qt[\w\.]+) ([0-9\.]+)(.*)?')
        valid = True
        for match in pat_imp.findall(str(qml)):
            min_fws = {}
            try:
                min_fws = QT_IMP_FRAMEWORKS[match[0]]
            except KeyError:
                t = 'warn'
                n = self._get_check_name('qt_qml_import_unknown')
                s = 'Unsupported Qt module import of `%s`' % (match[0])
                link = None
                self._add_result(t, n, s, link)
                continue

            min_ver = None
            for item in min_fws:
                if apt_pkg.version_compare(match[1], item[0]) <= 0:
                    min_ver = item[1]
                    break

            if min_ver is None:
                continue

            for fw in frameworks:
                if apt_pkg.version_compare(fw, min_ver) < 0:
                    valid = False
                    break
        return valid

    def check_qt_qml_import_versions(self):
        '''Check that Qt/QML applications use a new framework version.'''
        if not self.is_click:
            return

        t = 'info'
        n = self._get_check_name('qt_qml_import_versions_framework')
        s = "OK"
        link = None

        frameworks = self.manifest['framework'].split(',')

        files = []
        for i in self.qml_files:
            qml = open_file_read(i).read()
            if not self._validate_qml_import_versions(frameworks, qml):
                files.append(os.path.relpath(i, self.unpack_dir))

        for binary in self.pkg_bin_files:
            qml = subprocess.run(['strings', binary], stdout=subprocess.PIPE).stdout
            if not self._validate_qml_import_versions(frameworks, qml):
                files.append(os.path.relpath(binary, self.unpack_dir))

        if len(files) > 0:
            t = 'error'
            s = 'Files contain QML imports too new for framework used: %s' % ','.join(files)
            self._add_result(t, n, s, link)

    def check_qt_framework(self):
        '''Check that Qt/QML applications use a new framework version.'''
        if not self.is_click:
            return

        t = 'info'
        n = self._get_check_name('qt_version_framework')
        s = "OK"
        link = None

        frameworks = self.manifest['framework'].split(',')

        pat_qt = re.compile(r'Qt_([0-9]+\.[0-9]+)')
        for binary in self.pkg_bin_files:
            qt = subprocess.run(['strings', binary], stdout=subprocess.PIPE).stdout
            # Take only the newest linked Qt version from the binary, as Qt
            # libs include all previous API versions in the major series.
            # Sort by grabbing the minor version number and converting to int
            try:
                match = sorted(pat_qt.findall(str(qt)),
                               reverse=True,
                               key=lambda minor: int(minor.split('.')[1]))[0]
                min_ver = QT_MIN_FRAMEWORKS[match]
                valid = False
                for fw in frameworks:
                    if apt_pkg.version_compare(fw, min_ver) >= 0:
                        valid = True
                        break

                if not valid:
                    t = 'error'
                    s = 'Linked Qt version too new for framework used: %s' \
                        % os.path.relpath(binary, self.unpack_dir)
                    self._add_result(t, n, s, link)
            except KeyError:
                t = 'error'
                s = 'Unsupported `%s` version of Qt used: %s' \
                    % (match, os.path.relpath(binary, self.unpack_dir))
                self._add_result(t, n, s, link)
            except IndexError:
                # This binary does not link to Qt, so continue the loop
                continue
