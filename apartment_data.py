from dataclasses import dataclass

@dataclass
class ApartmentData:
    unit_number: str
    layout_name: str
    cost: str
    square_footage: str
    availability: str

    def print_all_data(self):
        print(f'{self.unit_number} | {self.layout_name} | {self.cost} | {self.square_footage} | {self.availability}')
