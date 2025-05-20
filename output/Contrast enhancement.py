import cv2
import numpy as np
import os

def adjust_contrast(image, contrast_factor):
    """
    对比度调整：contrast_factor 推荐范围 0.5～1.5
    <1 减弱对比度，>1 增强对比度
    """
    img_contrast = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=0)
    return img_contrast

def contrast_adjust_images_in_folder(input_folder, output_folder, factor_range=(0.5, 1.5)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过非图像文件: {filename}")
            continue

        # 随机对比度因子
        factor = np.round(np.random.uniform(factor_range[0], factor_range[1]), 2)
        contrast_img = adjust_contrast(img, factor)

        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_contrast{factor}{ext}")

        success = cv2.imwrite(output_path, contrast_img)
        if success:
            print(f"{filename} 对比度增强 factor={factor} 并保存至 {output_path}")
        else:
            print(f"保存失败: {output_path}")

if __name__ == "__main__":
    input_folder = r"input"       # 原图路径
    output_folder = r"output"      # 输出路径

    contrast_adjust_images_in_folder(input_folder, output_folder, factor_range=(0.5, 1.5))
