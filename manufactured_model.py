import math
from offer_object import Object


PI = 3.1415
WELDING_LENGTH = 20
FEMALE = 33
MALE = 10
EXTENSION = 40
FLANGE_CUT = 30
AREA_DEMULTIPLICATOR = 10 ** (-6)
LENGTH_DEMULTIPLICATOR = 10 ** (-3)
RACORD_LENGHT = 70


class RectangularStraight(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.width = self.ch_A()
        self.height = self.ch_B()
        self.length = self.ch_C()
        self.quantity = self.quantity()

    def item_name(self):
        return self.name

    def item_characteristics(self):
        return f"{int(self.width)}x{int(self.height)} L{int(self.length)}"

    def characteristics(self):
        return f"{self.width}x{self.height} L={self.length}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.item_characteristics()}"

    def label_field_A(self):
        return f"{self.width}x{self.height}"

    def label_field_B(self):
        return f"L={self.length}"

    def label_field_C(self):
        return False

    def item_thickness(self):
        item_lat = [self.width, self.height]
        return self.rectangular_thickness(item_lat)

    def area(self):
        return round(
            ((self.width * 2 + self.height * 2 + FEMALE + MALE) * self.length)
            * AREA_DEMULTIPLICATOR,
            2,
        )

    def total_area(self):
        area = self.area() * self.quantity
        return round(area, 2)

    def flange(self):
        flange = (
            (((self.width - FLANGE_CUT) * 2 + (self.height - FLANGE_CUT) * 2))
            * LENGTH_DEMULTIPLICATOR
        ) * 2
        return round(flange, 2)

    def total_flange(self):
        flange = self.flange() * self.quantity
        return round(flange, 2)

    def corners(self):
        return 8

    def total_corners(self):
        return self.corners() * self.quantity


class RectangularElbow(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.width = self.ch_A()
        self.height = self.ch_B()
        self.angle = self.ch_C()
        self.quantity = self.quantity()
        self.radius = self.ch_D() or 150

    def item_complete_name(self):
        return f"{self.name} {int(self.width)}x{int(self.height)} {int(self.angle)}degree Radius={int(self.radius)}"

    def item_name(self):
        return self.name

    def characteristics(self):
        return f"{int(self.width)}x{int(self.height)} {int(self.angle)}degree Radius={int(self.radius)}"

    def label_field_A(self):
        return f"{int(self.width)}x{int(self.height)}"

    def label_field_B(self):
        return f"{int(self.angle)}degree"

    def label_field_C(self):
        return f"Radius={int(self.radius)}"

    def item_thickness(self):
        item_lat = [self.width, self.height]
        return self.rectangular_thickness(item_lat)

    def top_area(self):
        return (
            (
                PI
                * ((self.width + self.radius - MALE) ** 2 - (self.radius + MALE) ** 2)
                * (AREA_DEMULTIPLICATOR)
            )
            * self.angle
            / 360
        )

    def lateral_area(self):
        return (
            (self.height + 2 * FEMALE)
            * ((2 * PI * (self.width + self.radius) + 2 * EXTENSION))
            * (AREA_DEMULTIPLICATOR)
        ) * (self.angle / 360)

    def small_side_area(self):
        return (
            (self.height + 2 * FEMALE)
            * ((2 * PI * (self.radius)))
            * (AREA_DEMULTIPLICATOR)
            * (self.angle / 360)
        )

    def area(self):
        return round(
            self.top_area() * 2 + self.lateral_area() + self.small_side_area(), 2
        )

    def true_area(self):
        return round(self.area() + (0.10 * self.area()), 2)

    def total_area(self):
        return self.area() * self.quantity

    def total_true_area(self):
        return self.true_area() * self.quantity

    def flange(self):
        return round((self.height * 4 + self.width * 4) * LENGTH_DEMULTIPLICATOR, 2)

    def total_flange(self):
        return self.flange() * self.quantity

    def corners(self):
        return 8

    def total_corners(self):
        return self.corners() * self.quantity


class RectangularReduction(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.A_width = self.ch_A()
        self.A_height = self.ch_B()
        self.B_width = self.ch_C()
        self.B_height = self.ch_D()
        self.length = self.ch_E()
        self.quantity = self.quantity()
        self.model = self.ch_F() or 1

    def item_name(self):
        return self.name

    def characteristics(self):
        return [
            self.A_width,
            self.A_height,
            self.B_width,
            self.B_height,
            self.length,
            self.model,
        ]

    def item_characteristics(self):
        return f"{int(self.A_width)}x{int(self.A_height)} - {int(self.B_width)}x{int(self.B_height)} L{int(self.length)} model{int(self.model)}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.item_characteristics}"

    def label_field_A(self):
        return f"{int(self.A_width)}x{int(self.A_height)}"

    def label_field_B(self):
        return f"{int(self.B_width)}x{int(self.B_height)}"

    def label_field_C(self):
        return f"L{int(self.length)} model{int(self.model)}"

    def item_thickness(self):
        item_lat = [self.A_width, self.A_height, self.B_width, self.B_height]
        return self.rectangular_thickness(item_lat)

    def area_top(self):
        if self.model in [1, 6]:
            total_width_A = self.A_width + FEMALE * 2
            total_width_B = self.B_width + FEMALE * 2
            top_length = math.sqrt(
                ((total_width_A - total_width_B) / 2) ** 2
                + ((self.length - 2 * EXTENSION) ** 2)
            )
            top_main_area = (1 / 2) * (self.A_width + self.B_width) * top_length
            extension_area = EXTENSION * (self.A_width + self.B_width)
            side_length = math.sqrt(
                (((total_width_A - total_width_B) / 2) ** 2) + ((top_length) ** 2)
            )
            wings_area = 2 * FEMALE * side_length
            area = (top_main_area + extension_area + wings_area) * AREA_DEMULTIPLICATOR
            return round(area, 3)

        elif self.model in [2, 3]:
            total_width_A = self.A_width + FEMALE
            total_width_B = self.B_width + FEMALE
            top_side_length = math.sqrt(
                (total_width_A - total_width_B) ** 2
                + (self.length - 2 * EXTENSION) ** 2
            )
            top_main_area = (1 / 2) * ((total_width_A + total_width_B) * self.length)
            wing_area = top_side_length * FEMALE
            area = (top_main_area + wing_area) * AREA_DEMULTIPLICATOR
            return round(area, 3)

    def area_bottom(self):
        if self.model in [1, 6]:
            return self.area_top()
        elif self.model in [2, 3]:
            bottom_length = (
                math.sqrt(
                    ((self.A_width - self.B_width) ** 2)
                    + (self.length - 2 * EXTENSION) ** 2
                )
                + 2 * EXTENSION
            )
            bottom_side_length = math.sqrt(
                ((self.A_width - self.B_width) ** 2)
                + (bottom_length - 2 * EXTENSION) ** 2
            )
            bottom_main_area = (1 / 2) * ((self.A_width + self.B_width) * bottom_length)
            bottom_wing_1 = bottom_length * FEMALE
            bottom_wing_2 = bottom_side_length * FEMALE
            area = bottom_main_area + bottom_wing_1 + bottom_wing_2
            area = area * AREA_DEMULTIPLICATOR
            return round(area, 3)

    def area_left_side(self):
        if self.model in [1, 6]:
            total_height_A = self.A_height + 2 * MALE
            total_height_B = self.B_height + 2 * MALE
            left_length = math.sqrt(
                ((total_height_A - total_height_B) / 2) ** 2
                + (self.length - (EXTENSION * 2)) ** 2
            )
            left_main_area = (1 / 2) * ((total_height_A + total_height_B) * left_length)
            extension_area = EXTENSION * (total_height_A + total_height_B)
            area = (left_main_area + extension_area) * AREA_DEMULTIPLICATOR
            return round(area, 3)

        elif self.model in [2, 3]:
            total_height_A = self.A_height + 2 * MALE
            total_height_B = self.B_height + 2 * MALE
            total_left_length = math.sqrt(
                ((self.A_height - self.B_height) ** 2)
                + ((self.length - (2 * EXTENSION)) ** 2)
            )
            total_left_length = total_left_length + (2 * EXTENSION)
            area = (1 / 2) * ((total_height_A + total_height_B) * total_left_length)
            area = area * (AREA_DEMULTIPLICATOR)
            return round(area, 3)

    def area_right_side(self):
        if self.model in [1, 6]:
            return self.area_left_side()
        elif self.model in [2, 3]:
            total_A_height = self.A_height + 2 * MALE
            total_B_height = self.B_height + 2 * MALE

            area = (1 / 2) * ((total_A_height + total_B_height) * self.length)
            area = area * AREA_DEMULTIPLICATOR
            return round(area, 3)

    def area(self):
        if self.model in [1, 2, 3]:
            return round(
                self.area_top()
                + self.area_bottom()
                + self.area_left_side()
                + self.area_right_side(),
                2,
            )
        elif self.model in [3, 4]:
            red = RectangularReduction(
                self.A_width,
                self.A_height,
                self.B_width,
                self.B_height,
                self.length,
                self.quantity,
                model=1,
            )
            area1 = red.area()
            red2 = RectangularReduction(
                self.A_width,
                self.A_height,
                self.B_width,
                self.B_height,
                self.length,
                self.quantity,
                model=2,
            )
            area2 = red2.area()

            return round(((area1 + area2) / 2), 2)

    def true_area(self):
        return round(self.area() + (0.1 * self.area()), 2)

    def total_area(self):
        return self.area() * self.quantity

    def total_true_area(self):
        return self.true_area() * self.quantity

    def flange(self):
        flange = (
            (self.A_width + self.A_height + self.B_width + self.B_height)
            * 2
            * LENGTH_DEMULTIPLICATOR
        )
        return round(flange, 2)

    def total_flange(self):
        return round((self.flange() * self.quantity), 2)

    def corners(self):
        return 8

    def total_corners(self):
        return self.corners() * self.quantity


class RectangularT_piece(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.A_width = self.ch_A()
        self.B_width = self.ch_B()
        self.C_width = self.ch_C()
        self.height = self.ch_D()
        self.radius = self.ch_E() or 110
        self.quantity = self.quantity()

    def item_name(self):
        return self.name

    def item_characteristics(self):
        return f"{int(self.A_width)}x{int(self.height)}-{int(self.B_width)}x{int(self.height)}-{int(self.C_width)}x{int(self.height)} R{(int(self.radius))}"

    def characteristics(self):
        return [
            self.A_width,
            self.height,
            self.B_width,
            self.height,
            self.C_width,
            self.height,
            self.radius,
        ]

    def item_complete_name(self):
        return f"{self.item_name()} {self.item_characteristics()}"

    def label_field_A(self):
        return f"{int(self.A_width)}x{int(self.height)}"

    def label_field_B(self):
        return f"{int(self.B_width)}x{int(self.height)}"

    def label_field_C(self):
        return f"{int(self.C_width)}x{int(self.height)}"

    def item_thickness(self):
        item_lat = [self.A_width, self.B_width, self.C_width, self.height]
        return self.rectangular_thickness(item_lat)

    def top_area(self):
        true_length = (self.radius + EXTENSION) * 2 + self.B_width
        main_area = true_length * (self.A_width + 2 * MALE)
        second_area = (1 / 2) * (
            ((true_length - 2 * EXTENSION + 2 * MALE) + self.B_width)
            * (self.radius - MALE)
        )
        area = (
            main_area + second_area + EXTENSION * (self.B_width + 2 * MALE)
        ) * AREA_DEMULTIPLICATOR
        return round(area, 3)

    def back_area(self):
        true_length = (self.radius + EXTENSION) * 2 + self.B_width

        area = true_length * (self.height + 2 * FEMALE) * AREA_DEMULTIPLICATOR

        return round(area, 3)

    def small_parts_area(self):
        true_length = math.sqrt(2 * (self.radius**2))
        area = (
            (true_length + 2 * EXTENSION)
            * (self.height + 2 * FEMALE)
            * AREA_DEMULTIPLICATOR
        ) * 2
        return round(area, 3)

    def area(self):
        return round(
            self.top_area() * 2 + self.back_area() + self.small_parts_area(), 2
        )

    def total_area(self):
        return round(self.area() * self.quantity, 2)

    def true_area(self):
        return round(self.area() + (0.1 * self.area()), 3)

    def total_true_area(self):
        return self.true_area() * self.quantity

    def flange(self):
        flange = (
            2 * ((self.A_width + self.B_width + self.C_width) - 3 * FLANGE_CUT)
            + 6 * (self.height - FLANGE_CUT)
        ) * LENGTH_DEMULTIPLICATOR
        return round(flange, 2)

    def total_flange(self):
        return round((self.flange() * self.quantity), 2)

    def corners(self):
        return 12

    def total_corners(self):
        return self.corners() * self.quantity


class RectangularEnd_cap(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.width = self.ch_A()
        self.height = self.ch_B()
        self.lenght = self.ch_C() or 40
        self.quantity = self.quantity()

    def item_name(self):
        return self.name

    def item_characteristics(self):
        return f"{int(self.width)}x{int(self.height)} L{int(self.lenght)}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.item_characteristics()} "

    def characteristics(self):
        return [self.width, self.height, self.lenght]

    def label_field_A(self):
        return f"{int(self.width)}x{int(self.height)}"

    def label_field_B(self):
        return False

    def label_field_C(self):
        return False

    def item_thickness(self):
        item_lat = [self.width, self.height]
        return self.rectangular_thickness(item_lat)

    def area(self):
        cap_area = (self.width + 2 * EXTENSION) * (self.height + 2 * EXTENSION)
        area = cap_area * (AREA_DEMULTIPLICATOR)
        return round(area, 2)

    def total_area(self):
        return self.area() * self.quantity

    def true_area(self):
        return round(self.area() + (0.1 * self.area()), 2)

    def total_true_area(self):
        return self.true_area() * self.quantity

    def flange(self):
        flange = (self.width + self.height) * 2 * (LENGTH_DEMULTIPLICATOR)
        return round(flange, 2)

    def total_flange(self):
        return round((self.flange() * self.quantity), 2)

    def corners(self):
        return 4

    def total_corners(self):
        return self.corners() * self.quantity


class Rect_to_round(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.width = self.ch_A()
        self.height = self.ch_B()
        self.diameter = self.ch_C()
        self.lenght = self.ch_D()
        self.model = self.ch_E() or 1
        self.quantity = self.quantity()

    def item_name(self):
        return self.name

    def item_characteristics(self):
        return f"{int(self.width)}x{int(self.height)} D{int(self.diameter)} L{int(self.lenght)} model:{self.model}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.item_characteristics()}"

    def characteristics(self):
        return [self.width, self.height, self.diameter, self.lenght, self.model]

    def label_field_A(self):
        return f"{int(self.width)}x{int(self.height)}"

    def label_field_B(self):
        return f" D{int(self.diameter)}"

    def label_field_C(self):
        return f"L{int(self.lenght)} model:{self.model}"

    def item_thickness(self):
        item_lat = [self.width, self.height, self.diameter]
        return self.rectangular_thickness(item_lat)

    def body_area(self):
        true_length_width = math.sqrt(
            ((self.length - EXTENSION) ** 2) + (((self.width - self.diameter) / 2) ** 2)
        )
        true_length_height = math.sqrt(
            ((self.length - EXTENSION) ** 2)
            + (((self.height - self.diameter) / 2) ** 2)
        )

        first_area = ((self.width / 2) * true_length_width) / 2
        second_area = ((self.height / 2) * true_length_height) / 2
        triangle_length_1 = math.sqrt((true_length_height) ** 2 + (self.width / 2) ** 2)
        triangle_length_2 = math.sqrt((true_length_width) ** 2 + (self.height / 2) ** 2)
        arc_length = PI * self.diameter / 4
        triangle_height = math.sqrt((triangle_length_1**2) - (0.5 * arc_length) ** 2)
        third_area = (arc_length * triangle_height) / 2
        extension_area = 0.5 * (self.width + self.height) * EXTENSION
        wing_area = triangle_length_2 * 20
        area = first_area + second_area + third_area + extension_area + wing_area
        area = area * AREA_DEMULTIPLICATOR

        return 4 * round(area, 2)

    def connector_area(self):
        return round(self.diameter * PI * RACORD_LENGHT, 2)

    def area(self):
        return round(self.body_area() + self.connector_area(), 2)

    def total_area(self):
        return round(self.area() * self.quantity(), 2)

    def true_area(self):
        return round(self.area() + (0.1 * self.area()), 2)

    def total_true_area(self):
        return self.true_area() * self.quantity

    def flange(self):
        flange = (
            ((self.width + self.height) - 2 * FLANGE_CUT) * 2 * (LENGTH_DEMULTIPLICATOR)
        )
        return round(flange, 2)

    def total_flange(self):
        return round((self.flange() * self.quantity), 2)

    def corners(self):
        return 8

    def total_corners(self):
        return self.corners() * self.quantity


class RectangularShoe(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.width = self.ch_A()
        self.lenght = self.ch_B()
        self.height = self.ch_C()
        self.quantity = self.quantity()

    def item_name(self):
        return self.name

    def item_characteristics(self):
        return f"{int(self.width)}x{int(self.length)} L{int(self.height)}"

    def characteristics(self):
        return [self.width, self.length, self.height]

    def item_complete_name(self):
        return f"{self.item_name()} {self.item_characteristics()}"

    def label_field_A(self):
        return f"{int(self.width)}x{int(self.length)}"

    def label_field_B(self):
        return f"L{int(self.height)}"

    def label_field_C(self):
        return False

    def item_thickness(self):
        item_lat = [self.width, self.lenght]
        return self.rectangular_thickness(item_lat)

    def area(self):
        area = ((self.length + self.width) * 2 + WELDING_LENGTH * 2) * (
            self.height + WELDING_LENGTH * 2
        )
        area = area * AREA_DEMULTIPLICATOR
        return round(area, 3)

    def total_area(self):
        return self.area() * self.quantity

    def true_area(self):
        return round(self.area() + (0.1 * self.area()), 2)

    def total_true_area(self):
        return self.true_area() * self.quantity

    def flange(self):
        flange = (self.width + self.height) * 2 * (LENGTH_DEMULTIPLICATOR)
        return round(flange, 2)

    def total_flange(self):
        return round((self.flange() * self.quantity), 2)

    def corners(self):
        return 8

    def total_corners(self):
        return self.corners() * self.quantity


class RectangularPlenum_box:
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.lenght = self.ch_A()
        self.width = self.ch_B()
        self.height = self.ch_C()
        self.diameter = self.ch_D()
        self.quantity = self.quantity()

    def item_name(self):
        return self.name

    def item_characteristics(self):
        return f"{int(self.width)}x{int(self.length)} L{int(self.height)} D{int(self.diameter)}"

    def characteristics(self):
        return [self.width, self.length, self.height, self.diameter]

    def item_complete_name(self):
        return f"{self.item_name()} {self.item_characteristics()}"

    def label_field_A(self):
        return f"{int(self.width)}x{int(self.length)}"

    def label_field_B(self):
        return f"L{int(self.height)}"

    def label_field_C(self):
        return f"D{int(self.diameter)}"

    def item_thickness(self):
        item_lat = [self.width, self.lenght]
        return self.rectangular_thickness(item_lat)

    def top_area(self):
        area = (self.length + 2 * WELDING_LENGTH) * (self.width + 2 * WELDING_LENGTH)
        area = area * AREA_DEMULTIPLICATOR
        return round(area, 3)

    def lateral_area(self):
        area = self.height * (2 * (self.length + self.width) + 20)
        area = area * AREA_DEMULTIPLICATOR
        return round(area, 3)

    def connector_area(self):
        return round(self.diameter * PI * RACORD_LENGHT, 2)

    def area(self):
        return self.top_area() + self.lateral_area() + self.connector_area()

    def total_area(self):
        return self.area() * self.quantity

    def true_area(self):
        return round(self.area() + (0.1 * self.area()), 2)

    def total_true_area(self):
        return self.true_area() * self.quantity


class RectangularOffset:
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.width = self.ch_A()
        self.height = self.ch_B()
        self.lenght = self.ch_C()
        self.eccentricity = self.ch_E()
        self.quantity = self.quantity()

    def item_name(self):
        return self.name

    def item_characteristics(self):
        return f"{int(self.width)}x{int(self.height)} L{int(self.lenght)} E{int(self.eccentricity)}"

    def characteristics(self):
        return [self.width, self.height, self.lenght, self.eccentricity]

    def item_complete_name(self):
        return f"{self.item_name()} {self.item_characteristics()}"

    def label_field_A(self):
        return f"{int(self.width)}x{int(self.height)}"

    def label_field_B(self):
        return f"L{int(self.lenght)}"

    def label_field_C(self):
        return f"E{int(self.eccentricity)}"

    def item_thickness(self):
        item_lat = [self.width, self.height]
        return self.rectangular_thickness(item_lat)

    def area(self):
        return round(2 * (self.width + self.height) * (self.length + self.eccentricity))

    def total_area(self):
        return self.area() * self.quantity

    def flange(self):
        flange = (self.width + self.height) * 2 * (LENGTH_DEMULTIPLICATOR)
        return round(flange, 2)

    def total_flange(self):
        return round((self.flange() * self.quantity), 2)

    def corners(self):
        return 8

    def total_corners(self):
        return self.corners() * self.quantity
