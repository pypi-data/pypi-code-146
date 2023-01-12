from enum import Enum
from lmfit import Parameters, fit_report, minimize
import numpy as np
import matplotlib.pyplot as plt

# Generic mixture fitter (like Gaussianmixture but with arbitrary functions)

class Fitfunctions(Enum):
    GAUSSIAN = 1
    DIFFGAUSSIAN = 2
    CAUCHY = 3
    DIFFCAUHCY = 4
    CONSTANT = 5

    def __int__(self):
        return int(self.value)

class Fitfunction:
    def __init__(self, idvalue, functiontype, parsymbolname, parsymboltitle):
        if len(parsymbolname) != len(parsymboltitle):
            raise ValueError("Each symbol name has to have a descriptive title")
        if not isinstance(idvalue, Fitfunctions):
            raise ValueError("Fitfunction ID has to be a Fitfunction enum")
        self._idvalue = idvalue
        self._functiontype = functiontype
        self._parsymbolname = parsymbolname
        self._parsymboltitle = parsymboltitle

    def get_param_symbols(self):
        return self._parsymbolname

    def eval(self, x, pars = None, parprefix = None):
        raise NotImplementedException()

    def initialGuess(self, x, data):
        raise NotImplementedException()

    def getFWHM(self, ppars = None, parprefix = ""):
        return NotImplementedException()

    def paramstring(self, ppars = None, parprefix = ""):
        if ppars is None:
            return f"{self._functiontype}"

        if not isinstance(ppars, dict):
            pars = ppars.valuesdict()
        else:
            pars = ppars


        res = f"{self._functiontype} ("
        for ik, k in enumerate(self._parsymbolname):
            if ik > 0:
                res = res + ", "
            res = f'{res}{k} {pars[f"{parprefix}{k}"]}'
        res = res + ")"

        return res

    def paramdict(self, ppars = None, parprefix = ""):
        res = {}

        if ppars is None:
            return f"{self._functiontype}"

        if not isinstance(ppars, dict):
            pars = ppars.valuesdict()
        else:
            pars = ppars

        res['typecode'] = self._idvalue.value
        res['type'] = self._functiontype
        for ik, k in enumerate(self._parsymbolname):
            res[k] = pars[f"{parprefix}{k}"]

        center, fwhm = self.getCenterFWHM(ppars, parprefix)
        res['fwhm'] = fwhm
        res['center'] = center

        return res

class Fitfunction_Constant(Fitfunction):
    def __init__(self):
        super().__init__(
            Fitfunctions.CONSTANT,
            "Constant offset",
            [ "offset" ],
            [ "offset" ]
        )
    def eval(self, x, ppars = None, parprefix = None):
        if not isinstance(ppars, dict):
            pars = ppars.valuesdict()
        else:
            pars = ppars

        if pars is None:
            offset = 0
        else:
            if parprefix is not None:
                pfx = parprefix
            else:
                pfx = ""
            offset = pars[f"{pfx}offset"]

        return offset

    def getFWHM(self, ppars = None, parprefix = ""):
        return 0

    def get_guess(self, x, data):
        return {
            "offset" : np.mean(data)
        }


class Fitfunction_Cauchy(Fitfunction):
    def __init__(self):
        super().__init__(
            Fitfunctions.CAUCHY,
            "Cauchy distribution",
            [ "amp", "x0", "gamma", "offset" ],
            [ "amplitude", "center", "gamma", "offset" ]
        )

    def _parse_pparms(self, ppars, parprefix):
        if not isinstance(ppars, dict):
            pars = ppars.valuesdict()
        else:
            pars = ppars

        if pars is None:
            amp = 1
            x0 = 0
            gamma = 1
            offset = 0
        else:
            if parprefix is not None:
                pfx = parprefix
            else:
                pfx = ""
            amp = pars[f"{pfx}amp"]
            x0 = pars[f"{pfx}x0"]
            gamma = pars[f"{pfx}gamma"]
            offset = pars[f"{pfx}offset"]

        return amp, x0, gamma, offset

    def eval(self, x, ppars = None, parprefix = None):
        amp, x0, gamma, offset = self._parse_pparms(ppars, parprefix)
        return amp * 1.0 / (np.pi * gamma) * (gamma**2 / ((x - x0)**2 + gamma**2)) + offset

    def getCenterFWHM(self, ppars = None, parprefix = ""):
        _, x0, gamma, _ = self._parse_pparms(ppars, parprefix)
        return x0, 2*gamma

    def get_guess(self, x, data):
        if np.max(data) > np.min(data):
            return {
                "amp" : np.max(data) - np.min(data),
                "x0" : x[np.argmax(data)],
                "gamma" : 1,
                "offset" : np.min(data)
            }
        else:
            return {
                "amp" : - np.max(data) + np.min(data),
                "x0" : x[np.argmin(data)],
                "gamma" : 1,
                "offset" : np.max(data)
            }

