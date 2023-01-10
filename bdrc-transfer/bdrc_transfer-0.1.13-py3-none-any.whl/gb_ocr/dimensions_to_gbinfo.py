import boto3
import botocore
import json
import os
import hashlib
import io
import gzip
from gb_lib.GbLib import VolumeToWork

SESSION = boto3.Session()
S3 = SESSION.client('s3')

def gets3blob(s3Key):
    f = io.BytesIO()
    try:
        S3.download_fileobj('archive.tbrc.org', s3Key, f)
        return f
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return None
        else:
            raise


# This has a cache mechanism
def getImageList(s3_bucket: str, v_w: VolumeToWork) ->[byte]:
    """
    Gets the image list as defined by a dimensions.json
    :param s3_bucket: source bucket
    :param v_w: Work and Volume
    :return:
    """

    # We don't have to worry about the image group name discjunction hack - these works are
    # already resolved in S3
    from archive_ops.shell_ws import get_mappings, Resolvers
    s3_work = get_mappings(s3_bucket+'Works', v_w.work_name, Resolvers.S3_BUCKET)
    s3_key = f"{s3_work}/images/{v_w.work_name}-{v_w.volume_label}/dimensions.json"
    blob = gets3blob(s3_key)
    if blob is None:
        return None
    blob.seek(0)
    b = blob.read()
    ub = gzip.decompress(b)
    s = ub.decode('utf8')
    data = json.loads(s)
    return data

def iltogbinfo(imagelist):
   res = {}
   for i, imginfo in enumerate(imagelist):
      res["%08d" % (i+1)] = imginfo["filename"]
   return res

def main():
   for i in range(423, 484):
      igLocalName = "I4PD%d" % i
      imglist = getImageList("W2PD17457", igLocalName)
      gbinfo = iltogbinfo(imglist)
      outdir = "info/W2PD17457-%s" % igLocalName
      os.makedirs(outdir, exist_ok=True)
      with open(outdir+'/gb-bdrc-map.json', 'w', encoding='utf-8') as f:
         json.dump(gbinfo, f, ensure_ascii=False)

main()