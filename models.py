class OpenedBuyOrder():
    """
    Represents an opened buy order in the trading system.
    """
    def __init__(self, pc_number, cod, dt_solicitation, dt_delivery, buy_order_value, supplier, description):
        self.pc_number = pc_number
        self.cod = cod
        self.dt_solicitation = dt_solicitation
        self.dt_delivery = dt_delivery
        self.buy_order_value = buy_order_value
        self.supplier = supplier
        self.description = description

    def serialize(self):
        return {"pc_number": self.pc_number,
                "cod": self.cod,
                "dt_solicitation": self.dt_solicitation,
                "dt_delivery": self.dt_delivery,
                "buy_order_value": self.buy_order_value,
                "supplier": self.supplier,
                "description": self.description}