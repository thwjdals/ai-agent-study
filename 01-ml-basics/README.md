# 1단계 · ML/DL 기초 (5–10주)

모델이 내부에서 어떻게 학습하고 추론하는지 설명할 수 있게 한다. LLM API만 쓰는 사람과 갈리는 지점.

주교재는 Karpathy의 *Neural Networks: Zero to Hero*.
주차별 항목은 [`../CURRICULUM.md`](../CURRICULUM.md#1단계--mldl-기초-5-10주).

## 이번 단계에서 만드는 것

| 주차 | 초점 | 남는 것 |
| --- | --- | --- |
| 5주 | 선형대수·신경망 직관 | **직접 구현**: micrograd (자동 미분 엔진) |
| 6주 | makemore 1–2편, PyTorch 기본 | bigram·MLP 언어모델 |
| 7주 | makemore 3–5편, 역전파 손계산 | 학습률·과적합 실험 기록 |
| 8주 | 어텐션·트랜스포머 블록 | **직접 구현**: 미니 GPT (*Let's build GPT*) |
| 9주 | 한국어 데이터 학습 | 하이퍼파라미터별 loss 곡선 비교 |
| 10주 | 버퍼·복습 | **산출물**: 미니 GPT 레포 + 구조 해설 글 |

micrograd와 미니 GPT는 PyTorch autograd로 대신 풀지 않는다. 직접 구현이 이 단계의 전부다.

## 기록

학습률, 배치 크기, 스텝 수 같은 설정과 loss는 `results/`에 남기고 요약 표를 이 README에 올린다.
체크포인트 파일은 커밋하지 않는다(`.gitignore`).

## 졸업 기준

- 트랜스포머 블록 하나를 종이에 그리고 말로 설명 가능
- 글 1편 발행 → 초안은 [`../blog/`](../blog/)