class Fitfunction_DiffCauchy(Fitfunction):
    def __init__(self):
        super().__init__(
            Fitfunctions.DIFFCAUHCY,
            "Differential Cauchy distribution",
            [ "amp", "x0", "gamma", "offset" ],
            [ "amplitude", "center", "gamma", "offset" ]
        )

    def _parse_pparms(self, ppars, parprefix):
        if not isinstance(ppars, dict):
            pars = ppars.valuesdict()
        else:
            pars = ppars

        if pars is None:
            amp = 1
            x0 = 0
            gamma = 1
            offset = 0
        else:
            if parprefix is not None:
                pfx = parprefix
            else:
                pfx = ""
            amp = pars[f"{pfx}amp"]
            x0 = pars[f"{pfx}x0"]
            gamma = pars[f"{pfx}gamma"]
            offset = pars[f"{pfx}offset"]

        return amp, x0, gamma, offset

    def eval(self, x, ppars = None, parprefix = None):
        amp, x0, gamma, offset = self._parse_pparms(ppars, parprefix)
        return amp * -2.0 / (np.pi * gamma ** 3) * (x - x0) / ((x-x0)**2/gamma**2 + 1.0)**2.0 + offset

    def getCenterFWHM(self, ppars = None, parprefix = ""):
        _, x0, gamma, _ = self._parse_pparms(ppars, parprefix)
        return x0, 2*gamma

    def get_guess(self, x, data):
        if (np.argmax(data) < np.argmin(data)):
            return {
                "amp" : np.max(data) - np.min(data),
                "offset" : (np.max(data) + np.min(data))/2.0,
                "gamma" : x[np.argmin(data)] - x[np.argmax(data)],
                "x0" : (x[np.argmin(data)] + x[np.argmax(data)]) / 2.0
            }
        else:
            return {
                "amp" : - np.max(data) + np.min(data),
                "offset" : (np.max(data) + np.min(data))/2.0,
                "gamma" : x[np.argmax(data)] - x[np.argmin(data)],
                "x0" : (x[np.argmax(data)] + x[np.argmin(data)]) / 2.0
            }

class Fitfunction_Gaussian(Fitfunction):
    def __init__(self):
        super().__init__(
            Fitfunctions.GAUSSIAN,
            "Gaussian",
            [ "mu", "sigma", "amp", "offset" ],
            [ "mu", "sigma", "amplitude", "offset"]
        )

    def _parse_pparms(self, ppars, parprefix):
        if not isinstance(ppars, dict):
            pars = ppars.valuesdict()
        else:
            pars = ppars

        if pars is None:
            amp = 1
            mu = 0
            sig = 1
            offs = 0
        else:
            if parprefix is not None:
                pfx = parprefix
            else:
                pfx = ""
            amp = pars[f"{pfx}amp"]
            mu = pars[f"{pfx}mu"]
            sig = pars[f"{pfx}sigma"]
            offs = pars[f"{pfx}offset"]
        return amp, mu, sig, offs

    def eval(self, x, ppars = None, parprefix = None):
        amp, mu, sig, offs = self._parse_pparms(ppars, parprefix)
        return amp * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.))) + offs

    def getCenterFWHM(self, ppars = None, parprefix = ""):
        _, mu, sig, _ = self._parse_pparms(ppars, parprefix)
        return mu, 2*np.sqrt(2)*sig

    def get_guess(self, x, data):
        if np.abs(np.max(data)) > np.abs(np.min(data)):
            return {
                "amp" : np.max(data) - np.min(data),
                "offset" : np.min(data),
                "sigma" : 1,
                "mu" : x[np.argmax(data)]
            }
        else:
            return {
                "amp" : -1 * (np.min(data) - np.min(data)),
                "offset" : np.max(data),
                "sigma" : 1,
                "mu" : x[np.argmin(data)]
            }

