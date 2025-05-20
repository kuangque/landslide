import cv2
import numpy as np
import os

def blur_image(image, max_kernel_size=5):
    """
    应用高斯模糊，随机选择奇数核大小，例如3x3、5x5、7x7等
    """
    kernel_size = np.random.choice([k for k in range(1, max_kernel_size + 1) if k % 2 == 1])
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blurred, kernel_size

def blur_images_batch(input_folder, output_folder, max_kernel_size=5):
    """
    批量对图像应用模糊处理并保存
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过无效文件: {filename}")
            continue

        blurred_img, k = blur_image(img, max_kernel_size)
        name, ext = os.path.splitext(filename)
        output_name = f"{name}_blur{k}{ext}"
        output_path = os.path.join(output_folder, output_name)

        success = cv2.imwrite(output_path, blurred_img)
        if success:
            print(f"{filename} 模糊处理 kernel={k} 保存至：{output_path}")
        else:
            print(f"保存失败：{output_path}")

if __name__ == "__main__":
    input_folder = r"input"       # 原图路径
    output_folder = r"output"      # 输出路径

    blur_images_batch(input_folder, output_folder, max_kernel_size=7)
