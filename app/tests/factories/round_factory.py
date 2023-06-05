from factory import Factory, Faker
from src.models.round_model import RoundModel


class RoundFactory(Factory):
    class Meta:
        model = RoundModel

    name = Faker("name")
    cards_type = Faker("word")
