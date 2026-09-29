# 0단계 · Python 백엔드 (1–4주)

TS로 하던 걸 Python으로 같은 수준에서 할 수 있게 만든다. AI 팀 대부분의 주 언어가 Python이다.

주차별 항목은 [`../CURRICULUM.md`](../CURRICULUM.md#0단계--python-백엔드-1-4주)의 체크박스를 본다.

## 이번 단계에서 만드는 것

| 주차 | 초점 | 남는 것 |
| --- | --- | --- |
| 1주 | 언어 차이 (타입힌트, dataclass, 제너레이터, 컨텍스트 매니저) | 비교 노트 |
| 2주 | asyncio | **직접 구현**: 동시성 제한 + 지수 백오프 비동기 HTTP 클라이언트 |
| 3주 | FastAPI, Pydantic, DI, SSE / pytest | 이 골격을 확장 |
| 4주 | PostgreSQL, SQLAlchemy | **산출물**: LLM 게이트웨이 서버 |

산출물인 게이트웨이는 멀티 프로바이더, 스트리밍, 레이트리밋, 요청 로그 DB 저장까지 포함한다.

## 졸업 기준

- 게이트웨이 GitHub 공개, 테스트 커버리지 80% 이상, README에 구조와 실행법
- 글 1편: TS 개발자가 본 Python 비동기 → 초안은 [`../blog/`](../blog/)

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