class Fitfunction_Diffgaussian(Fitfunction):
    def __init__(self):
        super().__init__(
            Fitfunctions.GAUSSIAN,
            "Differential Gaussian",
            [ "mu", "sigma", "amp", "offset" ],
            [ "mu", "sigma", "amplitude", "offset"]
        )

    def _parse_pparms(self, ppars, parprefix):
        if not isinstance(ppars, dict):
            pars = ppars.valuesdict()
        else:
            pars = ppars

        if pars is None:
            amp = 1
            mu = 0
            sig = 1
            offs = 0
        else:
            if parprefix is not None:
                pfx = parprefix
            else:
                pfx = ""
            amp = pars[f"{pfx}amp"]
            mu = pars[f"{pfx}mu"]
            sig = pars[f"{pfx}sigma"]
            offs = pars[f"{pfx}offset"]
        return amp, mu, sig, offs

    def eval(self, x, ppars = None, parprefix = None):
        amp, mu, sig, offs = self._parse_pparms(ppars, parprefix)
        return amp * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.))) * -1.0 * (x - mu) / (sig * sig)

    def getCenterFWHM(self, ppars = None, parprefix = ""):
        _, mu, sig, _ = self._parse_pparms(ppars, parprefix)
        return mu, 2*np.sqrt(2)*sig

    def get_guess(self, x, data):
        if (np.argmax(data) < np.argmin(data)):
            return {
                "amp" : np.max(data) - np.min(data),
                "offset" : (np.max(data) + np.min(data))/2.0,
                "sigma" : x[np.argmin(data)] - x[np.argmax(data)],
                "mu" : (x[np.argmin(data)] + x[np.argmax(data)]) / 2.0
            }
        else:
            return {
                "amp" : - np.max(data) + np.min(data),
                "offset" : (np.max(data) + np.min(data))/2.0,
                "sigma" : x[np.argmax(data)] - x[np.argmin(data)],
                "mu" : (x[np.argmax(data)] + x[np.argmin(data)]) / 2.0
            }



fitfunctionInstances = {
    Fitfunctions.GAUSSIAN.value     : Fitfunction_Gaussian(),
    Fitfunctions.DIFFGAUSSIAN.value : Fitfunction_Diffgaussian(),
    Fitfunctions.CAUCHY.value       : Fitfunction_Cauchy(),
    Fitfunctions.DIFFCAUHCY.value   : Fitfunction_DiffCauchy(),
    Fitfunctions.CONSTANT.value     : Fitfunction_Constant()
}

