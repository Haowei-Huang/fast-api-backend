from pydantic import BaseModel, Field


class Address(BaseModel):
    street: str
    city: str = Field(..., pattern="^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$")
    province: str = Field(
        ..., pattern="^(?:AB|BC|MB|N[BLTSU]|ON|PE|QC|SK|YT){1}$"
    )  # canadian provinces
    postal_code: str = Field(
        ...,
        alias="postalCode",
        pattern="^([ABCEGHJKLMNPRSTVXY][0-9][A-Z](?: [0-9][A-Z][0-9])?)$",
    )
    country: str = Field(..., pattern="^^[A-Za-z\s.-]+$")
