import pathlib
from pydantic import BaseModel, ConfigDict

model_config = ConfigDict(validate_assignment=True,
                          arbitrary_types_allowed=True,
                          use_enum_values=True)


user_data_path = pathlib.Path(__file__).parent.resolve() / "user_data.json"

class NablaModel(BaseModel):
    model_config = model_config