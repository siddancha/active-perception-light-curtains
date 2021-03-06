import csv
import numpy as np
import fire
import os
from pathlib import Path

def get_data(dir):
    dir = Path(dir) 
    data = {'test' : {'0.50': {}, '0.70': {}},
            'valid': {'0.50': {}, '0.70': {}}}
    
    filenames = os.listdir(dir)
    assert len(filenames) == 16

    for filename in filenames:
        split = 'test' if 'test' in filename else 'valid'
        thresh = '0.50' if '0.50' in filename else '0.70'

        # Get step.
        step = [e for e in filename.split('_') if 'step' in e][0][4:]
        
        with open(dir / filename, 'r') as f:
            csv_reader = csv.reader(f)
            rows = [row for row in csv_reader]
            contents = np.array(rows)[1:, 1:].astype(np.float32)
        data[split][thresh][step] = contents

    return data


def create_json_file(dir, out):
    """
    {"eval.kitti": {"valid_step0_official": {"Car": {"bbox@0.70": [0.0, 18.299794744200977, 18.483052009703425], "bev@0.70": [0.0, 8.993761826695755, 9.11027269804464], "3d@0.70": [0.0, 2.228904568815286, 2.1740311196617603], "aos": [0.0, 0.8510891786694208, 0.8697459611108836], "bev@0.50": [0.0, 26.724706874756365, 26.106909029711783], "3d@0.50": [0.0, 19.396430204828814, 19.006762959219085]}}, "valid_step1_official": {"Car": {"bbox@0.70": [0.0, 8.853462139677099, 8.760819001421469], "bev@0.70": [0.0, 4.440493705683089, 4.456611036694104], "3d@0.70": [0.0, 1.2167826191669289, 1.2462899993244307], "aos": [0.0, 0.46614640890904646, 0.4535393139035987], "bev@0.50": [0.0, 13.232892139416153, 13.054120429814315], "3d@0.50": [0.0, 9.541363359093268, 9.628073766081755]}}, "valid_step2_official": {"Car": {"bbox@0.70": [0.0, 8.248598267259398, 8.312409029698834], "bev@0.70": [0.0, 4.042631183083442, 4.056003906567103], "3d@0.70": [0.0, 1.2039897250404628, 1.2342155452203298], "aos": [0.0, 0.4387920460351618, 0.4373605548363407], "bev@0.50": [0.0, 12.10571231110869, 12.015419445569314], "3d@0.50": [0.0, 9.247764011416994, 9.393502052675936]}}, "valid_step3_official": {"Car": {"bbox@0.70": [0.0, 7.598583449747825, 7.677383989411567], "bev@0.70": [0.0, 3.7125442060086713, 3.7146063412044366], "3d@0.70": [0.0, 1.1308333573150058, 1.143085279151178], "aos": [0.0, 0.4076368921123673, 0.40617548824133176], "bev@0.50": [0.0, 11.342812276109653, 11.387537927516709], "3d@0.50": [0.0, 8.594902554614785, 8.542147535481389]}}}, "step": 1000}
    {"eval.kitti": {"test_step0_official": {"Car": {"bbox@0.70": [2.5974025974025974, 13.223140495867769, 13.223140495867769], "bev@0.70": [0.6734006734006733, 6.682340647857889, 6.766791715915516], "3d@0.70": [0.4784688995215311, 1.4354066985645932, 1.4354066985645932], "aos": [0.004810918835125703, 0.9712310222288998, 1.0645340670092314], "bev@0.50": [1.3636363636363635, 13.812341184055828, 13.733466502978978], "3d@0.50": [1.2987012987012987, 11.485578082907805, 11.574212440109646]}}, "test_step1_official": {"Car": {"bbox@0.70": [2.5974025974025974, 1.9795637012407754, 1.9895045531717857], "bev@0.70": [0.6493506493506493, 1.2789787471316134, 1.3173400673400673], "3d@0.70": [0.4784688995215311, 0.32085561497326204, 0.32085561497326204], "aos": [0.004810918835125703, 0.2271034460111299, 0.2196482120543699], "bev@0.50": [1.2987012987012987, 3.3649932157394846, 3.4027261650365452], "3d@0.50": [1.2987012987012987, 2.621811641595814, 2.596932674409155]}}, "test_step2_official": {"Car": {"bbox@0.70": [1.2121212121212122, 1.5250378978001533, 1.4035661423014696], "bev@0.70": [0.505050505050505, 0.8628719048204839, 0.884683761713924], "3d@0.70": [0.3952569169960474, 0.19342359767891684, 0.19342359767891684], "aos": [0.002245096996642414, 0.15163031069423202, 0.15163031069423202], "bev@0.50": [0.8264462809917356, 2.0469179667292874, 2.053796681235121], "3d@0.50": [0.8264462809917356, 1.9209956709956708, 1.9278743855015041]}}, "test_step3_official": {"Car": {"bbox@0.70": [1.1363636363636365, 1.3512460746900137, 1.2904982692044868], "bev@0.70": [0.505050505050505, 0.876382828079956, 0.8985129417314941], "3d@0.70": [0.3952569169960474, 0.20102747375474647, 0.20102747375474647], "aos": [0.0021398935734910133, 0.13471731070627468, 0.13471731070627468], "bev@0.50": [0.7272727272727273, 2.034676520860581, 2.022036213448305], "3d@0.50": [0.7272727272727273, 1.915038984004501, 1.902398676592225]}}}, "step": 1000}
    """
    data = get_data(dir)

    def step_string(split, step, iter_ind):
        thresh5val = data[split]['0.50'][step][iter_ind, 1]
        thresh7val = data[split]['0.70'][step][iter_ind, 1]
        return f"\"{split}_step{step}_official\": {{\"Car\": {{\"3d@0.50\": [0, {thresh5val}, 0], \"3d@0.70\": [0, {thresh7val}, 0]}}}}"
    
    def split_string(split, iter_ind):
        string = []
        steps = data[split]['0.50'].keys()
        for step in steps:
            string.append(step_string(split, step, iter_ind))
        train_iter = data[split]['0.50']['0'][iter_ind, 0]
        string = "{\"eval.kitti\": {" + ", ".join(string) + f"}}, \"step\": {int(train_iter)}}}"
        return string

    records = []
    for iter_ind in range(len(data['valid']['0.50']['0'])):
        records.append(split_string("valid", iter_ind))
        records.append(split_string("test", iter_ind))
    
    with open(out, 'w') as f:
        for record in records:
            print(record, file=f)

if __name__ == "__main__":
    fire.Fire()