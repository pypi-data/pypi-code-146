#!/usr/bin/python3
from os import listdir, makedirs
from os.path import isfile, join, getsize, splitext
from sys import argv
from urllib.parse import urlparse
from clint.textui import progress
from .api.api import PixSoupAPI, APIErrors
from .api.data import FileMetaInput
import usersettings
import dateutil.parser
import requests
import magic
import click

PACKAGE = 'com.pixsoup.cli'
WEB_PUBLIC_URI = 'https://pixsoup.com'
WEB_MEMBERS_URI = WEB_PUBLIC_URI + '/members'

# region CLI
# =====================================================

def non_empty(_, __, value):
  if len(value) < 1:
    raise click.BadParameter("cannot be empty")
  return value

def fmt_date(str):
  return dateutil.parser.isoparse(str).astimezone().strftime("%c")

@click.group()
def cli():
  f"""CLI for PixSoup service.

  Visit {WEB_PUBLIC_URI} for more information.
  """

@cli.group()
def datasets():
  """Manage datasets."""

@cli.group()
@click.argument('id')
@click.pass_context
def dataset(ctx, id):
  """Manage selected dataset."""
  if ctx.obj is None:
    ctx.obj = dict()
  ctx.obj["dataset_id"] = id

@dataset.group()
def resources():
  """Manage dataset resources."""

@cli.group()
@click.argument('id')
@click.pass_context
def resource(ctx, id):
  """Manage selected resource."""
  if ctx.obj is None:
    ctx.obj = dict()
  ctx.obj["resource_id"] = id

@dataset.group()
def run():
  """Run job on the selected dataset."""

@cli.group()
def jobs():
  """Manage jobs."""

@cli.group()
@click.argument('id')
@click.pass_context
def job(ctx, id):
  """Manage selected job."""
  if ctx.obj is None:
    ctx.obj = dict()
  ctx.obj["job_id"] = id

@cli.command("signin")
def signin():
  """Sign-in using an API key."""
  print(f"Visit {WEB_MEMBERS_URI} and generate API (key / token) pair.")
  print()
  settings.api_key = click.prompt('Please enter the API key', type=str)
  settings.api_token = click.prompt('Please enter the API token', type=str)
  settings.save_settings()
  print("You have been signed in")

@cli.command("account")
def account():
  """Show account info."""
  acc = api.account()
  if not acc.verifiedEmail:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!! Your email address has not been verified !!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print()
  cbk = acc.jobCallbackUri if acc.jobCallbackUri else '-- not set --'
  print(acc.email)
  print(f"    tokens:   {acc.tokens}")
  print(f"    callback: {cbk}")

@datasets.command("list")
def list_datasets():
  """List all datasets."""
  datasets = api.datasets()
  for ds in datasets:
    print(ds.name)
    print(f"    id:         {ds.id}")
    print(f"    created at: {fmt_date(ds.createdAt)}")
    if ds.sealedAt:
      print(f"    sealed at:  {fmt_date(ds.sealedAt)}")
    print()

@datasets.command("create")
@click.argument('name')
def create_dataset(name):
  """Create a new dataset."""
  id = api.create_dataset(name)
  print(f"dataset {id} created.")

@dataset.command("delete")
@click.pass_context
def delete_dataset(ctx):
  """Delete dataset and all its resources."""
  id = ctx.obj["dataset_id"]
  if api.delete_dataset(id):
    print(f"dataset {id} has been deleted.")

@dataset.command("seal")
@click.pass_context
def seal_dataset(ctx):
  """Seal dataset, so it can be used to create jobs. Once a dataset is sealed, it cannot be modified, only deleted."""
  id = ctx.obj["dataset_id"]
  if api.seal_dataset(id):
    print(f"dataset {id} has been sealed, you can now use it to create jobs.")

@resources.command("list")
@click.pass_context
def list_resources(ctx):
  """List dataset resources."""
  id = ctx.obj["dataset_id"]
  ds = api.dataset(id)
  print("dataset:")
  print(f"    id:         {ds.id}")
  print(f"    name:       {ds.name}")
  print(f"    created at: {fmt_date(ds.createdAt)}")
  if ds.sealedAt:
    print(f"    sealed at:  {fmt_date(ds.sealedAt)}")
  if len(ds.resources) < 1:
    print("    resources:  -- empty --")
  else :
    print("    resources:")
    for r in ds.resources:
      print(f"        {r.name}")
      print(f"            id:   {r.id}")

