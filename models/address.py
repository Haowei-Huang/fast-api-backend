from pydantic import BaseModel, Field, ConfigDict


class Address(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, validate_by_alias=True, validate_by_name=True
    )

    street: str = Field(..., max_length=100)
    city: str = Field(..., pattern="^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$", max_length=30)
    province: str = Field(
        ..., pattern="^(?:AB|BC|MB|N[BLTSU]|ON|PE|QC|SK|YT){1}$"
    )  # canadian provinces
    postal_code: str = Field(
        ...,
        alias="postalCode",
        pattern="^([ABCEGHJKLMNPRSTVXY][0-9][A-Z](?: [0-9][A-Z][0-9])?)$",
        max_length=7,
    )
    country: str = Field(..., pattern="^[A-Za-z\s.-]+$", max_length=50)
