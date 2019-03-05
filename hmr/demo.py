"""
Demo of HMR.
Note that HMR requires the bounding box of the person in the image. The best performance is obtained when max length of the person in the image is roughly 150px. 
When only the image path is supplied, it assumes that the image is centered on a person whose length is roughly 150px.
Alternatively, you can supply output of the openpose to figure out the bbox and the right scale factor.
Sample usage:
# On images on a tightly cropped image around the person
python -m demo --img_path data/im1963.jpg
python -m demo --img_path data/coco1.png
# On images, with openpose output
python -m demo --img_path data/random.jpg --json_path data/random_keypoints.json
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from absl import flags
import numpy as np

import skimage.io as io
import tensorflow as tf

from src.util import renderer as vis_util
from src.util import image as img_util
from src.util import openpose as op_util
import src.config
from src.RunModel import RunModel

import pandas as pd
import os
import glob
import shutil

flags.DEFINE_string('img_path', 'data/im1963.jpg', 'Image to run')
flags.DEFINE_string(
    'json_path', None,
    'If specified, uses the openpose output to crop the image.')


def visualize(img_path, img, proc_param, joints, verts, cam):
    """
    Renders the result in original image coordinate frame.
    """
    cam_for_render, vert_shifted, joints_orig = vis_util.get_original(
        proc_param, verts, cam, joints, img_size=img.shape[:2])

    # Render results
    skel_img = vis_util.draw_skeleton(img, joints_orig)
    rend_img_overlay = renderer(
        vert_shifted, cam=cam_for_render, img=img, do_alpha=True)
    rend_img = renderer(
        vert_shifted, cam=cam_for_render, img_size=img.shape[:2])
    rend_img_vp1 = renderer.rotated(
        vert_shifted, 60, cam=cam_for_render, img_size=img.shape[:2])
    rend_img_vp2 = renderer.rotated(
        vert_shifted, -60, cam=cam_for_render, img_size=img.shape[:2])

    import matplotlib.pyplot as plt
    # plt.ion()
    plt.figure(1)
    plt.clf()
    plt.subplot(231)
    plt.imshow(img)
    plt.title('input')
    plt.axis('off')
    plt.subplot(232)
    plt.imshow(skel_img)
    plt.title('joint projection')
    plt.axis('off')
    plt.subplot(233)
    plt.imshow(rend_img_overlay)
    plt.title('3D Mesh overlay')
    plt.axis('off')
    plt.subplot(234)
    plt.imshow(rend_img)
    plt.title('3D mesh')
    plt.axis('off')
    plt.subplot(235)
    plt.imshow(rend_img_vp1)
    plt.title('diff vp')
    plt.axis('off')
    plt.subplot(236)
    plt.imshow(rend_img_vp2)
    plt.title('diff vp')
    plt.axis('off')
    plt.draw()
    plt.savefig("hmr/output/images/" + os.path.splitext(os.path.basename(img_path))[0] + ".png")
    # import ipdb
    # ipdb.set_trace()


# TODO: Load all images, process all, and return all
def preprocess_image(img_path, json_path=None):
    img = io.imread(img_path)
    if img.shape[2] == 4:
        img = img[:, :, :3]

    if json_path is None:
        if np.max(img.shape[:2]) != config.img_size:
            print('Resizing so the max image size is %d..' % config.img_size)
            scale = (float(config.img_size) / np.max(img.shape[:2]))
        else:
            scale = 1.
        center = np.round(np.array(img.shape[:2]) / 2).astype(int)
        # image center in (x,y)
        center = center[::-1]
    else:
        #TODO: correct the json file name
        print(json_path)
        scale, center = op_util.get_bbox(json_path)

    crop, proc_param = img_util.scale_and_crop(img, scale, center,
                                               config.img_size)

    # Normalize image to [-1, 1]
    crop = 2 * ((crop / 255.) - 0.5)

    return crop, proc_param, img


def main(img_path, json_path=None):
    sess = tf.Session()
    model = RunModel(config, sess=sess)

    # TODO: input_img, proc_pram, img all should be array that contains all images
    images = glob.glob(os.path.join(img_path, "*.png"))
    input_images = []
    proc_params = []
    for img in images:
        #TODO: find the json file with the same name
        temp = img.split('/')
        json_name = temp[2]
        json_name = json_name[0:len(json_name)-3]
        json_path = json_path+json_name+'json'

        input_img, proc_param, img = preprocess_image(img, json_path)

    # ======== Original Script ==============
    #input_img, proc_param, img = preprocess_image(img_path, json_path)
    ## Add batch dimension: 1 x D x D x 3
    #input_img = np.expand_dims(input_img, 0)

    #joints, verts, cams, joints3d, theta = model.predict(
    #    input_img, get_theta=True)

    ##     print('JOINTS 3D:')
    ##    print(joints3d.shape)
    ##     print(joints3d)

    #joints_names = ['Ankle.R_x', 'Ankle.R_y', 'Ankle.R_z',
    #                'Knee.R_x', 'Knee.R_y', 'Knee.R_z',
    #                'Hip.R_x', 'Hip.R_y', 'Hip.R_z',
    #                'Hip.L_x', 'Hip.L_y', 'Hip.L_z',
    #                'Knee.L_x', 'Knee.L_y', 'Knee.L_z',
    #                'Ankle.L_x', 'Ankle.L_y', 'Ankle.L_z',
    #                'Wrist.R_x', 'Wrist.R_y', 'Wrist.R_z',
    #                'Elbow.R_x', 'Elbow.R_y', 'Elbow.R_z',
    #                'Shoulder.R_x', 'Shoulder.R_y', 'Shoulder.R_z',
    #                'Shoulder.L_x', 'Shoulder.L_y', 'Shoulder.L_z',
    #                'Elbow.L_x', 'Elbow.L_y', 'Elbow.L_z',
    #                'Wrist.L_x', 'Wrist.L_y', 'Wrist.L_z',
    #                'Neck_x', 'Neck_y', 'Neck_z',
    #                'Head_x', 'Head_y', 'Head_z',
    #                'Nose_x', 'Nose_y', 'Nose_z',
    #                'Eye.L_x', 'Eye.L_y', 'Eye.L_z',
    #                'Eye.R_x', 'Eye.R_y', 'Eye.R_z',
    #                'Ear.L_x', 'Ear.L_y', 'Ear.L_z',
    #                'Ear.R_x', 'Ear.R_y', 'Ear.R_z']

    #joints_export = pd.DataFrame(joints3d.reshape(1, 57), columns=joints_names)
    #joints_export.index.name = 'frame'

    #joints_export.iloc[:, 1::3] = joints_export.iloc[:, 1::3] * -1
    #joints_export.iloc[:, 2::3] = joints_export.iloc[:, 2::3] * -1

    #hipCenter = joints_export.loc[:][['Hip.R_x', 'Hip.R_y', 'Hip.R_z',
    #                                  'Hip.L_x', 'Hip.L_y', 'Hip.L_z']]

    #joints_export['hip.Center_x'] = hipCenter.iloc[0][::3].sum() / 2
    #joints_export['hip.Center_y'] = hipCenter.iloc[0][1::3].sum() / 2
    #joints_export['hip.Center_z'] = hipCenter.iloc[0][2::3].sum() / 2

    #joints_export.to_csv("hmr/output/csv/" + os.path.splitext(os.path.basename(img_path))[0] + ".csv")

    #visualize(img_path, img, proc_param, joints[0], verts[0], cams[0])


def join_csv():
    path = 'hmr/output/csv/'
    move_types = os.listdir(path)
    for move in move_types:
        move_path = path + move + '/'
        all_files = glob.glob(os.path.join(move_path, "*.csv"))
        df_from_each_file = (pd.read_csv(f) for f in sorted(all_files))
        concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

        concatenated_df['frame'] = concatenated_df.index + 1
        concatenated_df.to_csv(move_path + "/csv_joined.csv", index=False)


def classify_images():
    print("classify movements!")

    path = 'hmr/output/csv/'
    movement_types = []
    all_files = glob.glob(os.path.join(path, "*.csv"))

    for files in sorted(all_files):
        nameLen = len(files) - 7
        move_name = files[0:nameLen]
        if move_name not in movement_types:
            movement_types.append(move_name)
            if not os.path.exists(move_name):
                # shutil.rmtree(move_name)
                os.mkdir(move_name)

        newname = move_name + "/" + files[nameLen:len(files)]
        os.rename(files, newname)


if __name__ == '__main__':
    config = flags.FLAGS
    config(sys.argv)
    # Using pre-trained model, change this to use your own.
    config.load_path = src.config.PRETRAINED_MODEL

    config.batch_size = 1

    renderer = vis_util.SMPLRenderer(face_path=config.smpl_face_path)

    main(config.img_path, config.json_path)

    # classify_images()

    # join_csv()

print('\nResult is in hmr/output (you can open images in Colaboratory by double-clicking them)')
