from fastapi import BackgroundTasks, APIRouter
from fastapi.concurrency import run_in_threadpool
from app.models.schemas import CodeAnalysisResult, CodeInput
from app.services.analyzer import analyse_code
from app.services.debugger import debug_code
router = APIRouter()

@router.post("/analyze", response_model=CodeAnalysisResult)
async def analyze_code_handler(payload: CodeInput):
    # analysis = analyse_code(payload.code)
    # if analysis["status"] == "error":
    #     return {
    #         "status": "error",
    #         "syntax_errors": analysis["syntax_errors"]
    #     }

    llm_result = await run_in_threadpool(debug_code, payload.code)

    return {
        "status": "success",
        "llm_fixes": llm_result["llm_output"],
        "documentation": llm_result["llm_output"]
    }
