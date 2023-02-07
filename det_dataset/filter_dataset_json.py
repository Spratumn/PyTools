import json
import os

FILTER_CONDICTIONS = {
        "grouped": 1,
    }


def filter_json(json_path, **kwargs):
    anno_dict = json.load(open(json_path, 'r'))
    is_filtered = False
    for uid in anno_dict["annoDataList"]:
        objects = []
        for obj in anno_dict["annoDataList"][uid]['objects']:
            matched = False
            for key, value in kwargs.items():
                if key in obj and obj[key] == value:
                    matched = True

            if not matched: objects.append(obj)
        if len(objects) < len(anno_dict["annoDataList"][uid]['objects']):
            anno_dict["annoDataList"][uid]['objects'] = objects
            is_filtered = True
    return anno_dict if is_filtered else None


def is_dataset_dir(dataset_dir):
    for folder in os.listdir(dataset_dir):
        if folder == 'annotations.json': return True
    return False

def filter_process(dataset_dir):
    ori_json_path = os.path.join(dataset_dir, 'annotations.json')
    filtered_json = filter_json(ori_json_path, **FILTER_CONDICTIONS)
    if filtered_json is None: return
    os.rename(ori_json_path, os.path.join(dataset_dir, 'annotations-ori.json'))
    with open(ori_json_path, 'wt') as f:
        f.write(json.dumps(filtered_json, indent=4))
        print(ori_json_path, 'filtered!')

def filter_process_from_rootdir(root_dir):
    for sub in os.listdir(root_dir):
        subdir = os.path.join(root_dir, sub)
        if not os.path.isdir(subdir): continue
        if is_dataset_dir(subdir):
            filter_process(subdir)
        else:
            filter_process_from_rootdir(subdir)

if __name__ == '__main__':

    filter_process_from_rootdir('Y:/Datasets/OpenSource')




