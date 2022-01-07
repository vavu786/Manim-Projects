from manim import *


class CalculusConcepts(Scene):
    def construct(self):
        xyPlane = Axes(
            x_range=(0, 5),
            y_range=(0, 25, 5),
            x_length=5,
            axis_config={"include_numbers": True},
        )
        xyPlane.move_to(ORIGIN)
        xSquaredFunction = lambda x: x**2
        xSquared = xyPlane.get_graph(xSquaredFunction, color=RED)
        xSquaredName = MathTex("y=x^2")
        xSquaredName.next_to(xSquared)
        xSquaredName.set_color(RED)

        self.wait()
        self.add(xyPlane)
        self.add(xyPlane.get_y_axis_label("Position", UP*4 + LEFT*0.5).set_color(GREEN))
        self.add(xyPlane.get_x_axis_label("Time", DOWN*0.5 + RIGHT).set_color(GREEN))
        self.wait()
        self.play(Create(xSquared), run_time=2)
        self.wait()
        self.play(Write(xSquaredName))
