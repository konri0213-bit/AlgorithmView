from manim import *
from pyglet.font.dwrite import white


def color_edges(graph, edge_names, color):
    for m in graph:
        if hasattr(m, "edge_name") and m.edge_name in edge_names:
            m.set_color(color)

class SingleCycleAlgorithm(Scene):
    def construct(self):

        VERTEX_RADIUS = 0.15
        EDGE_WIDTH = 4

        # =========================
        # 顶点坐标（保持原有）
        # =========================
        pos = {
            "a": LEFT * 2.5,
            "b": LEFT * 1.5 + UP,
            "c": LEFT * 0.5 + UP,
            "d": RIGHT * 1.1+ UP,
            "e": RIGHT * 2,
            "f": LEFT * 1 + DOWN,

            "g": LEFT * 3.5 + DOWN,
            "h": LEFT * 3.5 + UP * 0.5,

            "j": LEFT * 1.5 + DOWN* 2,
            "k": RIGHT * 2 + DOWN * 1.5,
            "l": RIGHT * 1.1 + DOWN * 2,
            "m": LEFT * 2.5 + DOWN * 2.5,
        }

        # =========================
        # 顶点
        # =========================
        V = {}
        L = {}

        for v, p in pos.items():
            color = WHITE
            if v in ["a","b","c","d","e","f"]:
                color = RED
            if v in ["g","h"]:
                color = BLUE

            dot = Dot(p, radius=VERTEX_RADIUS, color=color)
            if v == "h":
                label = Text(v, font_size=24).next_to(dot, LEFT, buff=0.05)  # 左边
            else:
                label = Text(v, font_size=24).next_to(dot, DOWN, buff=0.05)  # 默认下边
            V[v] = dot
            L[v] = label

        # =========================
        # 边
        # =========================
        def edge(u, v, color=WHITE):
            e = Line(
                V[u].get_center(),
                V[v].get_center(),
                stroke_width=EDGE_WIDTH,
                color=color
            )
            e.edge_name = "".join(sorted([u, v]))  # ef, fk, bc
            return e

        E = {
            "ab": edge("a","b"),
            "bc": edge("b","c"),
            "cd": edge("c","d"),
            "de": edge("d","e"),
            "ef": edge("e","f"),
            "fa": edge("f","a"),

            "ag": edge("a","g"),
            "gh": edge("g","h"),
            "ha": edge("h","a"),

            "fk": edge("f","k"),
            "kl": edge("k","l"),
            "gj": edge("g","j"),
            "jm": edge("j","m"),
        }

        # =========================
        # STEP 1：原始图
        # =========================
        self.play(
            *[Create(e) for e in E.values()],
            *[FadeIn(v) for v in V.values()],
            *[FadeIn(l) for l in L.values()],
            run_time=2
        )
        self.wait()

        # =========================
        # STEP 2–3：算法文字 + 箭头
        # =========================
        title = Text("単閉路アルゴリズム", font_size=36).move_to(UP*2.7)
        arrow = Arrow(title.get_bottom(), ORIGIN, buff=0.2)

        self.play(Write(title))
        self.play(GrowArrow(arrow))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(arrow))

        # 原始大图消失
        orig_graph = VGroup(*V.values(), *L.values(), *E.values())
        self.play(FadeOut(orig_graph))
        self.wait(0.5)

        # =========================
        # 创建三张小图（方式1、2、3）
        # =========================
        g1_verts = {v: V[v].copy() for v in V}
        g1_edges = {k: E[k].copy() for k in E}
        g1_labels = {v: L[v].copy() for v in L}
        g1 = VGroup(*g1_verts.values(), *g1_edges.values(), *g1_labels.values()).scale(0.63).shift(LEFT * 4)

        g2_verts = {v: V[v].copy() for v in V}
        g2_edges = {k: E[k].copy() for k in E}
        g2_labels = {v: L[v].copy() for v in L}
        g2 = VGroup(*g2_verts.values(), *g2_edges.values(), *g2_labels.values()).scale(0.63).shift(RIGHT * 1)

        g3_verts = {v: V[v].copy() for v in V}
        g3_edges = {k: E[k].copy() for k in E}
        g3_labels = {v: L[v].copy() for v in L}
        g3 = VGroup(*g3_verts.values(), *g3_edges.values(), *g3_labels.values()).scale(0.63).shift(RIGHT * 5.5)

        # 标题
        t1 = Text("方式1", font_size=24).next_to(g1, DOWN)
        t2 = Text("方式2", font_size=24).next_to(g2, DOWN)
        t3 = Text("方式3", font_size=24).next_to(g3, DOWN)

        # 显示三张小图
        self.play(
            FadeIn(g1), FadeIn(g2), FadeIn(g3),
            FadeIn(t1), FadeIn(t2), FadeIn(t3),
            run_time=2
        )
        self.wait(1)

        # =========================
        # 染色动画
        # =========================
        color_edges(g1_edges.values(), ["ef", "fk", "kl"], RED)
        color_edges(g1_edges.values(), ["bc", "cd", "de"], YELLOW)

        color_edges(g2_edges.values(), ["af", "fk", "kl"], YELLOW)
        color_edges(g2_edges.values(), ["cd", "de", "ef"], RED)

        color_edges(g3_edges.values(), ["af", "fk", "kl"], YELLOW)
        color_edges(g3_edges.values(), ["ab", "bc", "cd"], RED)
        self.wait(2)

        # =========================
        # 消失指定边和顶点
        # =========================
        self.play(
            # 方式1边变淡
            *[g1_edges[k].animate.set_opacity(0.2) for k in ["ef", "fk", "kl", "bc", "cd", "de"]],
            # 方式1顶点变淡
            *[g1_verts[v].animate.set_opacity(0.2) for v in ["c", "d", "e", "k", "l"]],
            # 方式1标签变淡
            *[g1_labels[v].animate.set_opacity(0.2) for v in ["c", "d", "e", "k", "l"]],

            # 方式2边变淡
            *[g2_edges[k].animate.set_opacity(0.2) for k in ["fa", "fk", "kl", "cd", "de", "ef"]],
            # 方式2顶点变淡
            *[g2_verts[v].animate.set_opacity(0.2) for v in ["d", "e", "f", "k", "l"]],
            # 方式2标签变淡
            *[g2_labels[v].animate.set_opacity(0.2) for v in ["d", "e", "f", "k", "l"]],

            # 方式3边变淡
            *[g3_edges[k].animate.set_opacity(0.2) for k in ["fa", "fk", "kl", "ab", "bc", "cd"]],
            # 方式3顶点变淡
            *[g3_verts[v].animate.set_opacity(0.2) for v in ["b", "c", "k", "l"]],
            # 方式3标签变淡
            *[g3_labels[v].animate.set_opacity(0.2) for v in ["b", "c", "k", "l"]],

            run_time=2
        )
        self.wait()

        # =========================
        # STEP 13：方式1和方式2有利
        # =========================
        better = Text("方式1と方式2が有利", font_size=32).move_to(UP * 2)
        cross = Text("✕", font_size=72, color=RED).move_to(g3.get_center())

        self.play(Write(better))
        self.play(FadeIn(cross))
        self.wait()

        self.play(FadeOut(better))
        self.play(FadeOut(cross))
        # 彻底消失 g3
        self.play(
            # 消失 g3 的所有边
            *[FadeOut(g3_edges[k]) for k in g3_edges],
            # 消失 g3 的所有顶点
            *[FadeOut(g3_verts[v]) for v in g3_verts],
            # 消失 g3 的所有标签
            *[FadeOut(g3_labels[v]) for v in g3_labels],
            FadeOut(t3),  # t3 是单个物体，不需要使用 *[...] 语法
            run_time=2
        )

        self.wait()
        # =========================
        # STEP 14–15：方式1失败
        # =========================
        # 方式1黄色边和顶点
        g1_group = VGroup(*g1_verts.values(), *g1_edges.values(), *g1_labels.values())
        g2_group = VGroup(*g2_verts.values(), *g2_edges.values(), *g2_labels.values())

        yellow_edges = [g1_edges[k] for k in ["bc", "cd", "de"]]
        yellow_verts = [g1_verts[v] for v in ["c", "d", "e"]]
        yellow_edgess = [g2_edges[k] for k in ["fa", "fk", "kl"]]
        yellow_vertss =  [g2_verts[v] for v in ["f", "k", "l"]]
        # 方式1红色边和顶点
        red_edges = [g1_edges[k] for k in ["ef", "fk", "kl"]]
        red_verts = [g1_verts[v] for v in ["k","e","l"]]  # 如果红色顶点还需要闪烁

        # ---------- STEP: 方式2向右平移 ----------
        shift_vector2 = RIGHT * 5# 向右移动 2 单位

        g2_group = VGroup(
            *g2_edges.values(),  # 所有边
            *g2_verts.values(),  # 所有顶点
            *g2_labels.values(),  # 所有标签
            t2  # 方式2的标题
        )
        self.play(g2_group.animate.shift(shift_vector2), run_time=2)
        self.wait(0.5)

        # 创建形態V图（V_group）
        # =========================
        # 假设形態V是在原图基础上删除了边 cd, de, fk, kl，删除顶点 d, k, l
        V_group_verts = {v: V[v].copy() for v in V if v not in ["d", "e", "l"]}
        V_group_edges = {k: E[k].copy() for k in E if k not in ["cd", "de", "ef", "kl"]}
        V_group_labels = {v: L[v].copy() for v in V if v not in ["d", "e", "l"]}

        V_group = VGroup(*V_group_verts.values(), *V_group_edges.values(), *V_group_labels.values(),).scale(0.63)
        t4 = Text("形態Ｖ", font_size=24).next_to(V_group, DOWN)
        # 放到方式1和方式2中间
        middle_pos = (g1.get_center() + g2_group.get_center()) / 2
        V_group.move_to(middle_pos)

        # =========================
        # 方式2先向右平移
        # =========================

        # =========================
        # 形態V在中间停留1秒
        # =========================
        self.play(FadeIn(V_group),FadeIn(t4))
        self.wait()

        subtitle1 = Text(
            "黄色のP4を追加した後、形態Vを形成できない。",
            font_size=28,  # 字体大小可调整
            color=WHITE
        ).to_edge(UP)  # 放在屏幕底部
        subtitle2 = Text(
            "赤のP4を追加した後、形態Vを形成できない。",
            font_size=28,  # 字体大小可调整
            color=WHITE
        ).to_edge(UP)  # 放在屏幕底部
        # ----------------------------
        # 1️⃣ 黄色闪烁
        self.play(
            LaggedStart(
                *[
                    m.animate(rate_func=there_and_back)
                    .set_color(YELLOW_E)  # 变深色
                    .set_opacity(1)  # 变不透明
                    .scale(1.3)  # 放大
                    for m in yellow_edges + yellow_verts
                ],
                lag_ratio=0.2
            ),
            run_time=1.5
        )
        fe_edge_obj = V_group_edges["fk"]  # 形态V中 ef 边
        for _ in range(5):  # 闪烁5次
            self.play(
                fe_edge_obj.animate.set_color(RED).set_opacity(1),
                run_time=0.15
            )
        self.play(
                fe_edge_obj.animate.set_color(WHITE).set_opacity(1),
                Write(subtitle1),
                run_time=0.15
            )
        self.wait(1)  # 等待 1.5 秒
        self.play(FadeOut(subtitle1))



        # ----------------------------
        self.play(
            LaggedStart(
                *[
                    m.animate(rate_func=there_and_back)
                    .set_color(RED_E)  # 变深色
                    .set_opacity(1)  # 变不透明
                    .scale(1.3)  # 放大
                    for m in red_edges + red_verts
                ],
                lag_ratio=0.2
            ),
            run_time=1.5
        )

        fe_edge_obj1= V_group_edges["bc"]  # 形态V中 ef 边
        for _ in range(5):  # 闪烁5次
            self.play(
                fe_edge_obj1.animate.set_color(RED).set_opacity(1),
                run_time=0.15
            )
        self.play(
                fe_edge_obj1.animate.set_color(WHITE).set_opacity(1),
                Write(subtitle2),
                run_time=0.15
            )

        self.wait(1)  # 等待 1.5 秒
        self.play(FadeOut(subtitle2))

        # 添加日语字幕
        subtitle = Text(
            "どの P_4 を補充しても、図中には形態 V が含まれない",
            font_size=28,  # 字体大小可调整
            color=WHITE
        ).to_edge(UP)  # 放在屏幕底部

        # 显示字幕
        self.play(Write(subtitle))
        self.wait(1)  # 等待 2 秒
        self.play(FadeOut(subtitle))

        fail = Paragraph(
            "形態Vを形成できない",
            "形態IVを維持し",
            "次のステップへ進む",
            font_size=28,
            line_spacing=1.2,
            alignment="center"  # 注意这里是小写
        ).next_to(g1, UP)
        self.play(Write(fail))
        self.wait(2)
        self.play(FadeOut(fail))

        ok = Text("形態Vを形成できる", font_size=28).next_to(g2, UP)
        # =========================
        # STEP 16–18：方式2成功
        # =========================
        self.play(
            LaggedStart(
                *[
                    m.animate(rate_func=there_and_back)
                    .set_color(YELLOW_E)  # 变深色
                    .set_opacity(1)  # 变不透明
                    .scale(1.3)  # 放大
                    for m in yellow_edgess + yellow_vertss
                ],
                lag_ratio=0.2
            ),
            run_time=1.5
        )
        self.play(
            *[g2_edges[k].animate.set_opacity(1) for k in ["fa", "fk"]],
            # 方式2顶点变深
            *[g2_verts[v].animate.set_opacity(1) for v in ["f", "k"]],
            # 方式2标签变深
            *[g2_labels[v].animate.set_opacity(1) for v in ["f", "k"]],
            run_time=2
        )
        # 1. 零件筛选：必须用 k (key) 去比对字符串列表
        edges_in_V = [e for k, e in g2_edges.items() if k not in ["kl", "cd", "de", "ef"]]
        verts_in_V = [v for k, v in g2_verts.items() if k not in ["d", "e", "l"]]  # 这里之前是 v，一定要改写为 k
        labels_in_V = [l for k, l in g2_labels.items() if k not in ["d", "e", "l"]]  # 这里同理，改写为 k

        items_group = VGroup(*edges_in_V, *verts_in_V, *labels_in_V)

        # 2. V_group 动画组筛选：通过直接对比对象来过滤
        # 既然 items_group 已经正确过滤了，我们甚至可以只让 items_group 动画
        # 或者通过以下方式彻底排除这三个点
        excluded_mobs = [g2_verts["d"], g2_verts["e"], g2_verts["l"],
                         g2_labels["d"], g2_labels["e"], g2_labels["l"]]

        v_group_to_animate = VGroup(*[m for m in V_group if m not in excluded_mobs])

        # 3. 执行动画
        self.play(
            items_group.animate(rate_func=there_and_back)
            .set_color(RED_E)
            .set_opacity(1)
            .scale(1.3),

            v_group_to_animate.animate(rate_func=there_and_back)
            .set_color(RED_E)
            .set_opacity(1)
            .scale(1.3),

            Write(ok),
            run_time=2.5
        )
        self.play(FadeOut(ok))

        self.play(
            # 方式1消失 (解包列表)
            *[FadeOut(g1_edges[k]) for k in ["ef", "fk", "kl", "bc", "cd", "de"]],
            *[FadeOut(g1_verts[v]) for v in ["c", "d", "e", "k", "l"]],
            *[FadeOut(g1_labels[v]) for v in ["c", "d", "e", "k", "l"]],

            # 方式2消失 (解包列表)
            *[FadeOut(g2_edges[k]) for k in ["kl", "cd", "de", "ef"]],
            *[FadeOut(g2_verts[v]) for v in ["d", "e", "l"]],
            *[FadeOut(g2_labels[v]) for v in ["d", "e", "l"]],

            # 单个对象消失 (不加星号)
            FadeOut(V_group),
            FadeOut(t4),

            run_time=2
        )
        t6 =Text("形態IV", font_size=24)

        edges_to_move = [e for k, e in g1_edges.items() if k not in ["bc", "cd", "de", "fk", "kl", "ef"]]
        verts_to_move = [v for k, v in g1_verts.items() if k not in ["d", "e", "c", "k", "l"]]
        labels_to_move = [l for k, l in g1_labels.items() if k not in ["d", "e", "c", "k", "l"]]
        move_group = VGroup(*edges_to_move, *verts_to_move, *labels_to_move,t2)
        shift_vector1 = RIGHT * 2
        shift_vector3 = LEFT * 2

        # --- 2. 执行复合动画 ---
        # --- 1. 预对齐目标 ---
        t6.move_to(t1)
        t4.move_to(t2)

        # --- 2. 提前计算目标的终点坐标 ---
        # 我们直接修改 t6 和 t4 的坐标，而不是生成动画对象
        target_t6 = t6.copy().shift(shift_vector1)
        target_t4 = t4.copy().shift(shift_vector3)

        # --- 3. 执行动画 ---
        self.play(
            items_group.animate.shift(shift_vector3),
            move_group.animate.shift(shift_vector1),

            # 这里直接填入目标物体（target_t6 / target_t4）
            # Transform 过程会自动产生从起点到终点的平滑移动
            FadeTransform(t1, target_t6),
            ReplacementTransform(t2, target_t4),

            run_time=2
        )
        self.wait(0.5)

        alg = Text("単閉路アルゴリズム", font_size=36).move_to(UP * 2.8)
        self.play(Transform(title, alg))
        self.wait(0.5)
        self.play(FadeOut(title, alg))

        color_edges(g1_edges.values(), ["ag", "gj", "jm"], RED)
        color_edges(g1_edges.values(), ["gh", "ah", "ab"], YELLOW)
        color_edges(g2_edges.values(), ["ah", "ab", "bc"], BLUE)
        color_edges(g2_edges.values(), ["gh", "gj", "jm"], RED)
        color_edges(g2_edges.values(), ["ag"], YELLOW)

        self.wait(0.5)

        s2 = Text("サイズ2", font_size=24).next_to(g1, DOWN)
        s3 = Text("サイズ3", font_size=24).next_to(g2, DOWN)
        self.play(
        Transform(target_t6, s2),
                Transform(target_t4, s3),
            run_time=0.5
        )
        # =========================
        # STEP 19：两张结果图
        # =========================
        left = Text("結果1", font_size=24).move_to(LEFT*4 + UP*2)
        right = Text("結果2", font_size=24).move_to(RIGHT*4 + UP*2)

        self.play(Write(left), Write(right))
        self.wait()
        self.play(FadeOut(left), FadeOut(right))

        self.play(FadeOut(target_t4),
        run_time = 0.5
                  )

        # 1. 定义需要复活的边（注意：根据之前的逻辑，ha 应该写成 ah）
        adjustment = LEFT * 1
        g2_verts["d"].shift(adjustment)
        g2_verts["e"].shift(adjustment)
        g2_labels["d"].shift(adjustment)
        g2_labels["e"].shift(adjustment)
        restore_keys = ["cd", "de", "ef"]

        # 2. 预处理：同步位置、透明度和粗细
        for v_key in ["d", "e"]:
            g2_verts[v_key].shift(adjustment)
            g2_labels[v_key].shift(adjustment)

        # 3. 核心：重连所有受影响的边（包括已经在图里的和还没显示的）
        # 这样当 g2 第一次出现时，它的形状就是已经“收缩”过的
        all_affected_edges = ["cd", "de", "ef", "bc"]  # 凡是连接到 d, e 的边都要重连
        for k in all_affected_edges:
            if k in g2_edges:
                u, v = k[0], k[1]
                g2_edges[k].put_start_and_end_on(
                    g2_verts[u].get_center(),
                    g2_verts[v].get_center()
                )
        new_green_edges = VGroup()

        for k in ["cd", "de", "ef"]:
            u, v = k[0], k[1]
            # 直接根据现在屏幕上顶点的位置创建新线
            line = Line(
                g2_verts[u].get_center(),
                g2_verts[v].get_center(),
                stroke_width=8,  # 强制加粗
                color=PURE_GREEN  # 使用最亮的绿色
            ).set_z_index(100)  # 确保在最顶层，不被任何东西遮挡
            new_green_edges.add(line)

        for v_key in ["d", "e"]:
            target_dot = g2_verts[v_key]
            target_label = g2_labels[v_key]

            # 确保它们就在绿线的端点上
            # 强制不透明，颜色设为醒目的白色（或红色，根据你初始顶点的颜色）
            target_dot.set_opacity(1).set_color(RED).set_z_index(20).scale(1.2)
            target_label.set_opacity(1).set_color(WHITE).set_z_index(20)

        # 3. 执行同步动画
        self.play(
            Create(new_green_edges),
            # 这里的 FadeIn 会把之前消失的点和标记重新变回可见
            FadeIn(g2_verts["d"]),
            FadeIn(g2_labels["d"]),
            FadeIn(g2_verts["e"]),
            FadeIn(g2_labels["e"]),
            run_time=1
        )

        # 3. 震荡强调：如果还不明显，就让它跳动一下
        self.play(
            new_green_edges.animate.scale(1.2),
            rate_func=wiggle,
            run_time=0.5
        )
        g1_full_group = VGroup(g1_group, target_t6)
        u, v = "k", "l"
        # 物理对齐：确保它连接在最新的 k 和 l 顶点位置上
        g2_edges["kl"].put_start_and_end_on(
            g2_verts[u].get_center(),
            g2_verts[v].get_center()
        )

        # 视觉设置：白色、不透明、匹配缩放后的粗细
        g2_edges["kl"].set_color(WHITE)
        g2_edges["kl"].set_opacity(1)
        g2_edges["kl"].set_stroke(width=EDGE_WIDTH * 0.63)

        # 2. 如果顶点 k 和 l 也看不清，同步把它们捞回来
        for v_key in ["k", "l"]:
            g2_verts[v_key].set_opacity(1).set_color(RED).set_z_index(20)
            g2_labels[v_key].set_opacity(1).set_color(WHITE).set_z_index(20)

        # 1. 识别需要消失的残留物
        # 形态V 的文本应该是 t4
        # 顶点 l 在方式2中可能叫 g2_verts["l"] 或者 g2_labels["l"]
        self.play(
            FadeIn(g2_edges["kl"]),
            FadeIn(g2_verts["k"]), FadeIn(g2_labels["k"]),
            FadeIn(g2_verts["l"]), FadeIn(g2_labels["l"]),
            run_time=1.5
        )
        final_v2 = VGroup(
            g2_group,
            new_green_edges,
            g2_edges["kl"],
            g2_verts["k"], g2_labels["k"],  # 显式加入顶点和标签
            g2_verts["l"], g2_labels["l"],
            target_t4
        )
        # 2. 执行最终合并动画
        final_pure_v2 = VGroup(
            *[g2_verts[v] for v in g2_verts],  # 所有的点
            *[g2_labels[v] for v in g2_labels],  # 所有的标签

            # 【核心修正】排除 kl (为了用新的白边) 和 cd, de, ef (为了用新的绿边)
            *[g2_edges[e] for e in g2_edges if e not in ["kl", "cd", "de", "ef"]],

            g2_edges["kl"],  # 我们修复过的那条白色粗边
            new_green_edges  # 那三条绿色粗边
        )

        # 2. 物理清除所有干扰项（文本和旧组）
        self.remove(t4, t6, target_t6, target_t4, s2, s3, g1_group, g2_group)

        # 3. 执行最终位移动画
        self.play(
            # 强制让场景中所有“编外人员”消失
            *[m.animate.set_opacity(0) for m in self.mobjects if m not in final_pure_v2.get_family()],

            final_pure_v2.animate.move_to(ORIGIN),
            run_time=1.5
        )



        # 3. 执行平滑的浮现动画（不跳动，用 FadeIn）

        # =========================
        # STEP 22：最优解
        # =========================
        opt = Text("最適解", font_size=36, color=GREEN).move_to(DOWN*2.8)

        self.play(Write(opt))
        self.wait(2)

