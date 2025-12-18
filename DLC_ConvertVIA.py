# -*- coding: utf-8 -*-
"""
Created on Mon July 29 17:00:03 2019
​
@author: Pierre Karashchuk
"""
import pandas as pd
from pandas.errors import ParserError
from glob import glob
import os
import numpy as np
import json
import toml
from tqdm import trange


path = r"C:\Users\agrawal-admin\Desktop\TestMosquitoWalking-wayne-2025-04-16\labeled-data"
bodyparts = ["Center-point", "abdomen-tip", "L-fLT", "L-mLT", "L-hLT", "R-fLT", "R-mLT", "R-hLT"]
scorer = 'wayne'



invisibleboundary = 50

(root, dirs, files) = next(os.walk(path))
dirs = sorted(dirs)

# directory = '2019-09-04--11-41--A'
# directory = 'concat_3_27_19_F_fly1'

for directory in dirs:
    folder = os.path.join(path, directory)

    data_fname = os.path.join(folder, 'via_export_csv.csv')
    if not os.path.exists(data_fname):
        continue

    outname = os.path.join(folder,'CollectedData_' + scorer + '.h5')
    if os.path.exists(outname):
        continue

    print(folder)
    data = pd.read_csv(data_fname, engine='python', sep=None)
    prop_names = np.mean([len(x) > 3 for x in data['region_attributes']])
    has_names = prop_names > 0.75

    # print('has names:', has_names)
    if not has_names:
        bp = toml.load(os.path.join(folder, 'via_bodyparts.toml'))
        bodyparts_file = bp['bodyparts']


    coords = dict()
    datalen = None
    bad_data = False
    missing = []

    image_names = sorted(set(data['filename']))
    images = []
    for image in image_names:
        image = os.path.join('labeled-data', directory, image)
        images.append(image)

    index = pd.MultiIndex.from_product(
        [[scorer], bodyparts, ['x', 'y']],
        names=['scorer', 'bodyparts', 'coords'])

    dout = pd.DataFrame(columns=index, index=images)
    dout = dout.astype('float')

    for rnum in trange(len(data),ncols=70):
        row = data.iloc[rnum]
        imgname = os.path.join('labeled-data', directory, row['filename'])

        if has_names:
            attr = json.loads(row['region_attributes'])
            if 'name' not in attr:
                print('W: point without name for img: {}/{}'.format(directory, imgname))
                continue
            bp = attr['name']
        else:
            if row['region_id'] > len(bodyparts_file):
                print('W: extra points for img: {}/{}'.format(directory, imgname))
                continue

            if row['region_id'] >= len(bodyparts_file):
                continue

            bp = bodyparts_file[row['region_id']]

        shape = json.loads(row['region_shape_attributes'])

        x, y = shape['cx'], shape['cy']

        if x < invisibleboundary and y < invisibleboundary:
            x = np.nan
            y = np.nan

        dout.loc[imgname, (scorer, bp, 'x')] = x
        dout.loc[imgname, (scorer, bp, 'y')] = y

    if len(missing) > 0:
        print('W: {} missing parts: {}'.format(directory, missing))

    dout.to_hdf(os.path.join(folder,'CollectedData_' + scorer + '.h5'),
                  'df_with_missing', format='table', mode='w')

    dout.to_csv(os.path.join(folder, 'CollectedData_' + scorer + '.csv'))