from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import ImanFile, Dataset
from typing import Dict, List


@dataclass
class FileDigestInfoResponse(TcBaseObj):
    """
    This structure contains the details about the digest information for the ImanFile objects.
    
    :var fileDigestInfo: A map (ImanFile, list of DigestInfo) of input ImanFile objects to the digest informationa for
    the file.
    :var serviceData: The ServiceData response that can contain the partial errors.
    """
    fileDigestInfo: FileDigestInfoMap = None
    serviceData: ServiceData = None


@dataclass
class FileDigestInfoSet(TcBaseObj):
    """
    This structure contains the digest information available for each of the files in the map.
    
    :var map: A map of ImanFile objects to a list of DigestInfo objects for each digest available for the file.
    """
    map: FileDigestInfoMap = None


@dataclass
class DatasetDigestInfoResponse(TcBaseObj):
    """
    this structure contains the details about the digest information for the ImanFile objects in the Dataset objects.
    
    :var datasetDigestInfo: A list of DatasetDigestInfos objects. It contains the digest information for each file
    referenced by each of the input dataset object.
    :var serviceData: The ServiceData response that can contain the partial errors.
    """
    datasetDigestInfo: DatasetDigestInfoMap = None
    serviceData: ServiceData = None


@dataclass
class DigestInfo(TcBaseObj):
    """
    Structure containing information about an individual digest for an ImanFile object.
    
    :var digestAlgorithm: The digest algorithm used to the compute the digest for this file. This can be one of:
    - None
    - MD5
    - SHA-1
    - SHA-256
    
    
    :var digest: The digest for the file. Message digest algorithms ("digests") are widely used cryptographic hash
    functions.  Digests are utilized in a wide variety of cryptographic applications, and are also commonly used to
    verify data integrity.  FMS uses digest algorithms to produce a hash value of the contents of whole binary files,
    and expresses the hash value in text format as a hexadecimal number. An empty string is returned if no digest was
    available for the file.
    :var certainty: The certainty of the digest stored. The possible values are:
    - 0 - default for unknown or unparsable certainty values.
    - 1 - absolute certainty, a digest generated on the first generation of a file (before an FMS network transport)
    - 2 - high level of certainty, a digest generated as a file is stored in the volume (after an FMS network transport)
    - 3 - medium level of certainty, a digest generated on an existing file in a volume (sometime after the initial
    write to the server)
    - 4 - lowest level of certainty, a digest generated on the fly.
    
    """
    digestAlgorithm: str = ''
    digest: str = ''
    certainty: int = 0


"""
A map of input Dataset objects to a FileDigestInfoSet object, which contains a map of all the files referenced by the Dataset to the list of DigestInfo objects available for that file.
"""
DatasetDigestInfoMap = Dict[Dataset, FileDigestInfoSet]


"""
A map of ImanFile objects to a list of DigestInfo objects for each digest available for the file.
"""
FileDigestInfoMap = Dict[ImanFile, List[DigestInfo]]
