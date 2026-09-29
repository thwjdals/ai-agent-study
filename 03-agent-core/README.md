# 3단계 · Agent 코어 (17–24주)

이 직무의 본업. 각 개념을 바닥부터 만든 뒤에 프레임워크로 넘어간다.
본업의 Claude Code MCP 멀티에이전트 경험을 여기서 회수한다.

주차별 항목은 [`../CURRICULUM.md`](../CURRICULUM.md#3단계--agent-코어-17-24주).

## 이번 단계에서 만드는 것

| 주차 | 초점 | 남는 것 |
| --- | --- | --- |
| 17주 | Anthropic *Building effective agents* | **직접 구현**: 프레임워크 없는 tool calling 루프 (최대 스텝, 에러 복구) |
| 18주 | MCP 스펙 (JSON-RPC, tools·resources·prompts, stdio·HTTP) | **직접 구현**: SDK 없이 MCP 서버 |
| 19주 | 공식 SDK | **산출물**: 쓸 만한 MCP 서버를 npm 또는 PyPI에 배포 |
| 20주 | LangGraph (상태 그래프, 체크포인트, HITL) | 17주 버전과 같은 워크플로우로 비교 |
| 21주 | OpenAI Agents SDK / Claude Agent SDK / Google ADK 중 2개+ | 같은 과제 다중 구현 + 비교표 |
| 22주 | A2A (Agent Card, Task 수명주기) | 다른 프레임워크 에이전트 2개 협업 |
| 23주 | 지식그래프, Neo4j·Cypher | GraphRAG: 엔티티·관계 추출 → KG → 에이전트 tool |
| 24주 | 멀티에이전트 평가 | 성공률·스텝 수·비용, **캡스톤 v1** |

## 짝 비교 구조

직접 구현과 프레임워크 버전을 **둘 다 남긴다**. 중복이 아니라 비교 자료다.

- 17주 (직접 루프) ↔ 20주 (LangGraph) ↔ 21주 (SDK 2종)
- 18주 (JSON-RPC 직접) ↔ 19주 (공식 SDK)

비교는 코드 길이·제어 범위·디버깅 난이도에 성공률·스텝 수·비용 수치를 붙여서 표로 만든다.

## 졸업 기준

- MCP 서버 공개 후 내가 아닌 사용자 확보
- 첫 OSS PR 머지 (후보: MCP SDK·서버, LangGraph, A2A SDK, vLLM)
- 글 2편: MCP 직접 구현기, 에이전트 프레임워크 비교 → 초안은 [`../blog/`](../blog/)
