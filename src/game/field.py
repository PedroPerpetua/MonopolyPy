from lib.assets import Assets, Colors

# Colors in RGB

def import_fields(file):
    fields = []
    with open(file, "r") as in_file:
        for line in in_file:
            if line[0] == "#":
                pass
            else:
                args = line[:-1].split("|")
                if args[0] == "P":
                    taxes = []
                    for number in args[5].split(","):
                        taxes.append(int(number))
                    fields.append(PropertyField(args[1], int(args[2]), Colors.get_color(args[3]), args[4], taxes))
                elif args[0] == "W":
                    fields.append(WildcardField(args[1]))
                elif args[0] == "T":
                    fields.append(TaxField(args[1], args[2]))
                elif args[0] == "R":
                    fields.append(RailroadField(args[1]))
                elif args[0] == "U":
                    fields.append(UtilityField(args[1]))
                elif args[0] == "C0":
                    fields.append(StartCorner())
                elif args[0] == "C1":
                    fields.append(JailCorner())
                elif args[0] == "C2":
                    fields.append(FreeParkingCorner())
                elif args[0] == "C3":
                    fields.append(GoToJailCorner())
        return fields


class Field():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)
    @staticmethod
    def deserializeField(info):
        tag = info["tag"]
        if tag == "property":
            return PropertyField.deserialize(info)
        if tag == "utility":
            return UtilityField.deserialize(info)
        if tag == "railroad":
            return RailroadField.deserialize(info)
        if tag == "tax":
            return TaxField.deserialize(info)
        if tag == "wildcard":
            return WildcardField.deserialize(info)
        if tag == "C0":
            return StartCorner.deserialize(info)
        if tag == "C1":
            return JailCorner.deserialize(info)
        if tag == "C2":
            return FreeParkingCorner.deserialize(info)
        if tag == "C3":
            return GoToJailCorner.deserialize(info)
        return None

class BuyableField(Field):
    def __init__(self, name, price):
        super().__init__(name)
        self.price = price
        self.owner_id = None
    
class PropertyField(BuyableField):
    def __init__(self, name, price, color, house_price, house_taxes):
        super().__init__(name, price)
        self.color = color
        self.house_price = house_price
        self.house_taxes = house_taxes
        self.houses = 0
        self.mortaged = False
    
    def get_fieldInfo(self):
        info = {}
        info["type"] = "property"
        info["color"] = self.color
        info["houses"] = self.houses
        info["mortaged"] = self.mortaged
        return info
    def get_tooltipInfo(self):
        info = {}
        info["type"] = "property"
        info["name"] = self.name
        info["color"] = self.color
        return info
    def do_action(self, player):
        pass
    def serialize(self):
        info = {}
        info["tag"] = "property"
        info["name"] = self.name
        info["price"] = self.price
        info["owner_id"] = self.owner_id
        info["color"] = self.color
        info["house_price"] = self.house_price
        info["house_taxes"] = self.house_taxes
        info["houses"] = self.houses
        info["mortaged"] = self.mortaged
        return info
    @staticmethod
    def deserialize(info):
        field = PropertyField(info["name"], info["price"], info["color"], info["house_price"], info["house_taxes"])
        field.owner_id = info["owner_id"]
        field.houses = info["houses"]
        field.mortaged = info["mortaged"]
        return field

class UtilityField(BuyableField):
    def __init__(self, name):
        super().__init__(name, 150)
    def get_fieldInfo(self):
        info = {}
        info["type"] = "icon"
        if self.name == "Electricity Company":
            info["image"] = Assets.COMPANY_ELECTRICITY
        elif self.name == "Water Company":
            info["image"] = Assets.COMPANY_WATER
        info["color"] = Colors.LIGHT_CYAN
        return info
    def get_tooltipInfo(self):
        info = {}
        info["type"] = "simple"
        info["name"] = self.name
        info["color"] = Colors.LIGHT_CYAN
        return info
    def do_action(self, player):
        pass
    def serialize(self):
        info = {}
        info["tag"] = "utility"
        info["name"] = self.name
        info["owner_id"] = self.owner_id
        return info
    @staticmethod
    def deserialize(info):
        field = UtilityField(info["name"])
        field.owner_id = info["owner_id"]
        return field

class RailroadField(BuyableField):
    def __init__(self, name):
        super().__init__(name, 200)
    def get_fieldInfo(self):
        info = {}
        info["type"] = "icon"
        info["image"] = Assets.TRAIN
        info["color"] = Colors.LIGHT_GRAY
        return info
    def get_tooltipInfo(self):
        info = {}
        info["type"] = "simple"
        info["name"] = self.name
        info["color"] = Colors.LIGHT_GRAY
        return info
    def do_action(self, player):
        pass
    def serialize(self):
        info = {}
        info["tag"] = "railroad"
        info["name"] = self.name
        info["owner_id"] = self.owner_id
        return info
    @staticmethod
    def deserialize(info):
        field = RailroadField(info["name"])
        field.owner_id = info["owner_id"]
        return field

