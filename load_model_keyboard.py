from pathlib import Path
import math
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

asset.set_root_pose(sapien.Pose([0, 0, 0.0], [0, 0, 1, 0]))

print("=== joints info ===")
movable_joint_index = -1
lower = 0.0
upper = 1.0

for idx, j in enumerate(asset.get_joints()):
    print("name:", j.name)
    print("type:", j.type)
    print("limits:", j.get_limits())
    print("------")

    limits = j.get_limits()
    if movable_joint_index == -1 and len(limits) > 0:
        movable_joint_index = 0
        lower = float(limits[0][0])
        upper = float(limits[0][1])

qpos = asset.get_qpos()
print("原本 qpos:", qpos)
print("控制方式：")
print("  J = 關小一點")
print("  K = 開大一點")
print("  R = 重設")
print(f"joint 範圍: lower={lower}, upper={upper}")

scene.set_ambient_light([1.0, 1.0, 1.0])
scene.add_directional_light([0, 1, -1], [1.0, 1.0, 1.0])

viewer = Viewer()
viewer.set_scene(scene)
viewer.set_camera_xyz(x=3.0, y=0.0, z=2.0)
viewer.set_camera_rpy(r=0.0, p=-0.5, y=math.pi)

last_j = False
last_k = False
last_r = False

while not viewer.closed:
    qpos = asset.get_qpos()

    # Viewer 視窗有焦點時按鍵才會生效
    j_now = viewer.window.key_down("j")
    k_now = viewer.window.key_down("k")
    r_now = viewer.window.key_down("r")

    if len(qpos) > 0:
        if j_now and not last_j:
            qpos[0] -= 0.1
            if qpos[0] < lower:
                qpos[0] = lower
            asset.set_qpos(qpos)
            print("目前 qpos:", asset.get_qpos())

        if k_now and not last_k:
            qpos[0] += 0.1
            if qpos[0] > upper:
                qpos[0] = upper
            asset.set_qpos(qpos)
            print("目前 qpos:", asset.get_qpos())

        if r_now and not last_r:
            qpos[0] = lower
            asset.set_qpos(qpos)
            print("重設後 qpos:", asset.get_qpos())

    last_j = j_now
    last_k = k_now
    last_r = r_now

    scene.step()
    scene.update_render()
    viewer.render()