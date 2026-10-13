# AI Agent 엔지니어 커리큘럼

주 10시간 기준 12주 커리큘럼의 모노레포. 목표는 응용 AI 엔지니어 이직. 2026-10-13에 30주안에서 줄였다. 자격증 없이 실력과 공개 결과물로 증명한다.

- 진행 상태: **[CURRICULUM.md](CURRICULUM.md)의 체크박스가 단일 출처**
- 작업 규칙과 원칙: [CLAUDE.md](CLAUDE.md)

## 구조

| 디렉터리 | 단계 | 주차 |
| --- | --- | --- |
| [`00-python-backend/`](00-python-backend/) | Python 백엔드 | 1–2주 |
| [`01-ml-basics/`](01-ml-basics/) | LLM 기초와 로컬 모델 | 3주 |
| [`02-llm-apps/`](02-llm-apps/) | 검색과 평가 | 4–5주 |
| [`03-agent-core/`](03-agent-core/) | Agent 코어 | 6–9주 |
| [`04-production/`](04-production/) | 운영과 최적화 | 10–11주 |
| [`capstone/`](capstone/) | 평가 수치가 붙은 에이전트 하네스 | 12주 |
| [`blog/`](blog/) | 글·발표 (대외 검증) | 상시 |

## 원칙

1. **직접 구현 → 프레임워크** — 핵심을 바닥부터 한 번 만든 뒤에 프레임워크를 쓴다.
2. **수치 기록** — 2단계부터 모든 실험은 설정별 품질·지연·비용 수치로 남긴다.
3. **공개 산출물** — 단계는 레포, 글, 배포물 중 하나가 실제로 나와야 끝난다.

## 개발 환경

### 로컬 모델

```bash
brew install ollama && brew services start ollama
ollama pull qwen3:30b-a3b   # 기본 실습 (MoE, 약 19GB)
ollama pull qwen3:8b        # 약한 모델 비교용 (약 5GB)
ollama pull bge-m3          # 임베딩, 한국어 지원 (2단계 RAG)
brew install --cask lm-studio   # MLX 형식 비교용 (3주)
cp .env.example .env
```

OpenAI 호환 엔드포인트는 Ollama `http://localhost:11434/v1`, LM Studio `http://localhost:1234/v1`.

### Python

Python은 [uv](https://docs.astral.sh/uv/)로 관리한다. 루트가 uv 워크스페이스다.

```bash
# uv 설치 (한 번만)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 0단계 API 실행
cd 00-python-backend
uv run uvicorn stage00.main:app --reload

# 테스트
uv run pytest
```

새 단계에서 Python 프로젝트를 시작하면 루트 `pyproject.toml`의 `tool.uv.workspace.members`에 추가한다.

## 현재 상태

구조와 README, 0단계 FastAPI + pytest 골격까지 세팅됨. 주차 과제 코드는 아직 없다.
