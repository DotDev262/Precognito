from pydantic import BaseModel, Field

class PartReservationRequest(BaseModel):
    partId: int = Field(..., description="ID of the part to reserve")
    quantity: int = Field(default=1, gt=0, description="Quantity to reserve")
    workOrderId: int = Field(..., description="ID of the associated work order")

class PurchaseOrderRequest(BaseModel):
    partId: int = Field(..., description="ID of the part to order")
    quantity: int = Field(default=10, gt=0, description="Quantity to order")