class WildcardField(Field):
    def get_fieldInfo(self):
        info = {}
        info["type"] = "icon"
        if self.name == "Luck":
            info["image"] = Assets.LUCK
        elif self.name == "Community Chest":
            info["image"] = Assets.COMMUNITY_CHEST
        info["color"] = Colors.WHITE
        return info
    def get_tooltipInfo(self):
        info = self.get_fieldInfo()
        info["type"] = "wildcard"
        info["name"] = self.name
        return info
    def do_action(self, player):
        pass
    def serialize(self):
        return {"tag": "wildcard", "name": self.name}
    @staticmethod
    def deserialize(info):
        return WildcardField(info["name"])

class TaxField(Field):
    def __init__(self, name, tax):
        super().__init__(name)
        self.tax = tax
    def get_fieldInfo(self):
        info = {}
        info["type"] = "icon"
        if self.name == "Income Tax":
            info["image"] = Assets.TAX_INCOME
        elif self.name == "Luxury Tax":
            info["image"] = Assets.TAX_LUXURY
        info["color"] = Colors.WHITE
        return info
    def get_tooltipInfo(self):
        info = {}
        info["type"] = "label"
        info["name"] = self.name
        info["color"] = Colors.WHITE
        info["label"] = f"Pay {self.tax}€"
        return info
    def do_action(self):
        pass
    def serialize(self):
        info = {}
        info["tag"] = "tax"
        info["name"] = self.name
        info["tax"] = self.tax
        return info
    @staticmethod
    def deserialize(info):
        return TaxField(info["name"], info["tax"])        

class StartCorner(Field):
    def __init__(self):
        super().__init__("Start!")
    def get_fieldInfo(self):
        info = {}
        info["type"] = "corner"
        info["image"] = Assets.CORNER_START
        info["color"] = Colors.WHITE
        info["jail"] = False
        return info
    def get_tooltipInfo(self):
        info = {}
        info["type"] = "label"
        info["name"] = self.name
        info["color"] = Colors.WHITE
        info["label"] = "You get 200€ whenever you pass here!"
        return info
    def do_action(self, player):
        pass
    def serialize(self):
        return {"tag": "C0"}
    @staticmethod
    def deserialize(_):
        return StartCorner()

class JailCorner(Field):
    def __init__(self):
        super().__init__("Jail!")
    def get_fieldInfo(self):
        info = {}
        info["type"] = "corner"
        info["image"] = Assets.CORNER_JAIL
        info["color"] = Colors.WHITE
        info["jail"] = True
        return info
    def get_tooltipInfo(self):
        info = {}
        info["type"] = "label"
        info["name"] = self.name
        info["color"] = Colors.WHITE
        info["label"] = "You're jailed! (Or just visiting...)"
        return info
    def do_action(self, player):
        pass
    def serialize(self):
        return {"tag": "C1"}
    @staticmethod
    def deserialize(_):
        return JailCorner()

class FreeParkingCorner(Field):
    def __init__(self):
        super().__init__("Free Parking!")
        self.value = 0
    def get_fieldInfo(self):
        info = {}
        info["type"] = "corner"
        info["image"] = Assets.CORNER_FREEPARKING
        info["color"] = Colors.WHITE
        info["jail"] = False
        return info
    def get_tooltipInfo(self):
        info = {}
        info["type"] = "label"
        info["name"] = self.name
        info["color"] = Colors.WHITE
        info["label"] = f"Free Money! {self.value}€ so far..."
        return info
    def do_action(self, player):
        pass
    def serialize(self):
        return {"tag": "C2", "value": self.value}
    @staticmethod
    def deserialize(info):
        field = FreeParkingCorner()
        field.value = info["value"]
        return field

class GoToJailCorner(Field):
    def __init__(self):
        super().__init__("Go to Jail!")
    def get_fieldInfo(self):
        info = {}
        info["type"] = "corner"
        info["image"] = Assets.CORNER_GOTOJAIL
        info["color"] = Colors.WHITE
        info["jail"] = False
        return info
    def get_tooltipInfo(self):
        info = {}
        info["type"] = "label"
        info["name"] = self.name
        info["color"] = Colors.WHITE
        info["label"] = "Stop right there criminal scum!"
        return info
    def do_action(self, player):
        pass
    def serialize(self):
        return {"tag": "C3"}
    @staticmethod
    def deserialize(_):
        return GoToJailCorner()