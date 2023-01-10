def parse_pycoco_metrics(epoch: int, pycoco_train_metrics: str, pycoco_eval_metrics: str) -> dict:
    """
    Parses text output of the pycocotools metrics for the train loop and the eval loop for one epoch.
    """
    import re
    record = dict()
    record["epoch"] = epoch
    for name, value in re.findall('(\w+):[^(]+\(([^)]+)\)', pycoco_train_metrics):
        if name == "lr":
            continue # exclude learning rate.
        record[name] = float(value)
    for line in pycoco_eval_metrics.split("\n"):
        r = re.search('[^(]+\(([^)]+)\) @\[ IoU=([^|]+)\| area=([^|]+)\| maxDets=([^\]]+)] = (-?\d+.\d+)', line)
        if not r:
            continue
        m, iou, area, maxDets, value = r.group(1).strip(), r.group(2).strip().replace("0.", "."), r.group(3).strip(), r.group(4).strip(), r.group(5)
        metric = m
        if m == "AP":
            metric = "Average Precision"
        if m == "AR":
            metric = "Average Recall"
        iou = " @" + iou + "IoU "
        area = "" if area == "all" else "(" + area + ")"
        maxDets = "" if maxDets == "100" else "[" + maxDets + "]" 
        name = metric + iou + area + maxDets
        record[name] = float(value)
    return record