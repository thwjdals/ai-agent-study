# 0단계 · Python 백엔드 (1–2주)

TS로 하던 걸 Python으로 같은 수준에서 할 수 있게 만든다. AI 팀 대부분의 주 언어가 Python이다.

주차별 항목은 [`../CURRICULUM.md`](../CURRICULUM.md#0단계--python-백엔드-12주)의 체크박스를 본다.

## 이번 단계에서 만드는 것

| 주차 | 초점 | 남는 것 |
| --- | --- | --- |
| 1주 | 언어 차이, asyncio | 비교 노트, **직접 구현**: 동시성 제한 + 지수 백오프 비동기 HTTP 클라이언트 |
| 2주 | FastAPI, Pydantic, DI, SSE / pytest | **산출물**: LLM 게이트웨이 |

게이트웨이는 로컬 모델(Ollama·LM Studio의 OpenAI 호환 서버)과 클라우드 API를 같은 인터페이스로 묶고,
스트리밍과 요청 로그 SQLite 저장까지 포함한다. 3단계 하네스가 이 게이트웨이를 통해 모델을 부른다.

## 졸업 기준

- 게이트웨이 GitHub 공개, 테스트 커버리지 80% 이상, README에 구조와 실행법

## 현재 골격

```
src/stage00/
  main.py      FastAPI 앱, GET /health
  config.py    pydantic-settings 설정 + get_settings 의존성
tests/
  conftest.py  httpx ASGITransport 기반 async client 픽스처
  test_health.py
```

과제 코드는 아직 없다. 주차를 시작할 때 여기서부터 확장한다.

## 실행

```bash
uv run uvicorn stage00.main:app --reload   # http://127.0.0.1:8000/health
uv run pytest
uv run pytest --cov                        # 커버리지 (졸업 기준 80%)
uv add <패키지>                             # 런타임 의존성
uv add --dev <패키지>                       # 개발 의존성
```

의존성은 워크스페이스 루트의 `uv.lock` 하나로 잠긴다. `pip`은 쓰지 않는다.
