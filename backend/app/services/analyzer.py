import ast

def analyse_code(code: str):

    try:
        ast.parse(code)
        return {"status": "valid"}
    except Exception as e:
        return {
            "status": "error",
            "syntax_errors": str(e)
        }


