import numpy as np

def compute_rod(intrinsic, correct_principal_point=True):
    points_to_check = [
        np.array([0, 0]),
        np.array([intrinsic.w - 1, 0]),
        np.array([0, intrinsic.h - 1]),
        np.array([intrinsic.w - 1, intrinsic.h - 1])
    ]
    center = np.array([intrinsic.w * 0.5, intrinsic.h * 0.5])
    pp_correction = np.array([0, 0])
    if intrinsic.type == "valid_pinhole":
        pp_correction = intrinsic.principal_point - center
    optical_center = center + pp_correction
    points_to_check.append(np.array([optical_center[0], 0]))
    points_to_check.append(np.array([optical_center[0], intrinsic.h - 1]))
    points_to_check.append(np.array([0, optical_center[1]]))
    points_to_check.append(np.array([intrinsic.w - 1, optical_center[1]]))

    max_distortion_vector = []
    for n in points_to_check:
        n_undist = intrinsic.get_ud_pixel(n)
        max_distortion_vector.append(n_undist)

    max_distortion_vector.sort(key=lambda a: a[0], reverse=True)
    x_roi_max = int(np.round(max_distortion_vector[0][0]))
    x_roi_min = int(np.round(max_distortion_vector[-1][0]))
    max_distortion_vector.sort(key=lambda a: a[1], reverse=True)
    y_roi_max = int(np.round(max_distortion_vector[0][1]))
    y_roi_min = int(np.round(max_distortion_vector[-1][1]))

    rod = (x_roi_min, x_roi_max + 1, y_roi_min, y_roi_max + 1)

    if correct_principal_point:
        rod = (rod[0] - pp_correction[0], rod[1] - pp_correction[0],
               rod[2] - pp_correction[1], rod[3] - pp_correction[1])
    return rod

def convert_rod_to_roi(intrinsic, rod):
    x_offset = rod[0]
    y_offset = rod[2]
    roi = (-x_offset, intrinsic.w - x_offset, -y_offset, intrinsic.h - y_offset)
    return roi

import os
import re
import imageio
import numpy as np
import progressbar

def undistort_images(sfm_data, view_filter, undistorted_images, undistorted_images_folder_path, output_file_type, correct_principal_point, roi_for_intrinsic, export_full_roi):
    print("Build animated camera(s)...")

    bar = progressbar.ProgressBar(max_value=len(sfm_data.views))

    for view in sfm_data.views.values():
        bar.update(bar.value + 1)

        # regex filter
        if view_filter:
            regex_filter = re.compile(view_filter)
            if not regex_filter.match(view.image_path):
                continue

        image_path_stem = os.path.splitext(os.path.basename(view.image_path))[0]

        # undistort camera images
        if undistorted_images:
            intrinsic = sfm_data.intrinsics[view.intrinsic_id]
            dst_image = os.path.join(undistorted_images_folder_path, f"{view.intrinsic_id}_{image_path_stem}.{output_file_type}")

            image = imageio.imread(view.image_path, as_gray=False)
            metadata = imageio.immeta(view.image_path)

            if intrinsic.is_valid() and intrinsic.has_distortion():
                if export_full_roi:
                    key = view.intrinsic_id
                    if key not in roi_for_intrinsic:
                        rod = compute_rod(intrinsic, correct_principal_point)
                        roi_for_intrinsic[key] = rod
                    else:
                        rod = roi_for_intrinsic[key]
                    print(f"rod:{rod.xbegin};{rod.xend};{rod.ybegin};{rod.yend}")
                    image_ud = intrinsic.undistort(image, black_fill_value=np.array([0,0,0]), correct_principal_point=correct_principal_point, roi=rod)
                    roi = convert_rod_to_roi(intrinsic, rod)
                    write_image(dst_image, image_ud, metadata, roi)
                else:
                    image_ud = intrinsic.undistort(image, black_fill_value=np.array([0,0,0]), correct_principal_point=correct_principal_point)
                    imageio.imwrite(dst_image, image_ud, plugin=None, format=output_file_type, metadata=metadata)
            else: # (no distortion)
                imageio.imwrite(dst_image, image, plugin=None, format=output_file_type, metadata=metadata)

        # pose and intrinsic defined
        if not sfm_data.is_pose_and_intrinsic_defined(view):
            continue

        camera_name = view.metadata_make
