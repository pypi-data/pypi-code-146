from enum import Enum

class HybridSolverConnectionType(Enum):
	CLOUD = 0
	LOCAL = 1

class HybridSolverServers(Enum):
    PROD = "https://api.quantagonia.com"
    STAGING = "https://staging.quantagonia.com"
    DEV = "https://dev.quantagonia.com"
    DEV3 = "https://dev3.quantagonia.com"
    LOCAL = "http://localhost:8088"

class HybridSolverOptSenses(Enum):
        MAXIMIZE = "MAXIMIZE"
        MINIMIZE = "MINIMIZE"
