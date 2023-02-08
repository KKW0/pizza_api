import os
import re
import imageio
import progressbar
import numpy as np
import os
import re
import imageio
import progressbar


def compute_rod(intrinsic, correct_principal_point=True):
    """

    가져온 이미지의 중앙, 위치값을 계산하는 코드

    """

    points_to_check = [
        # 왼쪽 상단 모서리
        np.array([0, 0]),
        # 오른쪽 상단 모서리
        np.array([intrinsic.w - 1, 0]),
        # 왼쪽 하단 모서리
        np.array([0, intrinsic.h - 1]),
        # 오른쪽 하단 모서리
        np.array([intrinsic.w - 1, intrinsic.h - 1])
    ]
    center = np.array([intrinsic.w * 0.5, intrinsic.h * 0.5])

    # 이미지의 주점에 대한 보정 계수를 계산
    pp_correction = np.array([0, 0])

    # 모서리 외에 이미지의 중심선을 따라 카메라 고유 매개변수의 정확성을 확인
    if intrinsic.type == "valid_pinhole":
        pp_correction = intrinsic.principal_point - center
    optical_center = center + pp_correction
    points_to_check.append(np.array([optical_center[0], 0]))
    points_to_check.append(np.array([optical_center[0], intrinsic.h - 1]))
    points_to_check.append(np.array([0, optical_center[1]]))
    points_to_check.append(np.array([intrinsic.w - 1, optical_center[1]]))

    max_distortion_vector = []
    for n in points_to_check:
        """
        
        점 집합에 대한 최대 왜곡 벡터를 반복적으로 계산
        
        """

        # 왜곡되지 않은 이미지와 왜곡된 이미지의 값을 가져와서 그 차이를 픽셀값으로 가져옴
        n_undist = intrinsic.get_ud_pixel(n)
        # 왜곡되지 않은 픽셀 위치를 왜곡된 이미지의 벡터 최댓값 추가
        max_distortion_vector.append(n_undist)

    # 왜곡되지 않은 이미지의 최대, 최솟값
    max_distortion_vector.sort(key=lambda a: a[0], reverse=True)
    x_roi_max = int(np.round(max_distortion_vector[0][0]))
    x_roi_min = int(np.round(max_distortion_vector[-1][0]))
    max_distortion_vector.sort(key=lambda a: a[1], reverse=True)
    y_roi_max = int(np.round(max_distortion_vector[0][1]))
    y_roi_min = int(np.round(max_distortion_vector[-1][1]))

    # 왜곡되지 않은 이미지 값을 튜플에 저장
    rod = (x_roi_min, x_roi_max + 1, y_roi_min, y_roi_max + 1)

    # 이미지 중심과 카메라 주점이 아닌 경우 중앙에 배치
    if correct_principal_point:
        rod = (rod[0] - pp_correction[0], rod[1] - pp_correction[0],
               rod[2] - pp_correction[1], rod[3] - pp_correction[1])
    return rod


def convert_rod_to_roi(intrinsic, rod):
    """

    rod : 왜곡되지 않은 이미지
    roi : 왜곡되지 않은 이미지를 얼마큼 왜곡되었는지 값을 측정

    :return: roi

    """
    x_offset = rod[0]
    y_offset = rod[2]

    # roi = 언디스토션 이미지 값
    roi = (-x_offset, intrinsic.w - x_offset, -y_offset, intrinsic.h - y_offset)
    return roi

<<<<<<< HEAD
def undistort_images(sfm_data, view_filter, undistorted_images, undistorted_images_folder_path,
                     output_file_type, correct_principal_point, roi_for_intrinsic, export_full_roi):
=======

