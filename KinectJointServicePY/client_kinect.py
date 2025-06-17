import requests
import numpy as np
import cv2


class KinectClient:
    def __init__(self, base_url="http://localhost:59402"):
        self.base_url = base_url

    def get_render_frame(self):
        """Obtiene la imagen renderizada con esqueleto"""
        resp = requests.get(f"{self.base_url}/api/joints/render")
        if resp.status_code == 200:
            arr = np.frombuffer(resp.content, np.uint8)
            return cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return None

    def get_joint_data(self):
        """Obtiene la data 3D de las articulaciones"""
        resp = requests.get(f"{self.base_url}/api/joints/live")
        if resp.status_code == 200:
            return resp.json()
        return None
