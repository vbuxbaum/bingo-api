from app.models.base_model import BaseModel
import pytest


def test_base_model_invalid_objectid():
    with pytest.raises(ValueError, match="Invalid objectid"):
        BaseModel(_id="None")


def test_modify_model_schema():
    assert BaseModel.schema()["properties"]["_id"]["type"] == "string"
