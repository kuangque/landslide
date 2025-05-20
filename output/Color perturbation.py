import cv2
import numpy as np
import os

def distort_color(image, hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=20):
    """
    HSV通道扰动颜色：随机改变H（色调）、S（饱和度）、V（亮度）
    """
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.int32)
    h, s, v = cv2.split(image_hsv)

    h_shift = np.random.randint(-hue_shift_limit, hue_shift_limit + 1)
    s_shift = np.random.randint(-sat_shift_limit, sat_shift_limit + 1)
    v_shift = np.random.randint(-val_shift_limit, val_shift_limit + 1)

    h = (h + h_shift) % 180
    s = np.clip(s + s_shift, 0, 255)
    v = np.clip(v + v_shift, 0, 255)

    image_hsv = cv2.merge([h, s, v]).astype(np.uint8)
    image_bgr = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    return image_bgr, h_shift, s_shift, v_shift

def color_distortion_batch(input_folder, output_folder):
    """
    批量对文件夹中的图像进行色彩扰动，并保存处理后的图像
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过无效文件: {filename}")
            continue

        img_distorted, h_shift, s_shift, v_shift = distort_color(img)
        name, ext = os.path.splitext(filename)
        output_name = f"{name}_colorH{h_shift}S{s_shift}V{v_shift}{ext}"
        output_path = os.path.join(output_folder, output_name)

        success = cv2.imwrite(output_path, img_distorted)
        if success:
            print(f"{filename} 色彩扰动后保存至：{output_path}")
        else:
            print(f"保存失败：{output_path}")

if __name__ == "__main__":
    input_folder = r"input"       # 原图路径
    output_folder = r"output"      # 输出路径

    color_distortion_batch(input_folder, output_folder)
