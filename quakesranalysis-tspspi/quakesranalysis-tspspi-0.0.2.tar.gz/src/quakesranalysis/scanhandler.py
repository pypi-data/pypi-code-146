import numpy as np

def load_npz(filename):
    data = np.load(filename)
    if "scan" not in data:
        return QUAKESRScan.load(filename)
    else:
        return QUAKESRScan1D.load(filename)

class QUAKESRScan:
    @staticmethod
    def load(filename):
        # Loads a single scan from an NPZ
        mainAxis = None
        mainAxisTitle = None
        sigI = None
        sigQ = None
        sigIZero = None
        sigQZero = None

        data = np.load(filename)
        if "f_RF" in data:
            mainAxis = "f_RF"
            mainAxisTitle = "RF frequency"
        else:
            raise ValueError("Unsupported scan type (not a frequency scan)")

        sigI = data["sigI"]
        sigQ = data["sigQ"]
        
        if "sigIzero" in data:
            sigIZero = data["sigIzero"]
            sigQZero = data["sigQzero"]

        return QUAKESRScan(data[mainAxis], mainAxis, mainAxisTitle, sigI, sigQ, sigIZero, sigQZero, filename)

    def __init__(self, mainAxisData, mainAxis, mainAxisTitle, sigI, sigQ, sigIZero = None, sigQZero = None, filename = None):
        self._main_axis_data = mainAxisData
        self._main_axis = mainAxis
        self._main_axis_title = mainAxisTitle

        self._sigI = sigI
        self._sigQ = sigQ

        self._sigI_Mean = None
        self._sigI_Std = None
        self._sigQ_Mean = None
        self._sigQ_Std = None
        self._sig_Amp = None
        self._sig_Phase = None

        self._sigIZero = sigIZero
        self._sigQZero = sigQZero

        self._sigIZero_Mean = None
        self._sigIZero_Std = None
        self._sigQZero_Mean = None
        self._sigQZero_Std = None
        self._sigZero_Amp = None
        self._sigZero_Phase = None

        self._sigIDiff_Mean = None
        self._sigIDiff_Std = None
        self._sigQDiff_Mean = None
        self._sigQDiff_Std = None
        self._sigDiff_Amp = None
        self._sigDiff_Phase = None

        self._filename = filename

    def get_scans(self):
        return [ self ]

    def get_main_axis_title(self):
        return self._main_axis_title

    def get_main_axis_symbol(self):
        return self._main_axis

    def get_main_axis_data(self):
        return self._main_axis_data
        
    def get_raw_signal_iq(self):
        return self._sigI, self._sigQ
    def get_raw_zero_iq(self):
        return self._sigIZero, self._sigQZero

    def get_signal_mean_iq(self):
        if self._sigI_Mean is not None:
            return self._sigI_Mean, self._sigI_Std, self._sigQ_Mean, self._sigQ_Std

        self._sigI_Mean = np.zeros(self._main_axis_data.shape)
        self._sigQ_Mean = np.zeros(self._main_axis_data.shape)
        self._sigI_Std = np.zeros(self._main_axis_data.shape)
        self._sigQ_Std = np.zeros(self._main_axis_data.shape)
        
        for i in range(len(self._main_axis_data)):
            self._sigI_Mean[i] = np.mean(self._sigI[i])
            self._sigQ_Mean[i] = np.mean(self._sigQ[i])
            self._sigI_Std[i] = np.std(self._sigI[i])
            self._sigQ_Std[i] = np.std(self._sigQ[i])

        return self._sigI_Mean, self._sigI_Std, self._sigQ_Mean, self._sigQ_Std

    def get_signal_ampphase(self):
        if self._sig_Amp is not None:
            return self._sig_Amp, self._sig_Phase

        if self._sigI_Mean is None:
            # Generate mean and standard deviations
            _, _, _, _ = self.get_signal_mean_iq()

        self._sig_Amp = np.sqrt(self._sigI_Mean * self._sigI_Mean + self._sigQ_Mean * self._sigQ_Mean)
        self._sig_Phase = np.arctan(self._sigQ_Mean / self._sigI_Mean)

        return self._sig_Amp, self._sig_Phase

    def get_zero_mean_iq(self):
        if self._sigIZero is None:
            # This has not been a diffscan ...
            return None, None, None, None

        if self._sigIZero_Mean is not None:
            return self._sigIZero_Mean, self._sigIZero_Std, self._sigQZero_Mean, self._sigQZero_Std

        self._sigIZero_Mean = np.zeros(self._main_axis_data.shape)
        self._sigQZero_Mean = np.zeros(self._main_axis_data.shape)
        self._sigIZero_Std = np.zeros(self._main_axis_data.shape)
        self._sigQZero_Std = np.zeros(self._main_axis_data.shape)
        
        for i in range(len(self._main_axis_data)):
            self._sigIZero_Mean[i] = np.mean(self._sigIZero[i])
            self._sigQZero_Mean[i] = np.mean(self._sigQZero[i])
            self._sigIZero_Std[i] = np.std(self._sigIZero[i])
            self._sigQZero_Std[i] = np.std(self._sigQZero[i])

        return self._sigIZero_Mean, self._sigIZero_Std, self._sigQZero_Mean, self._sigQZero_Std

    def get_zero_ampphase(self):
        if self._sigIZero is None:
            # This has not been a diffscan ...
            return None, None

        if self._sigZero_Amp is not None:
            return self._sigZero_Amp, self._sigZero_Phase

        if self._sigIZero_Mean is None:
            # Generate mean and standard deviations
            _, _, _, _ = self.get_zero_mean_iq()

        self._sigZero_Amp = np.sqrt(self._sigIZero_Mean * self._sigIZero_Mean + self._sigQZero_Mean * self._sigQZero_Mean)
        self._sigZero_Phase = np.arctan(self._sigQZero_Mean / self._sigIZero_Mean)

        return self._sigZero_Amp, self._sigZero_Phase

    def get_diff_mean_iq(self):
        if self._sigIZero is None:
            # This has not been a diffscan ...
            return None, None, None, None

        if self._sigIDiff_Mean is not None:
            return self._sigIDiff_Mean, self._sigIDiff_Std, self._sigQDiff_Mean, self._sigQDiff_Std

        # Ensure means are available ...
        _, _, _, _ = self.get_signal_mean_iq()
        _, _, _, _ = self.get_zero_mean_iq()

        self._sigIDiff_Mean = self._sigIZero_Mean - self._sigI_Mean
        self._sigQDiff_Mean = self._sigQZero_Mean - self._sigQ_Mean
        self._sigIDiff_Std = np.sqrt(self._sigIZero_Std * self._sigIZero_Std + self._sigI_Std * self._sigI_Std)
        self._sigQDiff_Std = np.sqrt(self._sigQZero_Std * self._sigQZero_Std + self._sigQ_Std * self._sigQ_Std)

        return self._sigIDiff_Mean, self._sigIDiff_Std, self._sigQDiff_Mean, self._sigQDiff_Std

    def get_diff_ampphase(self):
        if self._sigIZero is None:
            # This has not been a diffscan ...
            return None, None

        if self._sigDiff_Amp is not None:
            return self._sigDiff_Amp, self._sigDiff_Phase

        # Make sure our means are present
        _, _, _, _ = self.get_diff_mean_iq()

        self._sigDiff_Amp = np.sqrt(self._sigIDiff_Mean * self._sigIDiff_Mean + self._sigQDiff_Mean * self._sigQDiff_Mean)
        self._sigDiff_Phase = np.arctan(self._sigQDiff_Mean / self._sigIDiff_Mean)

        return self._sigDiff_Amp, self._sigDiff_Phase

