class Object:
    def __init__(self, obj):
        self.obj = obj

    def item(self):
        return self.obj

    def values(self):
        self.values.append(iter(self.obj))

    def item_id(self):
        return self.obj[0]

    def project_id(self):
        return self.obj[1]

    def name(self):
        return self.obj[2]

    def ch_A(self):
        try:
            return int(self.obj[3])
        except ValueError:
            return self.obj[3]

    def ch_B(self):
        try:
            return int(self.obj[4])
        except ValueError:
            return self.obj[4]

    def ch_C(self):
        try:
            return int(self.obj[5])
        except ValueError:
            return self.obj[5]

    def ch_D(self):
        try:
            return int(self.obj[6])
        except ValueError:
            return self.obj[6]

    def ch_E(self):
        try:
            return int(self.obj[7])
        except ValueError:
            return self.obj[7]

    def ch_F(self):
        try:
            return int(self.obj[8])
        except ValueError:
            return self.obj[8]

    def characteristics(self):
        return [
            self.ch_A(),
            self.ch_B(),
            self.ch_C(),
            self.ch_D(),
            self.ch_E(),
            self.ch_F(),
        ]

    def dimensions(self):
        return [
            self.ch_A(),
            self.ch_B(),
            self.ch_C(),
            self.ch_D(),
            self.ch_E(),
            self.ch_F(),
        ]

    def um(self):
        return self.obj[9]

    def quantity(self):
        return self.obj[10] or float(self.obj[10])

    def category(self):
        return self.obj[11]

    def observations(self):
        return self.obj[12]

    def rectangular_thickness(self, list):
        max_item = max(list)
        if max_item <= 600:
            return 0.6
        elif max_item <= 1200:
            return 0.8
        elif max_item <= 1800:
            return 1.00
        return 1.2

    def circular_thickness(self, list):
        max_item = max(list)
        if max_item <= 316:
            return 0.6
        elif max_item <= 600:
            return 0.8
        elif max_item <= 800:
            return 1.00
        return 1.2

    # some refactoring
    # def thickness(self, list):
    #     return self._extracted_from_circular_thickness_2(list, 600, 1200, 1800)

    # def circular_thickness(self, list):
    #     return self._extracted_from_circular_thickness_2(list, 316, 600, 800)

    # # TODO Rename this here and in `thickness` and `circular_thickness`
    # def _extracted_from_circular_thickness_2(self, list, arg1, arg2, arg3):
    #     max_item = max(list)
    #     if max_item <= arg1:
    #         return 0.6
    #     elif max_item <= arg2:
    #         return 0.8
    #     elif max_item <= arg3:
    #         return 1.0
    #     return 1.2
