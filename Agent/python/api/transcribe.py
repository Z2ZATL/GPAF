from python.helpers.api import ApiHandler
from flask import Request, Response

from python.helpers import runtime, settings, whisper

class Transcribe(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        audio = input.get("audio")
        ctxid = input.get("ctxid", "")

        context = self.get_context(ctxid)
        if await whisper.is_downloading():
            context.log.log(type="info", content="Whisper model is currently being downloaded, please wait...")

        set = settings.get_settings()
        
        # จัดการกับ automatic selection สำหรับ STT model
        stt_model = set["stt_model_size"]
        if stt_model == "automatic":
            # เลือก model ตามภาษา
            if set["stt_language"] in ["en", "english"]:
                stt_model = "base"  # ใช้ base สำหรับภาษาอังกฤษ
            else:
                stt_model = "large"  # ใช้ large สำหรับภาษาอื่น ๆ
        
        result = await whisper.transcribe(stt_model, audio) # type: ignore
        return result
