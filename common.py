from pydantic import BaseModel, ConfigDict

model_config = ConfigDict(validate_assignment=True,
                          arbitrary_types_allowed=True,
                          use_enum_values=True)


class NablaModel(BaseModel):
    model_config = model_config