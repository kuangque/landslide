import cv2
import os
import numpy as np

def random_crop(image, scale_range=(0.3, 0.8)):
    """
    随机裁剪图像一块区域
    scale_range: 裁剪区域占原图面积比例范围 (最小, 最大)，如(0.3,0.8)
    返回裁剪后的图像
    """
    h, w = image.shape[:2]
    scale = np.random.uniform(scale_range[0], scale_range[1])

    crop_area = scale * (h * w)
    # 计算裁剪区域宽高比例，保持和原图一致，避免变形
    aspect_ratio = w / h

    crop_h = int(np.sqrt(crop_area / aspect_ratio))
    crop_w = int(crop_h * aspect_ratio)

    # 随机选取裁剪区域左上角坐标
    if h - crop_h > 0:
        y = np.random.randint(0, h - crop_h)
    else:
        y = 0
        crop_h = h
    if w - crop_w > 0:
        x = np.random.randint(0, w - crop_w)
    else:
        x = 0
        crop_w = w

    cropped = image[y:y+crop_h, x:x+crop_w]
    return cropped

def random_crop_images_in_folder(input_folder, output_folder, scale_range=(0.3, 0.8)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过非图像文件: {filename}")
            continue

        cropped_img = random_crop(img, scale_range=scale_range)

        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_crop{ext}")

        success = cv2.imwrite(output_path, cropped_img)
        if success:
            print(f"{filename} 随机裁剪并保存至 {output_path}")
        else:
            print(f"保存失败: {output_path}")

if __name__ == "__main__":
    input_folder = r"input"       # 原图路径
    output_folder = r"output"      # 输出路径

    random_crop_images_in_folder(input_folder, output_folder, scale_range=(0.3, 0.8))
