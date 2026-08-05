"""
NX 12.0 NXOpen Python 脚本 - 创建深沟球轴承 (6205型)

使用方法:
    1. 打开 NX 12.0
    2. File → Execute → NX Open (或 Journal)
    3. 选择本文件运行

说明:
    在原点处创建一个立式深沟球轴承，旋转轴为 Z 轴。
    包含: 外圈、内圈、滚珠 (环形阵列)
"""

import NXOpen
import math


def create_sketch_on_xz_plane(work_part, session):
    """在 XZ 平面上创建草图，用于绘制轴承截面"""
    mark_id = session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "创建草图")

    sketch_builder = work_part.Sketches.CreateSketchBuilder()

    # 设置草图平面为 XZ (法向 = Y)
    origin = NXOpen.Point3D(0.0, 0.0, 0.0)
    normal = NXOpen.Vector3d(0.0, -1.0, 0.0)
    x_dir = NXOpen.Vector3d(1.0, 0.0, 0.0)

    sketch_builder.SetPlane(origin, normal, x_dir)
    sketch = sketch_builder.CommitSketch()

    session.DeleteUndoMark(mark_id, None)
    return sketch


def draw_rectangle(sketch, x1, y1, x2, y2):
    """在草图中绘制矩形 (左下角到右上角)"""
    lines = []
    # 四条边
    pts = [
        (x1, y1, x2, y1),  # 底边
        (x2, y1, x2, y2),  # 右边
        (x2, y2, x1, y2),  # 顶边
        (x1, y2, x1, y1),  # 左边
    ]
    for (x0, y0, x1, y1) in pts:
        line = sketch.CreateLine(
            NXOpen.Point3D(x0, y0, 0.0),
            NXOpen.Point3D(x1, y1, 0.0),
        )
        lines.append(line)
    return lines


def create_revolve(work_part, session, sketch, angle_deg):
    """将草图截面绕 Z 轴旋转创建实体"""
    mark_id = session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "创建旋转体")

    revolve_builder = work_part.Features.CreateRevolveBuilder()

    # 设置截面 - 使用草图所有曲线
    section_builder = revolve_builder.Section
    section_builder.AllowSelfIntersection(True)

    # 添加几何体到截面
    for line in sketch.GetAllLines():
        section_builder.AddToSection(
            line, NXOpen.Point3D(0, 0, 0),
            NXOpen.SmartSelectionNull.Create(),
            None, None,
        )

    # 设置旋转轴 (Z 轴)
    revolve_builder.AxisPoint = NXOpen.Point3D(0.0, 0.0, 0.0)
    revolve_builder.AxisDirection = NXOpen.Vector3d(0.0, 0.0, 1.0)

    # 设置旋转角度
    revolve_builder.Limits.StartExtend.Value.RightHandSide = 0.0
    revolve_builder.Limits.EndExtend.Value.RightHandSide = angle_deg

    # 创建特征
    revolve_feature = revolve_builder.CommitFeature()

    session.DeleteUndoMark(mark_id, None)
    return revolve_feature


def create_sphere(work_part, session, center_x, center_y, center_z, diameter):
    """在指定位置创建球体"""
    mark_id = session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "创建球体")

    sphere_builder = work_part.Features.CreateSphereBuilder()

    # 设置球心
    sphere_builder.CenterPoint = NXOpen.Point3D(center_x, center_y, center_z)
    sphere_builder.Diameter.Value.RightHandSide = diameter

    sphere_feature = sphere_builder.CommitFeature()

    session.DeleteUndoMark(mark_id, None)
    return sphere_feature


