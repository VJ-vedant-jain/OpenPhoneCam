import json
import cv2
from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QFileDialog


class TabCammy:
    def __init__(self, ui):
        self.ui = ui

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS,          9999999)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  9999999)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 9999999)

        self.maxFPS = cap.get(cv2.CAP_PROP_FPS)
        self.maxW   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.maxH   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        self.cap = None
        self.fps = self.maxFPS
        self.resolution = [self.maxW, self.maxH]
        self.aspectRatio = None
        self.mirror_xaxis = False
        self.mirror_yaxis = False

        self.ui.lineEditFPS.setText(f"{int(self.maxFPS)}")
        self.ui.lineEditResolution.setText(f"{self.maxW}x{self.maxH}")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update_frame)

        self.ui.btnConnect.clicked.connect(self._start_camera)
        self.ui.btnDisconnect.clicked.connect(self._stop_camera)

        self.ui.lineEditFPS.editingFinished.connect(self._update_fps)
        self.ui.lineEditResolution.editingFinished.connect(self._update_resolution)
        self.ui.comboBoxAspectRatio.currentIndexChanged.connect(self._update_aspect_ratio)

        self.ui.checkBoxMirror_xaxis.stateChanged.connect(self._update_mirror_x)
        self.ui.checkBoxMirror_yaxis.stateChanged.connect(self._update_mirror_y)


    def _start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self.timer.start(int(1000 / self.fps))

        self.ui.textEditStatus.append("Camera started")
        self.ui.btnConnect.setEnabled(False)
        self.ui.btnDisconnect.setEnabled(True)

    def _stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.ui.labelVideoPreview.clear()
        self.ui.textEditStatus.append("Camera stopped")
        self.ui.btnConnect.setEnabled(True)
        self.ui.btnDisconnect.setEnabled(False)


    def _update_frame(self):
        if not self.cap:
            return

        retval, frame_bgr = self.cap.read()
        if not retval:
            return

        frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        # aspect ratio crop
        if self.aspectRatio and self.aspectRatio != "Auto":
            frame = self._change_image_ratio(frame).copy()

        # mirror
        flip_code = None
        if self.mirror_xaxis and self.mirror_yaxis:
            flip_code = -1
        elif self.mirror_xaxis:
            flip_code = 0
        elif self.mirror_yaxis:
            flip_code = 1
        if flip_code is not None:
            frame = cv2.flip(frame, flip_code)

        h, w, ch = frame.shape
        qimg = QtGui.QImage(frame.data, w, h, w * ch, QtGui.QImage.Format.Format_RGB888)
        self.ui.labelVideoPreview.setPixmap(
            QtGui.QPixmap.fromImage(qimg).scaled(
                self.ui.labelVideoPreview.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )
        )

    def _change_image_ratio(self, frame):
        h, w, _ = frame.shape
        parts         = self.aspectRatio.split(":")
        target_ratio  = float(parts[0]) / float(parts[1])
        current_ratio = w / h

        if current_ratio > target_ratio:
            new_w  = int(h * target_ratio)
            offset = (w - new_w) // 2
            return frame[:, offset:offset + new_w]
        else:
            new_h  = int(w / target_ratio)
            offset = (h - new_h) // 2
            return frame[offset:offset + new_h, :]


    def _update_fps(self):
        try:
            self.fps = int(self.ui.lineEditFPS.text())
        except ValueError:
            return
        if self.cap:
            self._stop_camera()
            self._start_camera()

    def _update_resolution(self):
        try:
            self.resolution = [int(x) for x in self.ui.lineEditResolution.text().split("x")]
        except ValueError:
            return
        if self.cap:
            self._stop_camera()
            self._start_camera()

    def _update_aspect_ratio(self):
        self.aspectRatio = self.ui.comboBoxAspectRatio.currentText()

    def _update_mirror_x(self):
        self.mirror_xaxis = self.ui.checkBoxMirror_xaxis.isChecked()

    def _update_mirror_y(self):
        self.mirror_yaxis = self.ui.checkBoxMirror_yaxis.isChecked()


    def save_settings(self):
        data = {
            "device_ip": self.ui.lineEditIP.text(),
            "port": self.ui.lineEditPort.text(),
            "resolution": self.ui.lineEditResolution.text(),
            "fps": self.ui.lineEditFPS.text(),
            "bitrate": self.ui.spinBoxBitrate.value(),
            "aspect_ratio": self.ui.comboBoxAspectRatio.currentIndex(),
            "enable_audio": self.ui.checkBoxEnableAudio.isChecked(),
            "sample_rate": self.ui.comboBoxSampleRate.currentIndex(),
            "mirror_video_yaxis": self.ui.checkBoxMirror_yaxis.isChecked(),
            "mirror_video_xaxis": self.ui.checkBoxMirror_xaxis.isChecked(),
            "keep_device_awake": self.ui.checkBoxKeepAwake.isChecked(),
        }

        path, _ = QFileDialog.getSaveFileName(
            self.ui, "Save Settings", "saved_settings.json", "JSON Files (*.json)"
        )
        if not path:
            return

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        self.ui.textEditStatus.append("Settings saved")

    def load_settings(self):
        path, _ = QFileDialog.getOpenFileName(
            self.ui, "Load Settings", "", "JSON Files (*.json)"
        )
        if not path:
            return

        with open(path, "r") as f:
            data = json.load(f)

        self.ui.lineEditIP.setText(data.get("device_ip", ""))
        self.ui.lineEditPort.setText(data.get("port", ""))
        self.ui.lineEditResolution.setText(data.get("resolution", ""))
        self.ui.lineEditFPS.setText(data.get("fps", ""))
        self.ui.spinBoxBitrate.setValue(int(data.get("bitrate", 0)))
        self.ui.comboBoxAspectRatio.setCurrentIndex(int(data.get("aspect_ratio", 0)))
        self.ui.checkBoxEnableAudio.setChecked(bool(data.get("enable_audio", False)))
        self.ui.comboBoxSampleRate.setCurrentIndex(int(data.get("sample_rate", 0)))
        self.ui.checkBoxMirror_yaxis.setChecked(bool(data.get("mirror_video_yaxis", False)))
        self.ui.checkBoxMirror_xaxis.setChecked(bool(data.get("mirror_video_xaxis", False)))
        self.ui.checkBoxKeepAwake.setChecked(bool(data.get("keep_device_awake", False)))

        self.ui.textEditStatus.append("Settings loaded")