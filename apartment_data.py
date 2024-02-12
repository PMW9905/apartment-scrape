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

    def get_formatted_string_for_discord_table(self):
        return f'{self.unit_number:<6} | {self.layout_name:<15} | {self.cost:<8} | {self.square_footage:<6} | {self.availability:<8}'