class QUAKESRScan1D:
    @staticmethod
    def load(filename, scannedQuantity = "X", scannedQuantityTitle = "Unknown scanned parameter"):
        data = np.load(filename)
        if "scan" not in data:
            raise ValueError("Not a 2D scan")
        if len(data["scan"].shape) != 1:
            raise ValueError("Not a 2D scan")

        mainAxisData = None
        mainAxisTitle = None
        mainAxis = None

        if "f_RF" in data:
            mainAxis = "f_RF"
            mainAxisTitle = "RF frequency"
            mainAxisData = data["f_RF"]
        else:
            raise ValueError("Unsupported main axis")

        scanned_quantity = scannedQuantity
        scanned_quantity_data = data["scan"]
        scanned_quantity_title = scannedQuantityTitle

        scans = []

        for iScanParam, scanParam in enumerate(data["scan"]):
            sigIZero = None
            sigQZero = None
            if "sigIzero" in data:
                sigIZero = data["sigIzero"][iScanParam]
                sigQZero = data["sigQzero"][iScanParam]

            newscan = QUAKESRScan(mainAxisData, mainAxis, mainAxisTitle, data["sigI"][iScanParam], data["sigQ"][iScanParam], sigIZero, sigQZero, f"{filename}_scan_{scanParam}")
            scans.append(newscan)

        return QUAKESRScan1D(scanned_quantity, scanned_quantity_data, scanned_quantity_title, scans)
             

    def __init__(self, scannedQuantity, scannedQuantityData, scannedQuantityTitle, scans):
        self._scanned_quantity = scannedQuantity
        self._scanned_quantity_data = scannedQuantityData
        self._scanned_quantity_title = scannedQuantityTitle
        self._scans = scans

    def get_scans(self):
        return self._scanned_quantity, self._scanned_quantity_title, self._scanned_quantity_data, self._scans