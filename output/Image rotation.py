import cv2
import numpy as np
import os

def rotate_image_with_blank(image, angle, fill_color=(0, 0, 0)):
    """
    旋转图像，边角空白部分用指定颜色填充（默认黑色）。
    """
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             borderMode=cv2.BORDER_CONSTANT,
                             borderValue=fill_color)
    return rotated

def rotate_images_in_folder(input_folder, output_folder, angle_range=(-15, 15), fill_color=(0,0,0)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过非图像文件: {filename}")
            continue

        angle = np.random.uniform(angle_range[0], angle_range[1])
        rotated_img = rotate_image_with_blank(img, angle, fill_color=fill_color)

        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_rot{int(angle)}{ext}")

        success = cv2.imwrite(output_path, rotated_img)
        if success:
            print(f"{filename} 旋转 {angle:.2f}° 并保存至 {output_path}")
        else:
            print(f"保存失败: {output_path}")

if __name__ == "__main__":
    input_folder = r"input"       # 原图路径
    output_folder = r"output"      # 输出路径
    # fill_color参数可以改为白色或其他颜色，比如白色(255,255,255)
    rotate_images_in_folder(input_folder, output_folder, angle_range=(-15, 15), fill_color=(0, 0, 0))