# 측정된 값으로 rod와 roi값을 추가(?)
def undistort_images(sfm_data, view_filter, undistorted_images, undistorted_images_folder_path, output_file_type, correct_principal_point, roi_for_intrinsic, export_full_roi):
>>>>>>> 3cf1d0d2cc14b5b3072b6aaa3e14cd7416727b7d
    print("Build animated camera(s)...")

    # 사용되는 진행률 표시줄 라이브러리
    bar = progressbar.ProgressBar(max_value=len(sfm_data.views))

    # 각 뷰를 처리한 후 값을 1씩 증가시켜 루프의 진행률 보여줌
    for view in sfm_data.views.values():
        bar.update(bar.value + 1)

        # 정규식 필터를 정규식 개체로 컴파일
        if view_filter:
            regex_filter = re.compile(view_filter)
            if not regex_filter.match(view.image_path):
                continue

        # 기본 이름과 확장자로 분할하고 튜플 결과 처리
        image_path_stem = os.path.splitext(os.path.basename(view.image_path))[0]

        # undistort camera images
        if undistorted_images:
            # 현재 보기에 대한 고유 개체 검색
            intrinsic = sfm_data.intrinsics[view.intrinsic_id]
            dst_image = os.path.join(undistorted_images_folder_path, f"{view.intrinsic_id}_{image_path_stem}.{output_file_type}")

            # 이미지와 해당 메타데이터 읽기
            image = imageio.imread(view.image_path, as_gray=False)
            metadata = imageio.immeta(view.image_path)

            # 내장 개체에 왜곡이 있는 경우 이미지 왜곡 해제
            if intrinsic.is_valid() and intrinsic.has_distortion():
                """
                
                1. sfm_data 먼저 개체에서 현재 보기에 대한 고유 개체를 검색합니다.
                2. 'imageio.imread', 'imageio.immeta'를 사용하여 이미지와 해당 메타데이터를 읽습니다.    
                3. 내장 개체에 왜곡이 있는 경우 코드는 내장 undistort 방법을 사용하여 이미지를 왜곡 해제합니다. 
                   True로 설정된 경우 export_full_roi 코드는 왜곡되지 않은 이미지에 대한 관심 영역(ROI)을 계산하고, 
                   ROI를 사용하여 이미지를 왜곡하지 않는다.
                   ROI를 관심 영역 개체로 변환하고, 'write_image'를 사용하여 메타데이터와 함께 왜곡되지 않은 이미지를 씁니다. 
                   False로 설정된 경우 export_full_roi 코드는 ROI를 계산하지 않고 이미지를 왜곡하지 않고 
                   'imageio.imwrite'를 사용하여 저장합니다.
                4. 내장 개체에 왜곡이 없는 경우 'imageio.imwrite' 코드를 사용하여 원본 이미지를 저장합니다.
                
                """

                if export_full_roi:
                    key = view.intrinsic_id
                    if key not in roi_for_intrinsic:
                        rod = compute_rod(intrinsic, correct_principal_point)
                        roi_for_intrinsic[key] = rod
                    else:
                        rod = roi_for_intrinsic[key]
                    print(f"rod:{rod.xbegin};{rod.xend};{rod.ybegin};{rod.yend}")
                    image_ud = intrinsic.undistort(image, black_fill_value=np.array([0,0,0]),
                                                   correct_principal_point=correct_principal_point, roi=rod)
                    roi = convert_rod_to_roi(intrinsic, rod)
                    write_image(dst_image, image_ud, metadata, roi)
                else:
                    image_ud = intrinsic.undistort(image, black_fill_value=np.array([0,0,0]),
                                                   correct_principal_point=correct_principal_point)
                    imageio.imwrite(dst_image, image_ud, plugin=None, format=output_file_type, metadata=metadata)
            else: # 왜곡이 없는 경우
                imageio.imwrite(dst_image, image, plugin=None, format=output_file_type, metadata=metadata)

        # 카메라 위치값과 고유 매개변수가 현재 보기에 대해 정의되어 있는지 확인
        if not sfm_data.is_pose_and_intrinsic_defined(view):
            continue

        # camera_name 뷰의 "make" 메타데이터 값으로 설정
        camera_name = view.metadata_make(camera_name)