def create_circular_pattern(work_part, session, feature, center_x, center_y, center_z, count):
    """创建圆形阵列特征"""
    mark_id = session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "创建圆形阵列")

    pattern_builder = work_part.Features.CreateCircularPatternBuilder()

    # 设置阵列参数
    pattern_builder.Formula = NXOpen.Features.PatternBuilder.Formulas.Simple
    pattern_builder.SimpleSpacing.Count = count
    pattern_builder.SimpleSpacing.AngularSpacing.Value.RightHandSide = 360.0 / count

    # 设置旋转轴 (Z 轴)
    pattern_builder.RotationAxis = NXOpen.Direction3d(
        NXOpen.Point3D(center_x, center_y, center_z),
        NXOpen.Vector3d(0.0, 0.0, 1.0),
    )

    # 添加特征到阵列
    pattern_builder.PatternObjects.Append(feature)

    pattern_feature = pattern_builder.CommitFeature()

    session.DeleteUndoMark(mark_id, None)
    return pattern_feature


def create_bearing():
    """主函数: 创建深沟球轴承"""
    the_session = NXOpen.Session.GetSession()
    work_part = the_session.Parts.Work

    if work_part is None:
        print("错误: 请先新建或打开一个 Part 文件")
        return

    # ============================================================
    # 轴承参数 (6205 深沟球轴承)
    # ============================================================
    inner_dia = 25.0      # 内径 (mm)
    outer_dia = 52.0      # 外径 (mm)
    width = 15.0          # 宽度 (mm)
    ball_dia = 7.94       # 滚珠直径 (mm)
    num_balls = 9         # 滚珠数量

    # 计算半径
    outer_ring_od = outer_dia / 2.0       # 外圈外半径 = 26.0
    outer_ring_id = outer_ring_od - 5.5   # 外圈内半径 = 20.5
    inner_ring_id = inner_dia / 2.0       # 内圈内半径 = 12.5
    inner_ring_od = inner_ring_id + 5.5   # 内圈外半径 = 18.0
    pitch_radius = (outer_ring_id + inner_ring_od) / 2.0  # 滚珠节圆半径 ≈ 19.25
    half_w = width / 2.0                  # 半宽 = 7.5

    print("=" * 50)
    print("开始创建 6205 深沟球轴承...")
    print(f"  外径: {outer_dia} mm")
    print(f"  内径: {inner_dia} mm")
    print(f"  宽度: {width} mm")
    print(f"  滚珠: Ø{ball_dia} mm × {num_balls} 颗")
    print("=" * 50)

    # ============================================================
    # 第1步: 创建外圈 (旋转体)
    # ============================================================
    print("[1/4] 创建外圈...")
    sketch_outer = create_sketch_on_xz_plane(work_part, the_session)
    draw_rectangle(sketch_outer, outer_ring_id, -half_w, outer_ring_od, half_w)
    create_revolve(work_part, the_session, sketch_outer, 360.0)
    print("      外圈创建完成 ✓")

    # ============================================================
    # 第2步: 创建内圈 (旋转体)
    # ============================================================
    print("[2/4] 创建内圈...")
    sketch_inner = create_sketch_on_xz_plane(work_part, the_session)
    draw_rectangle(sketch_inner, inner_ring_id, -half_w, inner_ring_od, half_w)
    create_revolve(work_part, the_session, sketch_inner, 360.0)
    print("      内圈创建完成 ✓")

    # ============================================================
    # 第3步: 创建第一个滚珠 (球体)
    # ============================================================
    print("[3/4] 创建滚珠...")
    # 第一个滚珠位于 X 轴正方向，Z=0 (居中)
    sphere = create_sphere(
        work_part, the_session,
        pitch_radius, 0.0, 0.0, ball_dia,
    )
    print(f"      第一个滚珠创建完成 ✓")

    # ============================================================
    # 第4步: 环形阵列滚珠
    # ============================================================
    print(f"[4/4] 环形阵列滚珠 ({num_balls} 颗)...")
    create_circular_pattern(
        work_part, the_session,
        sphere, 0.0, 0.0, 0.0, num_balls,
    )
    print("      阵列完成 ✓")

    # ============================================================
    # 完成
    # ============================================================
    print("=" * 50)
    print("轴承创建完成! 🎉")
    print(f"  文件: {work_part.FullPath}")
    print("=" * 50)


if __name__ == "__main__":
    create_bearing()
*** End of File
