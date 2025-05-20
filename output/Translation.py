import cv2
import numpy as np
import os

def translate_image(image, max_shift_x=50, max_shift_y=50, fill_color=(0, 0, 0)):
    """
    对图像进行随机平移，x和y方向平移距离在[-max_shift, max_shift]范围内
    fill_color：平移后空白部分填充颜色，默认黑色
    """
    h, w = image.shape[:2]
    tx = np.random.randint(-max_shift_x, max_shift_x + 1)
    ty = np.random.randint(-max_shift_y, max_shift_y + 1)

    M = np.float32([[1, 0, tx], [0, 1, ty]])
    translated = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=fill_color)
    return translated, tx, ty

def translate_images_in_folder(input_folder, output_folder, max_shift_x=50, max_shift_y=50, fill_color=(0,0,0)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过非图像文件: {filename}")
            continue

        translated_img, tx, ty = translate_image(img, max_shift_x, max_shift_y, fill_color)

        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_trans{tx}_{ty}{ext}")

        success = cv2.imwrite(output_path, translated_img)
        if success:
            print(f"{filename} 平移 tx={tx}, ty={ty} 并保存至 {output_path}")
        else:
            print(f"保存失败: {output_path}")

if __name__ == "__main__":
    input_folder = r"input"  # 原图路径
    output_folder = r"output"  # 输出路径

    translate_images_in_folder(input_folder, output_folder, max_shift_x=50, max_shift_y=50, fill_color=(0,0,0))
