# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""Test model coverage for a given CLI."""

import os
import unittest2 as unittest
import lxml.etree as et
from yscoverage.coverage import (
    generate_coverage,
    YangCoverage,
    YangCoverageException
)
from yscoverage.get2edit import GetToEdit


rpc_reply = """<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:818bd355-a026-4bcf-9579-e368c083d5c8" \
xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <network-instances xmlns="http://openconfig.net/yang/network-instance">
      <network-instance>
        <name>default</name>
        <config>
          <enabled>true</enabled>
          <name>default</name>
          <type>DEFAULT_INSTANCE</type>
          <mtu>9216</mtu>
        </config>
        <fdb>
          <config>
            <mac-aging-time>1800</mac-aging-time>
            <mac-learning>true</mac-learning>
            <maximum-entries>196000</maximum-entries>
          </config>
        </fdb>
        <vlans>
          <vlan>
            <vlan-id>1</vlan-id>
            <config>
              <status>ACTIVE</status>
              <vlan-id>1</vlan-id>
            </config>
          </vlan>
        </vlans>
      </network-instance>
    </network-instances>
  </data>
</rpc-reply>"""


class TestCoverage(unittest.TestCase):
    """Tests for model coverage."""

    testdir = os.path.join(os.path.dirname(__file__), 'data')

    def test_gen_no_text(self):
        """Raise an exception if no text is sent."""
        with self.assertRaises(YangCoverageException):
            generate_coverage()

    def test_gen_no_url(self):
        """Raise an exception if no URL is sent."""
        with self.assertRaises(YangCoverageException):
            generate_coverage(text='text')

    def test_get_config_bad_device(self):
        """Raise an exception if device is invalid."""
        with self.assertRaises(YangCoverageException):
            YangCoverage.get_config('blah')

    def test_get_local_releases(self):
        """Make sure dict is returned."""
        releases = YangCoverage.get_releases('xe')
        self.assertIn('releases', releases)

    def test_get_base_releases(self):
        """Make sure dict is returned."""
        releases = YangCoverage.get_releases("google.com")
        self.assertIn('releases', releases)

    def test_coverage_failed(self):
        """Only one coverage at a time allowed."""
        result = YangCoverage.get_coverage('text', 0, 'google.com')
        self.assertEqual(result, ('*** failed ***', ''))

    def test_get_to_edit(self):
        """Test conversion of get-config to edit-config."""
        g2e = GetToEdit(rpc_reply).edit_config('running')
        rpc = et.fromstring(g2e)
        self.assertTrue(rpc.tag.endswith('rpc'))
        self.assertTrue(rpc[0].tag.endswith('edit-config'))
        self.assertTrue(rpc[0][0].tag.endswith('target'))
        self.assertTrue(rpc[0][0][0].tag.endswith('running'))
        self.assertTrue(rpc[0][1].tag.endswith('config'))
        self.assertTrue(rpc[0][1][0].tag.endswith('network-instances'))

    def test_get_to_edit_no_target(self):
        """Test conversion of get-config to edit-config without target."""
        g2e = GetToEdit(rpc_reply).edit_config()
        rpc = et.fromstring(g2e)
        self.assertTrue(rpc.tag.endswith('rpc'))
        self.assertTrue(rpc[0].tag.endswith('edit-config'))
        self.assertTrue(rpc[0][0].tag.endswith('target'))
        self.assertTrue(rpc[0][0][0].tag.endswith('running'))
        self.assertTrue(rpc[0][1].tag.endswith('config'))
        self.assertTrue(rpc[0][1][0].tag.endswith('network-instances'))

    def test_get_to_edit_no_rpc(self):
        """Test conversion of invalid XML to edit-config fails properly."""
        g2e = GetToEdit('abc').edit_config()
        rpc = et.fromstring(g2e)
        self.assertTrue(rpc.tag.endswith('rpc'))
        self.assertTrue(rpc[0].tag.endswith('edit-config'))
        self.assertTrue(rpc[0][0].tag.endswith('target'))
        self.assertTrue(rpc[0][0][0].tag.endswith('running'))
        self.assertTrue(rpc[0][1].tag.endswith('config'))
        self.assertTrue(
            rpc[0][1].text.startswith('Invalid XML for rpc-reply')
        )
        self.assertTrue(rpc[0][1].text.endswith('abc'))
