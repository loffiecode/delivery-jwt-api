from datetime import datetime
from pydantic import BaseModel, model_validator


from typing import Optional

class DeliveryBase(BaseModel):
    id: int
    
class DeliveryUpdate(BaseModel):
    Status: Optional[str] = None
    TargetTimeDelivery: Optional[datetime] = None

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> 'DeliveryUpdate':
        if self.Status is None and self.TargetTimeDelivery is None:
            raise ValueError(
                "A mandatory parametr skipped: TargetTimeDelivery or Status needed"
            )
        return self