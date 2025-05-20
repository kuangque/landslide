import cv2
import numpy as np
import os

def adjust_brightness(image, brightness_shift):
    """
    调整亮度：brightness_shift 范围推荐为 [-50, 50]
    """
    img_bright = cv2.convertScaleAbs(image, alpha=1, beta=brightness_shift)
    return img_bright

def brightness_adjust_images_in_folder(input_folder, output_folder, shift_range=(-50, 50)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过非图像文件: {filename}")
            continue

        # 随机亮度偏移值
        shift = np.random.randint(shift_range[0], shift_range[1] + 1)
        bright_img = adjust_brightness(img, shift)

        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_bright{shift}{ext}")

        success = cv2.imwrite(output_path, bright_img)
        if success:
            print(f"{filename} 调整亮度 shift={shift} 并保存至 {output_path}")
        else:
            print(f"保存失败: {output_path}")

if __name__ == "__main__":
    input_folder = r"input"       # 原图路径
    output_folder = r"output"      # 输出路径

    brightness_adjust_images_in_folder(input_folder, output_folder, shift_range=(-50, 50))