@resources.command("add")
@click.argument('directory')
@click.pass_context
def add_resources(ctx, directory):
  """Add resources from the selected directory to the dataset."""
  dataset_id = ctx.obj["dataset_id"]
  mime = magic.Magic(mime=True)
  for file in [f for f in listdir(directory) if isfile(join(directory, f))]:
    path = join(directory, file)
    ct = mime.from_file(path)
    sz = getsize(path)
    try:
      meta = FileMetaInput(file, ct, sz)
      url = api.create_resource(dataset_id, meta)
      print(f"uploading {path}")
      data = open(path, 'rb')
      res = requests.put(url, data=data, headers={"Content-Type": ct})
      if not res.ok:
        raise Exception(f"cannot upload {path}: {res.text}")
      print(f"[{res.status_code}] file {path} succesfully uploaded")
    except APIErrors as err:
      fail = True
      for e in err.errors:
        if e.code == "dataset/resourceFileAlready":
          fail = False
        print(f"error: {file}:", e.message)
        if e.meta:
          print(f"    >> {e.meta}")
      if len(err.errors) > 1 or fail: return

@resource.command("delete")
@click.pass_context
def delete_resource(ctx):
  """Delete resource."""
  id = ctx.obj["resource_id"]
  if api.delete_resource(id):
    print(f"resource {id} has been deleted.")

@run.command("dreambooth")
@click.argument("name")
@click.option("--class", "className", callback=non_empty , required=True)
@click.option("--instance", "instanceName", callback=non_empty , default="sks", show_default=True)
@click.option("--withPriorPreservation", "withPriorPreservation", is_flag=True, default=False, show_default=True)
@click.option("--trainTextEncoder", "trainTextEncoder", is_flag=True, default=False, show_default=True)
@click.option("--learningRate", "learningRate", default=5e-6, type=click.FloatRange(2e-6, 5e-6, clamp=True), show_default=True)
@click.option("--maxTrainSteps", "maxTrainSteps", default=800, type=click.IntRange(200, 2000, clamp=True), show_default=True)
@click.option("--numClassImages", "numClassImages", default=200, type=click.IntRange(100, 400, clamp=True), show_default=True)
@click.option("--lrScheduler", "lrScheduler", default="Constant", type=click.Choice(['Linear', 'Cosine', 'CosineRestarts', 'Polynomial', 'Constant', 'ConstantWarmup']), show_default=True)
@click.option("--sdVersion", "sdVersion", default="V15", type=click.Choice(['V15']), show_default=True)
@click.pass_context
def run_dreambooth_job(ctx, name, **args):
  """Run Dreambooth job using provided parameters."""
  dataset_id = ctx.obj["dataset_id"]
  job = api.run_job(dataset_id, name, args)
  print(f"job {job.id} is {job.state}")

@jobs.command("list")
def list_jobs():
  """List all jobs."""
  jobs = api.jobs()
  for job in jobs:
    print(job.name)
    print(f"    id:          {job.id}")
    print(f"    state:       {job.state}")
    print(f"    args:        {job.args}")
    print(f"    created at:  {fmt_date(job.createdAt)}")
    if job.startedAt:
      print(f"    started at:  {fmt_date(job.startedAt)}")
    if job.finishedAt:
      print(f"    finished at: {fmt_date(job.finishedAt)}")
    print()

@job.command("download")
@click.argument("directory")
@click.pass_context
def download_job_data(ctx, directory):
  """Download job output file."""
  id = ctx.obj["job_id"]
  job = api.job(id)
  if job.state != "Done" and job.state != "Failed":
    raise Exception("job is not finished, try again later")
  p = urlparse(job.downloadLink)
  _, ext = splitext(p.path)
  makedirs(directory, exist_ok=True)
  path = f"{directory}/{job.name}{ext}"
  print(f"downloading job output file to {path}", job.downloadLink)
  res = requests.get(job.downloadLink, stream=True)
  if not res.ok:
    raise Exception(f"cannot download job output file")
  with open(path, 'wb') as f:
    total_length = int(res.headers.get('content-length'))
    for chunk in progress.bar(res.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
      if chunk:
        f.write(chunk)
        f.flush()
  print(f"job output file has been saved to {path}")

@job.command("delete")
@click.pass_context
def delete_job(ctx):
  """Delete finished job and all its data."""
  id = ctx.obj["job_id"]
  if api.delete_job(id):
    print(f"job has been deleted")

# endregion =====================================================

def main():
  global settings, api
  settings = usersettings.Settings(PACKAGE)
  settings.add_setting("api_key", default=None)
  settings.add_setting("api_token", default=None)
  settings.load_settings()
  if len(argv) > 1 and argv[1] == 'signin':
    cli()
    exit()
  if not settings.api_key or not settings.api_token:
    print("You are not signed in, sign-in first using the 'signin' command")
    print(f"$ {argv[0]} signin")
    exit(1)
  try:
    api = PixSoupAPI(settings.api_key, settings.api_token)
    cli()
  except APIErrors as err:
    for e in err.errors:
      if e.code:
        print(f'error: {e.code}: {e.message}')
      else:
        print('error:', e.message)
      if e.meta:
        print(f"    >> {e.meta}")
    exit(1)
  except Exception as e:
    print('error:', e)
    exit(1)

if __name__ == '__main__':
  main()