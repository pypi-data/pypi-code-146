from pathlib import Path
from typing import Optional, Tuple, Union
from zipfile import ZipFile

from .dev import annotate_bfx_file_type
from .schema.dev import id


class BfxRun:
    def __init__(
        self,
        *,
        pipeline: dict,
        fastq_bcl_path: Union[str, Path, Tuple],
        outdir: Union[str, Path],
        biosample_id: Optional[str] = None
    ):
        self._biosample_id = biosample_id
        if isinstance(fastq_bcl_path, (str, Path)):
            self._fastq_path = (Path(fastq_bcl_path), None)
        else:
            self._fastq_path = (
                Path(fastq_bcl_path[0]),  # type: ignore
                Path(fastq_bcl_path[1]),
            )
        self._outdir = Path(outdir)
        self._pipeline_id = pipeline["id"]
        self._pipeline_v = pipeline["v"]
        self._pipeline_name = pipeline["name"]
        self._pipeline_reference = pipeline["reference"]
        self._run_id = id.bfx_run()

    @property
    def biosample_id(self):
        """Bfx run's sample id."""
        return self._biosample_id

    @property
    def dobjects(self) -> list:
        """Dobjects associated with the run."""
        return [*self.inputs, *self.outputs]

    @property
    def fastq_path(self) -> Tuple:
        """Paths to input fastqs."""
        return self._fastq_path

    @property
    def file_type(self) -> dict:
        """Bfx file types for each dobject."""
        file_type_dict = {}
        for path in self.dobjects:
            file_type_dict[path] = annotate_bfx_file_type(path)
        return file_type_dict

    @property
    def inputs(self) -> list:
        """Pipeline run inputs."""
        return [path for path in self.fastq_path]

    @property
    def meta_table(self) -> str:
        """Bfx metadata table."""
        return "bfxmeta"

    @property
    def outdir(self) -> Path:
        """BFX pipeline run dir."""
        return self._outdir

    @property
    def outputs(self) -> list:
        """List of files in outdir."""
        dir = self.outdir
        if dir.suffix == ".zip":
            with ZipFile(dir, "r") as zipObj:
                filelist = zipObj.namelist()
                return [file for file in filelist if not file.endswith("/")]
        files = [file for file in dir.rglob("*") if file.is_file()]
        return files

    @property
    def pipeline_id(self):
        """Pipeline id."""
        return self._pipeline_id

    @property
    def pipeline_v(self):
        """Pipeline version."""
        return self._pipeline_v

    @property
    def pipeline_pk(self) -> dict:
        """Pipeline private key."""
        return {"id": self.pipeline_id, "v": self.pipeline_v}

    @property
    def pipeline_name(self):
        """Pipeline name."""
        return self._pipeline_name

    @property
    def pipeline_reference(self):
        """Pipeline reference."""
        return self._pipeline_reference

    @property
    def pipeline_table(self) -> str:
        """Pipeline table."""
        return "bfx_pipeline"

    @property
    def run_id(self):
        """Pipeline run id."""
        return self._run_id

    @property
    def run_pk(self) -> dict:
        """Pipeline private key."""
        return {"id": self.run_id}

    @property
    def run_fk(self) -> dict:
        """Pipeline run foreign key."""
        fk = {"bfx_pipeline_id": self.pipeline_id, "bfx_pipeline_v": self.pipeline_v}
        return fk

    @property
    def run_name(self):
        """Pipeline run name."""
        return self.outdir.as_posix()

    @property
    def run_table(self) -> str:
        """Pipeline run table."""
        return "bfx_run"
