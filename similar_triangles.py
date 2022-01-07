from manim import *
import math


class SimilarTriangles(Scene):
    def construct(self):
        def get_length_triangle_side(triangle, vertex1, vertex2, decimal_places):
            return round(math.sqrt(((triangle.get_vertices()[vertex1][0] -
                                     triangle.get_vertices()[vertex2][0]) ** 2) +
                                   ((triangle.get_vertices()[vertex1][1] -
                                     triangle.get_vertices()[vertex2][1]) ** 2)), decimal_places)

        title = Text("Similar Triangles")
        ratios = MathTex("\\frac{a_1}{b_1} = \\frac{x}{b_2}")
        VGroup(title, ratios).arrange(DOWN)
        self.play(
            Write(title),
            Write(ratios),
        )
        self.wait()

        transform_title = Text("They don't have to be so complicated")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            FadeOut(ratios),
        )
        self.wait()
        triangle_big = Polygon(LEFT + 2*DOWN, RIGHT + 2*DOWN, UP*(math.sqrt(77.0)/2) + 2*DOWN)
        triangle_small = Polygon(LEFT + 2*DOWN, RIGHT + 2*DOWN, UP*(math.sqrt(77.0)/2) + 2*DOWN)

        triangle_small.scale(0.5, about_point=triangle_big.get_vertices()[1])
        triangle_small.set_stroke(PINK)
        # triangle_small.align_to(triangle_big, DL)
        self.play(ShowCreation(triangle_big))
        self.wait()
        self.play(ShowCreation(triangle_small))
        self.wait()
        print(np.round(triangle_big.get_vertices(), 2))
        print()
        print(np.round(triangle_small.get_vertices(), 2))

        triangle_small_0_1_length_calculation = get_length_triangle_side(triangle_small, 0, 1, 2)
        triangle_small_1_2_length_calculation = get_length_triangle_side(triangle_small, 1, 2, 2)
        triangle_small_0_2_length_calculation = get_length_triangle_side(triangle_small, 0, 2, 2)

        triangle_big_0_1_length_calculation = get_length_triangle_side(triangle_big, 0, 1, 2)
        triangle_big_1_2_length_calculation = get_length_triangle_side(triangle_big, 1, 2, 2)
        triangle_big_0_2_length_calculation = get_length_triangle_side(triangle_big, 0, 2, 2)

        triangle_small_0_1_length = DecimalNumber(
            triangle_small_0_1_length_calculation,
            show_ellipsis=False,
            num_decimal_places=2,
            include_sign=False,
        )

        triangle_small_1_2_length = DecimalNumber(
            triangle_small_1_2_length_calculation,
            show_ellipsis=False,
            num_decimal_places=2,
            include_sign=False,
        )

        triangle_small_0_2_length = DecimalNumber(
            triangle_small_0_2_length_calculation,
            show_ellipsis=False,
            num_decimal_places=2,
            include_sign=False,
        )

        triangle_big_0_1_length = DecimalNumber(
            triangle_big_0_1_length_calculation,
            show_ellipsis=False,
            num_decimal_places=2,
            include_sign=False,
        )

        triangle_big_1_2_length = DecimalNumber(
            triangle_big_1_2_length_calculation,
            show_ellipsis=False,
            num_decimal_places=2,
            include_sign=False,
        )

        triangle_big_0_2_length = DecimalNumber(
            triangle_big_0_2_length_calculation,
            show_ellipsis=False,
            num_decimal_places=2,
            include_sign=False,
        )

        print(triangle_small_0_1_length_calculation)
        triangle_small_0_1_length.scale(0.75)
        triangle_small_0_1_length.next_to(triangle_small, 0.5*DOWN)
        triangle_small_1_2_length.scale(0.75)
        triangle_small_1_2_length.next_to(triangle_small, 0.5*RIGHT)
        triangle_small_0_2_length.scale(0.75)
        triangle_small_0_2_length.next_to(triangle_small, 0.5*LEFT)
        # triangle_small_0_1_length.add_updater(lambda d: d.next_to(triangle_small, LEFT))
        # triangle_small_0_1_length.add_updater(lambda d: d.set_value(triangle_small_0_1_length_calculation))
        #triangle_small_scaled_up = Triangle().align_to(triangle_big, DL)
        #triangle_small_scaled_up.set_stroke(PINK)
        self.play(
            Write(triangle_small_0_1_length),
            Write(triangle_small_1_2_length),
            Write(triangle_small_0_2_length),
        )
        self.wait()
        self.play(
            #Transform(triangle_small, triangle_small_scaled_up),
            ApplyMethod(triangle_small.scale, 2, {"about_point": triangle_big.get_vertices()[1]}),
            Transform(triangle_small_0_1_length, triangle_big_0_1_length.move_to(np.array([0, -2.5, 0]))),
            Transform(triangle_small_1_2_length, triangle_big_1_2_length.move_to(np.array([1.5, 0.25, 0]))),
            Transform(triangle_small_0_2_length, triangle_big_0_2_length.move_to(np.array([-1.5, 0.25, 0]))),
        )
