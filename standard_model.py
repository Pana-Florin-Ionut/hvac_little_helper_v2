from offer_object import Object
import working_databases as database


class Mdl(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()

    def item_thickness(self):
        item_lat = []
        return self.circular_thickness(item_lat)

    def item_name(self):
        return {self.name}

    def name_characteristics(self):
        return f"D"

    def item_complete_name(self):
        return f"{self.item_name()} {self.name_characteristics()}"

    def label_field_A(self):
        return f"D: {int(self.diameter)}"

    def label_field_B(self):
        return f""

    def label_field_C(self):
        return f""

    def characteristics(self):
        return []

    def item_dimensions(self):
        return [i for i in self.dimensions() if i]


class RoundElbow(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.diameter = self.ch_A()
        self.angle = self.ch_B()
        self.radius = self.ch_C() or self.diameter
        self.quantity = self.quantity()

    def item_thickness(self):
        item_lat = [self.diameter]
        return self.circular_thickness(item_lat)

    def item_name(self):
        return self.name

    def name_characteristics(self):
        return (
            f"D{int(self.diameter)} {int(self.angle)}degree  Radius={int(self.radius)}"
        )

    def item_complete_name(self):
        return f"{self.item_name()} {self.name_characteristics()}"

    def label_field_A(self):
        return f"D: {int(self.diameter)}"

    def label_field_B(self):
        return f"Deg: {int(self.angle)}"

    def label_field_C(self):
        return f"R: {int(self.radius)}"

    def characteristics(self):
        return [int(self.diameter), int(self.angle), int(self.radius)]

    def item_dimensions(self):
        dims = [i for i in self.dimensions() if i]
        if len(dims) < 3:
            dims.append(self.radius)
        return dims


class RoundStraight(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.diameter = self.ch_A()
        self.lenght = self.ch_B()
        self.quantity = self.quantity()

    def item_thickness(self):
        item_lat = [self.diameter]
        return self.circular_thickness(item_lat)

    def item_name(self):
        return self.name

    def name_characteristics(self):
        return f"D{int(self.diameter)} L{int(self.lenght)}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.name_characteristics()}"

    def label_field_A(self):
        return f"D: {int(self.diameter)}"

    def label_field_B(self):
        return f"L: {int(self.lenght)}"

    def label_field_C(self):
        return f""

    def characteristics(self):
        return [int(self.diameter), int(self.lenght)]

    def item_dimensions(self):
        return [i for i in self.dimensions() if i]


class RoundReduction(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.entry_dim = self.ch_A()
        self.exit_dim = self.ch_B()
        self.lenght = self.ch_C() or 80
        self.quantity = self.quantity()

    def item_thickness(self):
        item_lat = [self.entry_dim, self.exit_dim]
        return self.circular_thickness(item_lat)

    def item_name(self):
        return self.name

    def name_characteristics(self):
        return f"D{int(self.entry_dim)}-D{int(self.exit_dim)} L{int(self.lenght)}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.name_characteristics()}"

    def label_field_A(self):
        return f"D1: {int(self.entry_dim)}"

    def label_field_B(self):
        return f"D2: {int(self.exit_dim)}"

    def label_field_C(self):
        return f"L: {int(self.lenght)}"

    def characteristics(self):
        return [self.entry_dim, self.entry_dim, self.lenght]

    def item_dimensions(self):
        return [i for i in self.dimensions() if i]


class RoundT_piece(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.pipe_diam_1 = self.ch_A()
        self.branch_diam = self.ch_B() or self.pipe_diam_1
        self.pipe_diam_2 = self.ch_C() or self.pipe_diam_1
        self.pipe_lenght = self.ch_D() or self.branch_diam + 2 * 80
        self.branch_lenght = self.ch_E() or 80
        self.quantity = self.quantity()

    def item_thickness(self):
        item_lat = [self.pipe_diam_1, self.branch_diam, self.pipe_diam_2]
        return self.circular_thickness(item_lat)

    def item_name(self):
        return self.name

    def name_characteristics(self):
        return f"D1: {self.pipe_diam_1} D2: {self.branch_diam} D3: {self.pipe_diam_2}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.name_characteristics()}"

    def label_field_A(self):
        return f"D1: {int(self.pipe_diam_1)}"

    def label_field_B(self):
        return f"D2: {int(self.branch_diam)}"

    def label_field_C(self):
        return f"D3: {int(self.pipe_diam_2)}"

    def characteristics(self):
        return [
            self.pipe_diam_1,
            self.branch_diam,
            self.pipe_diam_2,
            self.pipe_lenght,
            self.branch_lenght,
        ]

    def item_dimensions(self):
        return [i for i in self.dimensions() if i]


class RoundEnd_cap(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.diameter = self.ch_A()
        self.lenght = self.ch_B() or 60
        self.quantity = self.quantity()

    def item_thickness(self):
        item_lat = [self.diameter]
        return self.circular_thickness(item_lat)

    def item_name(self):
        return self.name

    def name_characteristics(self):
        return f"D {self.diameter}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.name_characteristics()}"

    def label_field_A(self):
        return f"D: {int(self.diameter)}"

    def label_field_B(self):
        return f""

    def label_field_C(self):
        return f""

    def characteristics(self):
        return [self.diameter, self.lenght]

    def item_dimensions(self):
        return [i for i in self.dimensions() if i]


class RoundCoupling(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.diameter = self.ch_A()
        self.lenght = self.ch_B() or 70
        self.quantity = self.quantity()

    def item_thickness(self):
        item_lat = [self.diameter]
        return self.circular_thickness(item_lat)

    def item_name(self):
        return self.name

    def name_characteristics(self):
        return f"D {self.diameter}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.name_characteristics()}"

    def label_field_A(self):
        return f"D: {int(self.diameter)}"

    def label_field_B(self):
        return f""

    def label_field_C(self):
        return f""

    def characteristics(self):
        return [self.diameter, self.lenght]

    def item_dimensions(self):
        return [i for i in self.dimensions() if i]


class RoundSaddle(Object):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = self.name()
        self.pipe_dim = self.ch_A()
        self.branch_dim = self.ch_B()
        self.lenght = self.ch_C() or 80
        self.quantity = self.quantity()

    def item_thickness(self):
        item_lat = [self.pipe_dim, self.branch_dim]
        return self.circular_thickness(item_lat)

    def item_name(self):
        return self.name

    def name_characteristics(self):
        return f"D{int(self.pipe_dim)}-D{int(self.branch_dim)} L{int(self.lenght)}"

    def item_complete_name(self):
        return f"{self.item_name()} {self.name_characteristics()}"

    def label_field_A(self):
        return f"D1: {int(self.pipe_dim)}"

    def label_field_B(self):
        return f"D2: {int(self.batch_dim)}"

    def label_field_C(self):
        return f"L: {int(self.lenght)}"

    def characteristics(self):
        return [self.pipe_dim, self.branch_dim, self.lenght]

    def item_dimensions(self):
        return [i for i in self.dimensions() if i]


# item2 = RoundElbow(database.read_row("helo", "id", 2))
# print(item2.item_name())
# print(item2.item_dimensions())
