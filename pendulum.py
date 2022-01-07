from manim import *
import math
#from manimlib.imports import *

'''
class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen
'''

# 3B1B Pendulum class
class Pendulum(VGroup):
    CONFIG = {
        "length": 3,
        "gravity": 9.8,
        "weight_diameter": 0.5,
        "initial_theta": PI/4,
        "omega": 0,
        "damping": 0,
        "top_point": 2 * UP,
        "rod_style": {
            "stroke_width": 3,
            "stroke_color": LIGHT_GREY,
            "sheen_direction": UP,
            "sheen_factor": 1,
        },
        "weight_style": {
            "stroke_width": 0,
            "fill_opacity": 1,
            "fill_color": GREY_BROWN,
            "sheen_direction": UL,
            "sheen_factor": 0.5,
            "background_stroke_color": BLACK,
            "background_stroke_width": 3,
            "background_stroke_opacity": 0.5,
        },
        "angle_arc_config": {
            "radius": 1,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "velocity_vector_config": {
            "color": RED,
        },
        "theta_label_height": 0.25,
        "set_theta_label_height_cap": False,
        "n_steps_per_frame": 100,
        "include_theta_label": True,
        "include_velocity_vector": False,
        "velocity_vector_multiple": 0.5,
        "max_velocity_vector_length_to_length_ratio": 0.5,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_fixed_point()
        self.create_rod()
        self.create_weight()
        self.rotating_group = VGroup(self.rod, self.weight)
        self.create_dashed_line()
        self.create_angle_arc()
        if self.CONFIG["include_theta_label"]:
            self.add_theta_label()
        if self.CONFIG["include_velocity_vector"]:
            self.add_velocity_vector()

        self.set_theta(self.CONFIG["initial_theta"])
        self.update()

    def create_fixed_point(self):
        self.fixed_point_tracker = VectorizedPoint(self.CONFIG["top_point"])
        self.add(self.fixed_point_tracker)
        return self

    def create_rod(self):
        rod = self.rod = Line(UP, DOWN)
        rod.set_height(self.CONFIG["length"])
        rod.set_style(**self.CONFIG["rod_style"])
        rod.move_to(self.get_fixed_point(), UP)
        self.add(rod)

    def create_weight(self):
        weight = self.weight = Circle()
        weight.set_width(self.CONFIG["weight_diameter"])
        weight.set_style(**self.CONFIG["weight_style"])
        weight.move_to(self.rod.get_end())
        self.add(weight)

    def create_dashed_line(self):
        line = self.dashed_line = DashedLine(
            self.get_fixed_point(),
            self.get_fixed_point() + self.CONFIG["length"] * DOWN,
        )
        line.add_updater(
            lambda l: l.move_to(self.get_fixed_point(), UP)
        )
        self.add_to_back(line)

    def create_angle_arc(self):
        self.angle_arc = always_redraw(lambda: Arc(
            arc_center=self.get_fixed_point(),
            start_angle=-90 * DEGREES,
            angle=self.get_arc_angle_theta(),
            **self.CONFIG["angle_arc_config"],
        ))
        self.add(self.angle_arc)
    
    def get_arc_angle_theta(self):
        # Might be changed in certain scenes
        return self.get_theta()
    '''
    def add_velocity_vector(self):
        def make_vector():
            omega = self.get_omega()
            theta = self.get_theta()
            mvlr = self.max_velocity_vector_length_to_length_ratio
            max_len = mvlr * self.rod.get_length()
            vvm = self.velocity_vector_multiple
            multiple = np.clip(
                vvm * omega, -max_len, max_len
            )
            vector = Vector(
                multiple * RIGHT,
                **self.velocity_vector_config,
                )
            vector.rotate(theta, about_point=ORIGIN)
            vector.shift(self.rod.get_end())
            return vector

        self.velocity_vector = always_redraw(make_vector)
        self.add(self.velocity_vector)
        return self
    '''
    def add_theta_label(self):
        self.theta_label = always_redraw(self.get_label)
        self.add(self.theta_label)

    def get_label(self):
        label = Tex('$\\theta$')
        label.set_height(self.CONFIG["theta_label_height"])
        if self.CONFIG["set_theta_label_height_cap"]:
            max_height = self.angle_arc.get_width()
            if label.get_height() > max_height:
                label.set_height(max_height)
        top = self.get_fixed_point()
        arc_center = self.angle_arc.point_from_proportion(0.5)
        vect = arc_center - top
        norm = sum([x**2 for x in vect])**0.5
        vect = normalize(vect) * (norm + self.CONFIG["theta_label_height"])
        label.move_to(top + vect)
        return label

    def get_theta(self):
        theta = self.rod.get_angle() - self.dashed_line.get_angle()
        theta = (theta + PI) % TAU - PI
        return theta

    def set_theta(self, theta):
        self.rotating_group.rotate(
            theta - self.get_theta()
        )
        self.rotating_group.shift(
            self.get_fixed_point() - self.rod.get_start(),
            )
        return self

    def get_omega(self):
        return self.CONFIG["omega"]

    def set_omega(self, omega):
        self.CONFIG["omega"] = omega
        return self

    def get_fixed_point(self):
        return self.fixed_point_tracker.get_location()

    #
    def start_swinging(self):
        self.add_updater(Pendulum.update_by_gravity)

    def end_swinging(self):
        self.remove_updater(Pendulum.update_by_gravity)

    def update_by_gravity(self, dt):
        theta = self.get_theta()
        omega = self.get_omega()
        nspf = self.CONFIG["n_steps_per_frame"]
        for x in range(nspf):
            d_theta = omega * dt / nspf
            d_omega = np.add(
                -self.CONFIG["damping"] * omega,
                -(self.CONFIG["gravity"] / self.CONFIG["length"]) * np.sin(theta),
                ) * dt / nspf
            theta += d_theta
            omega += d_omega
        self.set_theta(theta)
        self.set_omega(omega)
        return self


class PendulumUpdater(Scene):
    def construct(self):
        def ball_on_string(ball):
            ball.move_to(pendulum_string.get_end())

        def rotate_string_back(string, dt):
            string.rotate(-dt, about_point=string.get_start())

        def let_pendulum_fall(string, dt):
            theta = string.get_angle() + (PI/2)
            dtheta = -math.sqrt(9.8/5) * theta * dt
            string.rotate(dtheta, about_point=string.get_start())

        pendulum_base = Line((LEFT*3)+(UP*3), (RIGHT*3)+(UP*3))
        pendulum_string = Line(UP*3, DOWN*2)
        pendulum_ball = Circle(radius=0.5, color=GREEN)
        pendulum_ball.set_fill(color=GREEN, opacity=1)
        pendulum_ball.add_updater(ball_on_string)

        self.add(pendulum_base, pendulum_string, pendulum_ball)
        self.wait(PI/4)
        pendulum_string.add_updater(rotate_string_back)
        self.wait(PI/3)
        pendulum_string.remove_updater(rotate_string_back)
        self.wait()
        pendulum_string.add_updater(let_pendulum_fall)
        self.wait(10)
        pendulum_string.remove_updater(let_pendulum_fall)
        self.wait()


class PendulumTracker(Scene):
    def construct(self):
        def ball_on_string(ball):
            ball.move_to(pendulum_string.get_end())

        def rotate_string_back(string, dt):
            string.rotate(-dt, about_point=string.get_start())

        def draw_pendulum(string):
            string.move_to(
                UP*3, (LEFT * length * math.sin(theta.get_value())) +
                ((3 - (length * math.cos(theta.get_value()))) * DOWN)
            )

        theta_max = PI/4
        length = 5
        g = 9.8
        omega = math.sqrt(g/length)
        period = 2 * PI / omega
        pendulum_base = Line((LEFT*3)+(UP*3), (RIGHT*3)+(UP*3))
        pendulum_string = Line(UP*3, DOWN*2)
        pendulum_ball = Circle(radius=0.5, color=GREEN)
        pendulum_ball.set_fill(color=GREEN, opacity=1)
        pendulum_ball.add_updater(ball_on_string)

        total_time = ValueTracker(0)
        theta = DecimalNumber()
        theta.add_updater(lambda m: m.set_value(theta_max * math.cos(omega * total_time.get_value())))

        pendulum_string.add_updater(draw_pendulum)
        self.add(pendulum_base, pendulum_string, pendulum_ball)
        self.play(total_time.animate.set_value(3 * period), rate_func=linear, run_time=3 * period)


class Implement3B1BPendulum(Scene):
    def construct(self):
        myPend = Pendulum()
        self.add(myPend)
        self.wait()
        myPend.start_swinging()
        self.wait(7)
