from classy_imaginary.samplers import kdiff
from classy_imaginary.samplers.base import SamplerName  # noqa
from classy_imaginary.samplers.ddim import DDIMSampler
from classy_imaginary.samplers.plms import PLMSSampler

SAMPLERS = [
    PLMSSampler,
    DDIMSampler,
    kdiff.DPMFastSampler,
    kdiff.DPMAdaptiveSampler,
    kdiff.LMSSampler,
    kdiff.DPM2Sampler,
    kdiff.DPM2AncestralSampler,
    kdiff.DPMPP2MSampler,
    kdiff.DPMPP2SAncestralSampler,
    kdiff.EulerSampler,
    kdiff.EulerAncestralSampler,
    kdiff.HeunSampler,
]

SAMPLER_LOOKUP = {sampler.short_name: sampler for sampler in SAMPLERS}
SAMPLER_TYPE_OPTIONS = [sampler.short_name for sampler in SAMPLERS]
