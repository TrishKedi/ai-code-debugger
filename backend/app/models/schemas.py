from pydantic import BaseModel

class CodeInput(BaseModel):
    code: str

class CodeAnalysisResult(BaseModel):
    status: str
    syntax_errors: str | None = None
    llm_fixes: str | None = None
    documentation: str | None = None
