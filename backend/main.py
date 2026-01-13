from __future__ import annotations

from typing import Any, Literal

from typing_extensions import TypedDict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

AnswerValue = Literal["yes", "no"]


class NextQuestion(TypedDict):
    type: Literal["question"]
    id: str


class NextResult(TypedDict):
    type: Literal["result"]
    id: Literal["A", "B", "C", "D", "E"]


class Option(TypedDict):
    label: str
    value: AnswerValue
    next: NextQuestion | NextResult


class Question(TypedDict):
    id: str
    title: str
    description: str | None
    bullets: list[str] | None
    options: list[Option]


class Result(TypedDict):
    id: Literal["A", "B", "C", "D", "E"]
    title: str
    description: str
    bullets: list[str] | None


QUESTIONS: dict[str, Question] = {
    "q1": {
        "id": "q1",
        "title": "问题1：您的产品是否是一个能够为达成某个目标，自行处理信息并做出预测、推荐或决策的计算机系统？",
        "description": "例如：自动化推荐、图像识别、决策辅助等。",
        "bullets": None,
        "options": [
            {"label": "是", "value": "yes", "next": {"type": "question", "id": "q2"}},
            {"label": "否", "value": "no", "next": {"type": "result", "id": "A"}},
        ],
    },
    "q2": {
        "id": "q2",
        "title": "问题2：您的AI系统是专门为军队、国防或国家安全目的而设计和使用吗？",
        "description": "例如：用于军事作战、国防情报分析等。",
        "bullets": None,
        "options": [
            {"label": "是", "value": "yes", "next": {"type": "result", "id": "B"}},
            {"label": "否", "value": "no", "next": {"type": "question", "id": "q3"}},
        ],
    },
    "q3": {
        "id": "q3",
        "title": "问题3：您的AI系统是纯粹为了科学研究和技术开发，尚未准备上市销售或提供给客户使用吗？",
        "description": "例如：大学实验室的研究原型。",
        "bullets": None,
        "options": [
            {"label": "是", "value": "yes", "next": {"type": "result", "id": "B"}},
            {"label": "否", "value": "no", "next": {"type": "question", "id": "q4"}},
        ],
    },
    "q4": {
        "id": "q4",
        "title": "问题4：您的AI系统是否用于以下任何一项被法律明确禁止的用途？",
        "description": None,
        "bullets": [
            "使用人眼无法察觉的“隐形广告”等技术，在用户不知情下操纵其行为并造成严重伤害。",
            "利用儿童、残障人士等群体的弱点，欺骗或操纵他们并造成严重伤害。",
            "由政府或商业机构对个人或群体进行“社会评分”，导致其在社会生活中受到不公平的歧视性待遇。",
            "仅凭计算机对个人的分析（画像），就预测或评估其犯罪风险（有例外，如用于辅助人类调查具体案件）。",
            "在公共场合使用摄像头实时远程识别特定个人（即“实时远程生物识别”，执法机关在严格限制下除外）。",
        ],
        "options": [
            {"label": "是", "value": "yes", "next": {"type": "result", "id": "C"}},
            {"label": "否", "value": "no", "next": {"type": "question", "id": "q5"}},
        ],
    },
    "q5": {
        "id": "q5",
        "title": "问题5：您的AI系统是以下产品的核心安全部件吗？或者它本身就是一个这样的产品？",
        "description": "并且，根据这些产品自身的法律，它们上市前必须经过官方指定的第三方机构检验合格。",
        "bullets": ["医疗器械（如AI诊断软件）", "汽车、飞机", "工业机械", "玩具", "电梯等"],
        "options": [
            {"label": "是", "value": "yes", "next": {"type": "result", "id": "D"}},
            {"label": "否", "value": "no", "next": {"type": "question", "id": "q6"}},
        ],
    },
    "q6": {
        "id": "q6",
        "title": "问题6：您的AI系统是否主要用于以下任何一个领域？",
        "description": None,
        "bullets": [
            "生物识别：如远程人脸识别、根据人脸推断情绪或种族等敏感特征。",
            "关键基础设施：如电网、供水系统、交通网络的管理和安全控制。",
            "教育：如用于学生的录取选拔、考试评分、作弊监控。",
            "就业：如用于招聘筛选、员工晋升、工作表现评估。",
            "重要服务获取：如评估个人能否获得贷款、保险、社会保障福利、公共服务。",
            "执法：如评估证据可靠性、预测犯罪高发区、评估个人再犯罪风险。",
            "移民和边境管控：如评估签证、庇护申请，或在边境进行风险评估。",
            "司法与民主：如协助法官分析案件，或用于影响选举投票。",
        ],
        "options": [
            {"label": "否", "value": "no", "next": {"type": "result", "id": "E"}},
            {"label": "是", "value": "yes", "next": {"type": "question", "id": "q6a"}},
        ],
    },
    "q6a": {
        "id": "q6a",
        "title": "问题6a：在您打算使用AI系统的上述领域里，这个系统是否只是一个无足轻重的辅助工具？",
        "description": "具体判断标准如下：",
        "bullets": [
            "它是否只执行一些简单的程序性任务（如整理文件、给邮件分类）？",
            "它是否仅仅是在人类已经完成的工作基础上进行优化（如改进文档的语法）？",
            "它是否只是检测工作模式是否存在偏差，而不会替代或影响最终的人类判断？",
            "它是否只是为重要评估做准备工作，本身的影响非常小？",
        ],
        "options": [
            {"label": "是", "value": "yes", "next": {"type": "result", "id": "E"}},
            {"label": "否", "value": "no", "next": {"type": "result", "id": "D"}},
        ],
    },
}