class MixtureFitter:
    def __init__(
        self,

        allowedFunctions = None,
        minimumResiduumImprovement = 0,
        maxiterations = 1000,
        stoperror = 1e-99
    ):
        self._allowedfunctions = []
        self._maxiterations = maxiterations
        self._minimumResiduumImprovement = minimumResiduumImprovement
        self._stoperror = stoperror
        if allowedFunctions is not None:
            if not isinstance(allowedFunctions, list) and not isinstance(allowedFunctions, tuple):
                raise ValueError("Supplied allowed function has to be a list or tuple")
            for af in allowedFunctions:
                if not isinstance(allowedFunctions, Fitfunctions):
                    raise ValueError("Supplied entry for fitfunction has to be a Fitfunctions enum member")

            for af in allowedFunctions:
                self._allowedfunctions.append(af.value)
        else:
            for fkey in fitfunctionInstances:
                self._allowedfunctions.append(fkey)

    def dict2fitpars(self, paras):
        p = Parameters()
        for k in paras:
            if k == "n":
                continue
            varies = True
            if k.endswith("_type"):
                varies = False

            p.add(k, value = paras[k], vary = varies)

        p.add("n", paras["n"], vary = False)

        return p

    def guess2fitpars(self, guess):
        p = Parameters()
        p.add("n", 1, vary = False)
        for k in guess:
            varies = True
            if k.endswith("_type"):
                varies = False
            p.add(f"f0_{k}", guess[k], vary = varies)

        return p

    def evalMixture(self, paras, x, inputdata = None):
        if isinstance(paras, Parameters):
            p = paras.valuesdict()
        else:
            p = paras

        res = np.zeros(x.shape)
        for ifun in range(p["n"]):
            res = res + fitfunctionInstances[p[f"f{ifun}_type"]].eval(x, p, f"f{ifun}_")

        if inputdata is not None:
            res = res - inputdata

        return res

    def fitMixture(self, x, inputData, debugplots = False, debugplotsshow = True, debugplotsprefix = None, printprogress = False):
        fittedFunctions = { 'n' : 0 }
        chis = []

        if printprogress:
            print(f"[MIXFIT] Starting fit (prefix {debugplotsprefix})")

        while (len(chis) < 2) or ((chis[len(chis)-1] < chis[len(chis)-2]) and (len(chis) < self._maxiterations) and ((chis[len(chis)-2] - chis[len(chis)-1]) > self._minimumResiduumImprovement) and (chis[len(chis)-1] > self._stoperror)):
            if printprogress:
                print(f"[MIXFIT] Iteration {len(chis)+1} (prefix {debugplotsprefix})")

            # Subtract previously fitted functions
            stageInput = inputData - self.evalMixture(fittedFunctions, x)

            # Guess next candidate ...
            bestType = None
            bestChi2 = None
            bestParams = None

            if debugplots:
                fig, ax = plt.subplots(len(self._allowedfunctions), figsize=(6.4*2, 4.8*2*len(self._allowedfunctions)))

            for icandidate, candidatetype in enumerate(self._allowedfunctions):
                # Perform a single fit from an (function dependent) initial guess
                guess = fitfunctionInstances[candidatetype].get_guess(x, stageInput)
                guessParams = self.guess2fitpars(guess)
                guessParams.add("f0_type", candidatetype, vary = False)
                res = minimize(self.evalMixture, guessParams, args=(x,), kws= { 'inputdata' : stageInput })

                if debugplots:
                    ax[icandidate].plot(x, stageInput, label = "Stage input")
                    ax[icandidate].plot(x, self.evalMixture(res.params, x), "r--", label = f"Initial guess {fitfunctionInstances[candidatetype].paramstring()} ($\chi^2$ = {res.chisqr})")
                    ax[icandidate].legend()
                    ax[icandidate].grid()

                if bestChi2 is None:
                    bestType = candidatetype
                    bestParams = res.params
                    bestChi2 = res.chisqr
                elif bestChi2 > res.chisqr:
                    bestType = candidatetype
                    bestParams = res.params
                    bestChi2 = res.chisqr

            if debugplots:
                if debugplotsshow:
                    plt.show()
                if debugplotsprefix is not None:
                    plt.savefig(f"{debugplotsprefix}fittry_iter_{len(chis)}.png")
                plt.close()

            # Add best candidate to mixture (using the "fit result")
            n_new = fittedFunctions['n']
            fittedFunctions['n'] = fittedFunctions['n'] + 1
            bestParamsDict = bestParams.valuesdict()

            if debugplots:
                fig, ax = plt.subplots(3, figsize=(6.4*2, 4.8*3*2))

                funstr = fitfunctionInstances[bestType].paramstring(bestParamsDict, 'f0_')

                ax[0].set_title(f"Stage, iteration {len(chis)+1}")
                ax[0].plot(x, stageInput, "b", label = "Stage input")
                ax[0].plot(x, self.evalMixture(bestParams, x), "r--", label = f"Initial guess\n({funstr})")
                ax[0].grid()
                ax[0].legend()

            for k in bestParamsDict:
                if k.startswith("f0_"):
                    fittedFunctions[f"f{n_new}_{k[3:]}"] = bestParamsDict[k]

            # Bundle adjust (on whole input data)
            adjustParsIn = self.dict2fitpars(fittedFunctions)
            try:
                res = minimize(self.evalMixture, adjustParsIn, args=(x,), kws = {'inputdata' : inputData})
            except:
                break

            chis.append(res.chisqr)
            fittedFunctions = res.params.valuesdict()

            if debugplots:
                ax[1].set_title(f"Bundle, iteration {len(chis)}")
                ax[1].plot(x, inputData, "b", label = "Input data")
                ax[1].plot(x, self.evalMixture(res.params, x), "r--", label = "Current fit")
                ax[1].grid()
                ax[1].legend()

                ax[2].set_title("$\chi^2$")
                ax[2].set_xlabel("Iteration")
                ax[2].set_ylabel("$\chi^2$")
                ax[2].plot(chis)
                ax[2].grid()

                plt.tight_layout()
                if debugplotsshow:
                    plt.show()
                if debugplotsprefix is not None:
                    plt.savefig(f"{debugplotsprefix}iter_{len(chis)}.png")
                plt.close()

        # In case we include elements that did not improve or did not improve enough -> remove them from our result
        while (len(chis) > 2) and ((chis[len(chis)-1] > chis[len(chis)-2]) or ((chis[len(chis)-2] - chis[len(chis)-1]) < self._minimumResiduumImprovement)):
            chis = chis[:-1]
            fittedFunctions['n'] = fittedFunctions['n'] - 1
        while chis[len(chis)-1]  < self._stoperror:
            chis = chis[:-1]
            fittedFunctions['n'] = fittedFunctions['n'] - 1


        for i in range(len(chis)):
            fittedFunctions["f{i}_chisqr"] = chis[i]

        return fittedFunctions

    def mixture2str(self, mixture):
        if isinstance(mixture, Parameters):
            p = mixture.valuesdict()
        else:
            p = mixture

        res = ""
        for ielement in range(p["n"]):
            res = res + fitfunctionInstances[mixture[f"f{ielement}_type"]].paramstring(mixture, f"f{ielement}_") + "\t"
            center, fwhm = fitfunctionInstances[mixture[f"f{ielement}_type"]].getCenterFWHM(mixture, f"f{ielement}_")
            res = res + f"Center: {center}, FWHM: {fwhm}"
            res = res + "\n"
        return res

    def mixtures2dictlist(self, mixture):
        res = []
        if isinstance(mixture, Parameters):
            p = mixture.valuesdict()
        else:
            p = mixture

        for ielement in range(p["n"]):
            res.append(fitfunctionInstances[mixture[f"f{ielement}_type"]].paramdict(mixture, f"f{ielement}_"))

        return res

    def mixtures2barplot(self, mixture, yunitlabel = "", chanlabel = ""):
        if isinstance(mixture, Parameters):
            p = mixture.valuesdict()
        else:
            p = mixture

        labeldata = []
        amplitude = []
        for ielement in range(p["n"]):
            center, fwhm = fitfunctionInstances[p[f"f{ielement}_type"]].getCenterFWHM(mixture, f"f{ielement}_")
            paras = fitfunctionInstances[p[f"f{ielement}_type"]].paramdict(mixture, f"f{ielement}_")

            if 'amp' in paras:
                amplitude.append(paras['amp'])
                labeldata.append(fitfunctionInstances[p[f"f{ielement}_type"]].paramstring() + f"\nCenter {np.round(center, 2)} {yunitlabel}\nFWHM {np.round(np.abs(fwhm), 2)} {yunitlabel}")

        ypos = np.arange(len(labeldata))
        fig, ax = plt.subplots()
        hbars = ax.barh(ypos, amplitude, align='center')
        ax.set_yticks(ypos, labels=labeldata)
        ax.invert_yaxis()
        ax.set_xlabel("Amplitude")
        ax.set_title(f"Fitted components {chanlabel}")
        ax.bar_label(hbars, fmt='%.2f')
        fig.tight_layout()

        return fig, ax


if __name__ == "__main__":
    mf = MixtureFitter()

    data = np.load("/home/quakesr/20230105_001/2023-01-05_09:23:10_peak.npz")
    x = data['f_RF']
    meansI = np.zeros((len(data['sigI']),))
    for i in range(len(meansI)):
        meansI[i] = np.mean(data['sigI'][i])

    #x = np.linspace(-10, 10, 1000)
    #testdata = np.sin(x)
    testdata = meansI

    #resmix = mf.fitMixture(x, testdata, debugplots = True, debugplotsshow = True)
    resmix = mf.fitMixture(x, testdata, debugplots = False, debugplotsshow = True)
    mf.mixtures2barplot(resmix, yunitlabel="MHz")
    #print(mf.mixtures2dictlist(resmix))