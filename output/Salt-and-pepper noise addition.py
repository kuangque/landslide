import cv2
import numpy as np
import os

def add_salt_pepper_noise(image, amount=0.004, salt_vs_pepper=0.5):
    """
    向图像添加椒盐噪声
    - amount: 噪声占像素比例，建议 0.001 ~ 0.01
    - salt_vs_pepper: 盐（白）与椒（黑）比例
    """
    noisy = image.copy()
    h, w, c = image.shape
    num_noise = int(h * w * amount)

    # 添加盐噪声（白点）
    num_salt = int(num_noise * salt_vs_pepper)
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]
    noisy[coords[0], coords[1]] = [255, 255, 255]

    # 添加椒噪声（黑点）
    num_pepper = num_noise - num_salt
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
    noisy[coords[0], coords[1]] = [0, 0, 0]

    return noisy

def add_sp_noise_batch(input_folder, output_folder, amount=0.004, salt_vs_pepper=0.5):
    """
    批量对图像添加椒盐噪声并保存
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过无效文件: {filename}")
            continue

        noisy_img = add_salt_pepper_noise(img, amount, salt_vs_pepper)
        name, ext = os.path.splitext(filename)
        output_name = f"{name}_sp{int(amount*10000)}.png"
        output_path = os.path.join(output_folder, output_name)

        success = cv2.imwrite(output_path, noisy_img)
        if success:
            print(f"{filename} 添加椒盐噪声后保存至：{output_path}")
        else:
            print(f"保存失败：{output_path}")

if __name__ == "__main__":
    input_folder = r"input"       # 原图路径
    output_folder = r"output"      # 输出路径

    add_sp_noise_batch(input_folder, output_folder, amount=0.005, salt_vs_pepper=0.5)
