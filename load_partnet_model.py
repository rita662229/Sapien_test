from pathlib import Path
import sapien
from sapien.utils.viewer import Viewer

urdf_path = Path("/mnt/d/Code/3d_model/8867/8867/mobility.urdf")

scene = sapien.Scene()

loader = scene.create_urdf_loader()
loader.fix_root_link = True

asset = loader.load(str(urdf_path))
if asset is None:
    raise RuntimeError("URDF 載入失敗")

asset.set_root_pose(sapien.Pose([0, 0, 0.0]))

print("=== joints info ===")
for j in asset.get_joints():
    print("name:", j.name)
    print("type:", j.type)
    print("limits:", j.get_limits())
    print("------")

qpos = asset.get_qpos()
print("原本 qpos:", qpos)

if len(qpos) > 0:
    qpos = asset.get_qpos()
    qpos[0] = -0.5
    qpos[1] = -0.5

    asset.set_qpos(qpos)
    print("設定後 qpos:", asset.get_qpos())

scene.set_ambient_light([1.0, 1.0, 1.0])
scene.add_directional_light([0, 1, -1], [1.0, 1.0, 1.0])

viewer = Viewer()
viewer.set_scene(scene)
viewer.set_camera_xyz(x=3.0, y=0.0, z=2.0)
viewer.set_camera_rpy(r=0.0, p=-0.5, y=3.14)

while not viewer.closed:
    scene.step()
    scene.update_render()
    viewer.render()