from pathlib import Path
import math
import time
import sapien
from sapien.utils.viewer import Viewer

urdf_path = Path("/mnt/d/Code/3d_model/7236/7236/mobility.urdf")

scene = sapien.Scene()
scene.set_timestep(1 / 240.0)

loader = scene.create_urdf_loader()
loader.fix_root_link = True

asset = loader.load(str(urdf_path))
if asset is None:
    raise RuntimeError("URDF 載入失敗")

# 放到原點，並旋轉讓它正面比較朝向你
asset.set_root_pose(sapien.Pose([0, 0, 0.0], [0, 0, 1, 0]))

print("=== joints info ===")
for j in asset.get_joints():
    print("name:", j.name)
    print("type:", j.type)
    print("limits:", j.get_limits())
    print("------")

qpos = asset.get_qpos()
print("原本 qpos:", qpos)

scene.set_ambient_light([1.0, 1.0, 1.0])
scene.add_directional_light([0, 1, -1], [1.0, 1.0, 1.0])

viewer = Viewer()
viewer.set_scene(scene)
viewer.set_camera_xyz(x=3.0, y=0.0, z=2.0)
viewer.set_camera_rpy(r=0.0, p=-0.5, y=math.pi)

# 只有至少 1 個自由度才做動畫
if len(qpos) == 0:
    print("這個模型沒有可動關節，無法做開蓋動畫。")

direction = 1.0

# 取 joint limit
lower = 0.0
upper = 1.0
joints = asset.get_joints()

# 找第一個可動 joint 的範圍
for j in joints:
    limits = j.get_limits()
    if len(limits) > 0:
        lower = float(limits[0][0])
        upper = float(limits[0][1])
        break

print(f"使用的 joint 範圍: lower={lower}, upper={upper}")

while not viewer.closed:
    if len(asset.get_qpos()) > 0:
        qpos = asset.get_qpos()
        qpos[0] += direction * 0.01

        if qpos[0] >= upper:
            qpos[0] = upper
            direction = -1.0
        elif qpos[0] <= lower:
            qpos[0] = lower
            direction = 1.0

        asset.set_qpos(qpos)

    scene.step()
    scene.update_render()
    viewer.render()