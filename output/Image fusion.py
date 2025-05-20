import cv2
import numpy as np
import random
import time
from pathlib import Path
from skimage import exposure


class ImageBlender:
    def __init__(self, source_path, backgrounds_folder, output_folder, max_display_width=1200):
        self.source_path = Path(source_path)
        self.backgrounds_folder = Path(backgrounds_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # 原始图像和缩放图像
        self.image = cv2.imread(str(self.source_path))
        self.clone = self.image.copy()
        self.points = []

        # 缩放比例处理
        self.display_image, self.ratio = self.resize_image(self.image, max_display_width)

    def resize_image(self, image, max_width):
        h, w = image.shape[:2]
        if w > max_width:
            ratio = max_width / w
            resized = cv2.resize(image, (int(w * ratio), int(h * ratio)))
            return resized, ratio
        return image.copy(), 1.0

    def draw_polygon(self, image, points):
        if len(points) > 1:
            for i in range(len(points) - 1):
                cv2.line(image, points[i], points[i + 1], (0, 255, 0), 2)
        if len(points) > 2:
            cv2.polylines(image, [np.array(points)], True, (0, 255, 0), 2)

    def create_mask(self, size, points):
        mask = np.zeros(size, dtype=np.uint8)
        cv2.fillPoly(mask, [np.array(points, dtype=np.int32)], 255)
        return mask

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))

    def histogram_match(self, src, target):
        matched = exposure.match_histograms(src, target, channel_axis=-1)
        return np.clip(matched, 0, 255).astype(np.uint8)

    def feather_mask(self, mask, radius=15):
        return cv2.GaussianBlur(mask, (radius * 2 + 1, radius * 2 + 1), 0)

    def extract_roi_and_mask(self):
        if len(self.points) < 3:
            raise ValueError("至少选择三个点以构成多边形")

        # 将缩放图上的点映射回原图
        pts = np.array([(int(x / self.ratio), int(y / self.ratio)) for x, y in self.points])
        x, y, w, h = cv2.boundingRect(pts)
        roi = self.clone[y:y + h, x:x + w]
        shifted_pts = [(px - x, py - y) for px, py in pts]
        mask = self.create_mask((h, w), shifted_pts)
        return roi, mask

    def blend_to_backgrounds(self, roi, mask):
        bg_files = list(self.backgrounds_folder.glob("*.*"))
        bg_files = [f for f in bg_files if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]

        if not bg_files:
            print("背景图像目录为空")
            return

        for bg_path in bg_files:
            bg = cv2.imread(str(bg_path))
            if bg is None or bg.shape[0] < roi.shape[0] + 40 or bg.shape[1] < roi.shape[1] + 40:
                print(f"跳过尺寸不合适的背景图: {bg_path.name}")
                continue

            h_roi, w_roi = roi.shape[:2]
            h_bg, w_bg = bg.shape[:2]
            pad = 20
            x = random.randint(pad, w_bg - w_roi - pad)
            y = random.randint(pad, h_bg - h_roi - pad)
            center = (x + w_roi // 2, y + h_roi // 2)

            roi_adjusted = self.histogram_match(roi, bg[y:y + h_roi, x:x + w_roi])
            mask_blur = self.feather_mask(mask)

            blended = cv2.seamlessClone(roi_adjusted, bg, mask_blur, center, cv2.MIXED_CLONE)

            out_name = f"blend_{bg_path.stem}_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(str(self.output_folder / out_name), blended)
            print(f"保存融合结果: {out_name}")

    def run(self):
        print("请用鼠标点击图像选区，按 Enter 确认，ESC 退出")
        cv2.namedWindow("Select ROI", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Select ROI", self.mouse_callback)

        while True:
            display = self.display_image.copy()
            self.draw_polygon(display, self.points)
            cv2.imshow("Select ROI", display)
            key = cv2.waitKey(1)

            if key == 13:  # Enter
                try:
                    roi, mask = self.extract_roi_and_mask()
                    self.blend_to_backgrounds(roi, mask)
                except Exception as e:
                    print(f"处理错误: {e}")
                break
            elif key == 27:  # ESC
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    source_path = r"image"                   #原图
    backgrounds_folder = r"backgrounds"      #背景图片
    output_folder = r"output"                #输出路径

    blender = ImageBlender(source_path, backgrounds_folder, output_folder)
    blender.run()
