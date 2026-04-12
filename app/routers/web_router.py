from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict

from .dependencies import MessageServiceDep

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


class MessageSchema(BaseModel):
    id: int
    content: str

    model_config = ConfigDict(from_attributes=True)


class MessageCreateSchema(BaseModel):
    content: str


@router.get("/web/messages", response_class=HTMLResponse)
async def get_messages_page(request: Request, service: MessageServiceDep):
    messages = await service.get_all_messages()
    messages = messages if messages else []
    print(messages)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"messages": messages}
    )


@router.get("/web/messages/create", response_class=HTMLResponse)
async def get_create_message_page(request: Request):
    return templates.TemplateResponse(request=request, name="create.html")


@router.post("/web/messages", response_class=HTMLResponse)
async def create_message_form(
    request: Request,
    service: MessageServiceDep,
    content: str = Form(...),
):
    await service.create_message(content)
    messages = await service.get_all_messages()

    return templates.TemplateResponse(
        request=request, name="index.html", context={"messages": messages}
    )


@router.get("/web/messages/{message_id}", response_class=HTMLResponse)
async def get_message_detail_page(
    request: Request,
    service: MessageServiceDep,
    message_id: int,
):
    message = await service.get_message_or_404(message_id=message_id)
    return templates.TemplateResponse(
        request=request, name="detail.html", context={"message": message}
    )