RESULTS: dict[str, Result] = {
    "A": {
        "id": "A",
        "title": "【结果A】不属于《人工智能法》监管范围",
        "description": "您的产品不属于《人工智能法》监管范围，无需进行AI合规认证。",
        "bullets": None,
    },
    "B": {
        "id": "B",
        "title": "【结果B】被排除在法规之外",
        "description": "您的产品因用于特殊目的或处于纯研发阶段而被排除在法规之外，无需进行AI合规认证。",
        "bullets": None,
    },
    "C": {
        "id": "C",
        "title": "【结果C】涉及法律禁止用途",
        "description": "您的产品涉及法律明令禁止的用途，不得在欧盟市场投放或使用。",
        "bullets": None,
    },
    "D": {
        "id": "D",
        "title": "【结果D】高风险AI系统",
        "description": "您的产品被归类为高风险AI系统，必须进行合规认证。",
        "bullets": [
            "需要准备详尽的技术文档。",
            "需要建立质量管理体系。",
            "通过合格评定并加贴CE标志后，方可在欧盟市场销售或提供。",
        ],
    },
    "E": {
        "id": "E",
        "title": "【结果E】非高风险AI系统",
        "description": "您的产品不属于高风险AI系统，无需进行强制性的合规认证（但可能需遵守透明度等轻度义务）。",
        "bullets": [
            "若为聊天机器人或生成/修改内容系统，需明确告知用户其正在与AI互动或内容由AI生成。",
            "仍建议遵循最佳实践，确保产品值得信赖。",
        ],
    },
}


class EvaluateRequest(BaseModel):
    answers: dict[str, AnswerValue] = Field(default_factory=dict)


class EvaluateResponse(BaseModel):
    result_id: Literal["A", "B", "C", "D", "E"]
    path: list[str]
    result: Result


app = FastAPI(title="AI Questionnaire API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tree")
def get_tree() -> dict[str, Any]:
    return {"start": "q1", "questions": list(QUESTIONS.values())}


@app.get("/api/results")
def get_results() -> dict[str, Any]:
    return {"results": list(RESULTS.values())}


def _evaluate(answers: dict[str, AnswerValue]) -> tuple[str, list[str]]:
    current_id = "q1"
    path: list[str] = []
    while True:
        question = QUESTIONS.get(current_id)
        if question is None:
            raise HTTPException(status_code=500, detail="question_not_found")

        path.append(current_id)
        answer = answers.get(current_id)
        if answer is None:
            raise HTTPException(status_code=400, detail={"missing_answer": current_id, "path": path})

        options = {opt["value"]: opt for opt in question["options"]}
        selected = options.get(answer)
        if selected is None:
            raise HTTPException(status_code=400, detail={"invalid_answer": current_id, "value": answer})

        nxt = selected["next"]
        if nxt["type"] == "result":
            return nxt["id"], path

        current_id = nxt["id"]


@app.post("/api/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest) -> EvaluateResponse:
    result_id, path = _evaluate(req.answers)
    result = RESULTS.get(result_id)
    if result is None:
        raise HTTPException(status_code=500, detail="result_not_found")
    return EvaluateResponse(result_id=result_id, path=path, result=result)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

