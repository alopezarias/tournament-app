from pydantic import BaseModel

class InvitationBase(BaseModel):
    team_id: int
    inviter_id: int
    invitee_id: int

class InvitationCreate(InvitationBase):
    pass

class InvitationOut(InvitationBase):
    id: int
    status: str  # 'pending', 'accepted', 'rejected'

    class Config:
        orm_mode = True

class InvitationRespond(BaseModel):
    response: str  # "accepted" o "rejected"
