from pydantic import BaseModel, Field


class CreateGenReadmeResponse(BaseModel):
    token: str = Field(...)
