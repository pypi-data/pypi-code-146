#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
from dataclasses import dataclass
from typing import Any


@dataclass
class Family:
    """Tenable Family

    Returns:
        _type_: _description_
    """

    id: str
    name: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> "Family":
        """Create Family object from dict

        Args:
            obj (Any): _description_

        Returns:
            Family: _description_
        """
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _type = str(obj.get("type"))
        return Family(_id, _name, _type)


@dataclass
class Repository:
    """Tenable Repository

    Returns:
        _type_: _description_
    """

    id: str
    name: str
    description: str
    dataFormat: str

    @staticmethod
    def from_dict(obj: Any) -> "Repository":
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _description = str(obj.get("description"))
        _dataFormat = str(obj.get("dataFormat"))
        return Repository(_id, _name, _description, _dataFormat)


@dataclass
class Severity:
    id: str
    name: str
    description: str

    @staticmethod
    def from_dict(obj: Any) -> "Severity":
        """Create Severity object from dict

        Args:
            obj (Any): _description_

        Returns:
            Severity: _description_
        """
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _description = str(obj.get("description"))
        return Severity(_id, _name, _description)


@dataclass
class TenableAsset:
    """Tenable Asset

    Returns:
        _type_: _description_
    """

    pluginID: str
    severity: Severity
    hasBeenMitigated: str
    acceptRisk: str
    recastRisk: str
    ip: str
    uuid: str
    port: str
    protocol: str
    pluginName: str
    firstSeen: str
    lastSeen: str
    exploitAvailable: str
    exploitEase: str
    exploitFrameworks: str
    synopsis: str
    description: str
    solution: str
    seeAlso: str
    riskFactor: str
    stigSeverity: str
    vprScore: str
    vprContext: str
    baseScore: str
    temporalScore: str
    cvssVector: str
    cvssV3BaseScore: str
    cvssV3TemporalScore: str
    cvssV3Vector: str
    cpe: str
    vulnPubDate: str
    patchPubDate: str
    pluginPubDate: str
    pluginModDate: str
    checkType: str
    version: str
    cve: str
    bid: str
    xref: str
    pluginText: str
    dnsName: str
    macAddress: str
    netbiosName: str
    operatingSystem: str
    ips: str
    recastRiskRuleComment: str
    acceptRiskRuleComment: str
    hostUniqueness: str
    acrScore: str
    keyDrivers: str
    uniqueness: str
    family: Family
    repository: Repository
    pluginInfo: str
    count: int

    # 'uniqueness': 'repositoryID,ip,dnsName'
    # Enable object to be hashable
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return (
            self.dnsName == other.dnsName
            and self.macAddress == other.macAddress
            and self.ip == other.ip
            and self.repository.name == other.respository.name
        )

    @staticmethod
    def from_dict(obj: Any) -> "TenableAsset":
        """Create TenableAsset object from dict

        Args:
            obj (Any): _description_

        Returns:
            TenableAsset: _description_
        """
        _pluginID = str(obj.get("pluginID"))
        _severity = Severity.from_dict(obj.get("severity"))
        _hasBeenMitigated = str(obj.get("hasBeenMitigated"))
        _acceptRisk = str(obj.get("acceptRisk"))
        _recastRisk = str(obj.get("recastRisk"))
        _ip = str(obj.get("ip"))
        _uuid = str(obj.get("uuid"))
        _port = str(obj.get("port"))
        _protocol = str(obj.get("protocol"))
        _pluginName = str(obj.get("pluginName"))
        _firstSeen = str(obj.get("firstSeen"))
        _lastSeen = str(obj.get("lastSeen"))
        _exploitAvailable = str(obj.get("exploitAvailable"))
        _exploitEase = str(obj.get("exploitEase"))
        _exploitFrameworks = str(obj.get("exploitFrameworks"))
        _synopsis = str(obj.get("synopsis"))
        _description = str(obj.get("description"))
        _solution = str(obj.get("solution"))
        _seeAlso = str(obj.get("seeAlso"))
        _riskFactor = str(obj.get("riskFactor"))
        _stigSeverity = str(obj.get("stigSeverity"))
        _vprScore = str(obj.get("vprScore"))
        _vprContext = str(obj.get("vprContext"))
        _baseScore = str(obj.get("baseScore"))
        _temporalScore = str(obj.get("temporalScore"))
        _cvssVector = str(obj.get("cvssVector"))
        _cvssV3BaseScore = str(obj.get("cvssV3BaseScore"))
        _cvssV3TemporalScore = str(obj.get("cvssV3TemporalScore"))
        _cvssV3Vector = str(obj.get("cvssV3Vector"))
        _cpe = str(obj.get("cpe"))
        _vulnPubDate = str(obj.get("vulnPubDate"))
        _patchPubDate = str(obj.get("patchPubDate"))
        _pluginPubDate = str(obj.get("pluginPubDate"))
        _pluginModDate = str(obj.get("pluginModDate"))
        _checkType = str(obj.get("checkType"))
        _version = str(obj.get("version"))
        _cve = str(obj.get("cve"))
        _bid = str(obj.get("bid"))
        _xref = str(obj.get("xref"))
        _pluginText = str(obj.get("pluginText"))
        _dnsName = str(obj.get("dnsName"))
        _macAddress = str(obj.get("macAddress")).upper()
        _netbiosName = str(obj.get("netbiosName"))
        _operatingSystem = str(obj.get("operatingSystem"))
        _ips = str(obj.get("ips"))
        _recastRiskRuleComment = str(obj.get("recastRiskRuleComment"))
        _acceptRiskRuleComment = str(obj.get("acceptRiskRuleComment"))
        _hostUniqueness = str(obj.get("hostUniqueness"))
        _acrScore = str(obj.get("acrScore"))
        _keyDrivers = str(obj.get("keyDrivers"))
        _uniqueness = str(obj.get("uniqueness"))
        _family = Family.from_dict(obj.get("family"))
        _repository = Repository.from_dict(obj.get("repository"))
        _pluginInfo = str(obj.get("pluginInfo"))
        if obj.get("count") is not None:
            _count = int(obj.get("count"))
        else:
            _count = 0
        return TenableAsset(
            pluginID=_pluginID,
            severity=_severity,
            hasBeenMitigated=_hasBeenMitigated,
            acceptRisk=_acceptRisk,
            recastRisk=_recastRisk,
            ip=_ip,
            uuid=_uuid,
            port=_port,
            protocol=_protocol,
            pluginName=_pluginName,
            firstSeen=_firstSeen,
            lastSeen=_lastSeen,
            exploitAvailable=_exploitAvailable,
            exploitEase=_exploitEase,
            exploitFrameworks=_exploitFrameworks,
            synopsis=_synopsis,
            description=_description,
            solution=_solution,
            seeAlso=_seeAlso,
            riskFactor=_riskFactor,
            stigSeverity=_stigSeverity,
            vprScore=_vprScore,
            vprContext=_vprContext,
            baseScore=_baseScore,
            temporalScore=_temporalScore,
            cvssVector=_cvssVector,
            cvssV3BaseScore=_cvssV3BaseScore,
            cvssV3TemporalScore=_cvssV3TemporalScore,
            cvssV3Vector=_cvssV3Vector,
            cpe=_cpe,
            vulnPubDate=_vulnPubDate,
            patchPubDate=_patchPubDate,
            pluginPubDate=_pluginPubDate,
            pluginModDate=_pluginModDate,
            checkType=_checkType,
            version=_version,
            cve=_cve,
            bid=_bid,
            xref=_xref,
            pluginText=_pluginText,
            dnsName=_dnsName,
            macAddress=_macAddress,
            netbiosName=_netbiosName,
            operatingSystem=_operatingSystem,
            ips=_ips,
            recastRiskRuleComment=_recastRiskRuleComment,
            acceptRiskRuleComment=_acceptRiskRuleComment,
            hostUniqueness=_hostUniqueness,
            acrScore=_acrScore,
            keyDrivers=_keyDrivers,
            uniqueness=_uniqueness,
            family=_family,
            repository=_repository,
            pluginInfo=_pluginInfo,
            count=_count,
        )
