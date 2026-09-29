# 1주차 · TS 개발자가 본 Python 언어 차이

주제: 타입힌트, dataclass, 제너레이터, 컨텍스트 매니저 + 『Fluent Python』 데이터 모델·함수 파트.
모든 예제는 Python 3.12에서 실제로 돌려 출력을 확인했다. 실행: `uv run python notes/week01_examples.py`

## 한 줄 요약

TS와 Python은 **타입의 위치**가 다르다. TS는 타입이 컴파일 단계에 있고 런타임에는 사라지지만,
Python은 타입힌트가 런타임에도 객체로 남아 있으면서 **아무것도 강제하지 않는다.**
대신 런타임 동작은 **던더 메서드(`__len__`, `__enter__`, `__iter__` …) 프로토콜**이 결정한다.
TS에서 타입이 하던 역할의 절반은 Python에서 던더가 한다.

## 대응표

| TS | Python | 주의 |
| --- | --- | --- |
| `interface`, `type` | `Protocol`, `TypedDict`, `dataclass` | 용도별로 갈린다 (아래) |
| `string \| null` | `str \| None` (= `Optional[str]`) | 3.10+ 부터 `\|` 문법 |
| `'a' \| 'b'` 리터럴 유니온 | `Literal["a", "b"]` | 동일 개념 |
| `readonly` / `as const` | `@dataclass(frozen=True)`, `Final` | frozen은 런타임에 실제로 막는다 |
| `class` + 생성자 보일러플레이트 | `@dataclass` | `__init__`·`__eq__`·`__repr__` 자동 |
| `function*` / `yield` | `def` + `yield` | Python 쪽이 훨씬 관용적으로 쓰인다 |
| `for await (… of …)` | `async for` | 2주차 |
| `using` (TS 5.2, Symbol.dispose) | `with` + `__enter__`/`__exit__` | Python은 20년 전부터 있던 핵심 문법 |
| 데코레이터 (클래스 멤버 위주) | 데코레이터 (함수·클래스 어디나) | Python은 그냥 고차함수다 |
| `Object.freeze`, 스프레드 | `frozen=True`, `dataclasses.replace` | |
| 연산자 오버로딩 없음 | 던더로 전부 가능 | TS에 대응 없음 |

---

## 1. 타입힌트 — 있지만 강제하지 않는다

```python
def add(a: int, b: int) -> int:
    return a + b

add("1", "2")        # → "12"   에러 없음
add.__annotations__  # → {'a': int, 'b': int, 'return': int}
```

- **런타임 검사가 없다.** TS의 `tsc`처럼 별도 타입체커(`mypy` / `pyright`)를 돌려야 의미가 있다.
  힌트만 써놓고 체커를 안 돌리면 주석과 다를 게 없다.
- 반대로 **런타임에 타입 정보가 남는다**(`__annotations__`). FastAPI·Pydantic이 이걸 읽어서
  검증·직렬화·OpenAPI 스키마를 자동 생성한다. TS에서 zod 스키마를 따로 쓰던 일이 사라진다.
  → TS: 타입(컴파일) + zod(런타임) **두 벌** / Python: 타입힌트 **한 벌**로 둘 다.

### 구조적 타이핑은 `Protocol`로

TS의 인터페이스는 기본이 구조적(덕 타이핑)인데, Python 클래스 상속은 명목적이다.
구조적으로 쓰려면 `Protocol`을 쓴다 — **구현체가 상속하지 않아도 된다.**

```python
from typing import Protocol

class Tokenizer(Protocol):
    def encode(self, text: str) -> list[int]: ...

class CharTokenizer:                      # Tokenizer를 상속하지 않았다
    def encode(self, text: str) -> list[int]:
        return [ord(c) for c in text]

def count(t: Tokenizer, text: str) -> int:
    return len(t.encode(text))

count(CharTokenizer(), "hi")              # → 2, 타입체커도 통과
```

- `@runtime_checkable`을 붙이면 `isinstance()`도 되지만 **메서드 존재만** 보고 시그니처는 안 본다.
- 실무 감각: 내가 정의하는 경계(프로바이더, 스토리지, 툴 인터페이스)는 ABC 상속보다 `Protocol`이 낫다.
  테스트 더블을 상속 없이 끼울 수 있다.

### interface 자리에 뭘 쓰나

| 상황 | 선택 |
| --- | --- |
| 메서드 있는 경계 (의존성 주입) | `Protocol` |
| 값 묶음, 내가 만드는 객체 | `@dataclass` |
| 외부에서 온 dict 모양 (JSON 응답) | `TypedDict` |
| 외부 입력을 **검증**해야 함 (API 바디, 설정) | `pydantic.BaseModel` |

`TypedDict`는 런타임에 그냥 dict다. 검증이 필요하면 Pydantic — 3주차 FastAPI에서 본격적으로.

---

## 2. dataclass — 값 객체의 기본형

```python
from dataclasses import dataclass, field, replace, asdict

@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str
    meta: dict[str, str] = field(default_factory=dict)

m = Message("user", "hi")
m                              # Message(role='user', content='hi', meta={})   __repr__ 공짜
m == Message("user", "hi")     # True                                          __eq__ 공짜 (값 비교!)
replace(m, content="bye")      # 스프레드 대응: {...m, content: "bye"}
asdict(m)                      # {'role': 'user', 'content': 'hi', 'meta': {}}
m.role = "assistant"           # FrozenInstanceError
```

- `__eq__`가 **값 비교**로 생성된다. TS 클래스 인스턴스는 참조 비교였던 것과 다르다. 테스트가 편해진다.
- `frozen=True` = 런타임 불변. `readonly`가 컴파일타임에만 있던 것과 달리 실제로 막힌다.
- `slots=True` = `__dict__` 제거. 메모리 줄고 오타 속성 대입이 막힌다.
  (함정: `frozen=True, slots=True` 조합에서 없는 속성에 대입하면 `AttributeError`가 아니라
  `TypeError: super(type, obj)...`라는 엉뚱한 메시지가 난다. dataclass 구현 특성이라 당황하지 말 것.)

### 가장 많이 밟는 함정: 가변 기본값

기본값은 **정의 시점에 한 번** 평가되고 호출마다 공유된다. TS에는 없는 함정이다.

```python
def append_bad(x, acc=[]):        # 나쁜 예
    acc.append(x); return acc
append_bad(1), append_bad(2)      # → ([1, 2], [1, 2])   같은 리스트!

def append_ok(x, acc=None):       # 관용적 해법
    acc = [] if acc is None else acc
    acc.append(x); return acc
append_ok(1), append_ok(2)        # → ([1], [2])
```

dataclass에서 같은 이유로 `meta: dict = {}`는 에러가 나고 `field(default_factory=dict)`를 써야 한다.

---

## 3. 제너레이터 — Python의 주력 도구

```python
def chunks(text: str, size: int):
    for i in range(0, len(text), size):
        yield text[i : i + size]

g = chunks("abcdefg", 3)
list(g)   # → ['abc', 'def', 'g']
list(g)   # → []            한 번 쓰면 소진된다 (TS iterator와 동일)
```

- **게으르다.** 10,000자를 3자씩 자르는 제너레이터는 232 bytes, 같은 걸 리스트로 만들면 29,336 bytes.
  (실측) 스트리밍·대용량 파일·토큰 단위 처리에서 이 차이가 곧 메모리 상한이 된다.
- 무한 시퀀스가 자연스럽다: `itertools.islice(naturals(), 5)` → `[0, 1, 2, 3, 4]`
- **제너레이터 표현식**은 리스트를 안 만든다: `sum(len(c) for c in chunks(t, 3))`.
  `[...]`로 감싸는 순간 전부 메모리에 올라간다. TS의 `.map().filter()` 체인이 매번 배열을
  새로 만드는 것과 대비되는 습관.
- `yield from other_gen()` = 위임. 재귀적 순회에 쓴다.
- **중요:** `yield`가 멈췄다 재개하는 이 메커니즘이 `async`/`await`의 뿌리다. 2주차 asyncio가
  이 위에 올라간다. 이번 주에 제너레이터를 몸으로 익혀두면 다음 주가 쉬워진다.

LLM 스트리밍이 곧 이 모양이다 — 3주차 SSE에서 `yield`로 토큰을 흘려보낸다.

---

## 4. 컨텍스트 매니저 — `try/finally`를 이름 붙여 재사용

TS는 5.2에서야 `using`이 생겼고 거의 안 쓰인다. Python에서는 리소스·계측·트랜잭션 전부 이 문법이다.

```python
from contextlib import contextmanager
import time

@contextmanager
def timed(label: str):
    t0 = time.perf_counter()
    try:
        yield                       # 여기가 with 블록 본문
    finally:
        print(f"{label}: {(time.perf_counter() - t0) * 1000:.2f}ms")

with timed("sleep"):
    time.sleep(0.01)                # → sleep: 15.01ms
```

제너레이터 하나로 "앞/뒤"를 감싼다 — 3번과 4번이 같은 메커니즘이라는 게 핵심이다.

클래스로 쓰면 `__enter__` / `__exit__`이고, **`__exit__`이 `True`를 반환하면 예외를 삼킨다.**

```python
class Tracked:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb):
        return True                 # 예외를 여기서 끝낸다

with Tracked():
    raise ValueError("터졌다")
print("여기까지 온다")               # 실행된다
```

`contextlib.suppress(ZeroDivisionError)`도 같은 원리. 이 "삼킴"은 TS에 대응 개념이 없어서
처음에 예외가 사라지는 걸로 보일 수 있으니 반환값을 반드시 의식할 것.

실무에서 만나는 지점: DB 세션/트랜잭션, 파일, httpx 클라이언트, 락, 그리고 FastAPI의 `lifespan`.
`async with`(비동기 버전)는 2주차.

---

## 5. 『Fluent Python』 발췌 — 데이터 모델과 함수

### 데이터 모델: 던더는 언어 기능에 꽂는 플러그

내 클래스에 `__len__`과 `__getitem__`만 구현하면 **내장 문법이 전부 따라온다.**

```python
class TokenSeq:
    def __init__(self, ids): self._ids = list(ids)
    def __len__(self): return len(self._ids)
    def __getitem__(self, i): return self._ids[i]
    def __repr__(self): return f"TokenSeq({self._ids})"

s = TokenSeq([10, 20, 30, 40])
len(s)        # 4          ← __len__
s[1]          # 20         ← __getitem__
s[1:3]        # [20, 30]   슬라이싱도 공짜
20 in s       # True       __contains__ 없이 __getitem__으로 폴백
[x for x in s]  # [10, 20, 30, 40]   __iter__ 없이 반복도 된다
```

TS라면 `Symbol.iterator`를 직접 구현하고 인덱싱·슬라이싱은 흉내도 못 낸다.
**"파이썬답다"는 건 이 프로토콜에 맞춰 쓴다는 뜻이다.** 알아둘 던더:

| 던더 | 켜지는 기능 |
| --- | --- |
| `__len__`, `__getitem__` | `len()`, 인덱싱, 슬라이싱, 반복, `in` |
| `__iter__`, `__next__` | 반복자 |
| `__repr__` / `__str__` | 디버깅 출력 / `print` |
| `__eq__`, `__hash__` | 비교, dict 키·set 원소 |
| `__enter__`, `__exit__` | `with` |
| `__call__` | 인스턴스를 함수처럼 호출 |
| `__add__`, `__lt__` … | 연산자 오버로딩 |

### 함수는 일급 객체 + 데코레이터는 그냥 고차함수

TS 데코레이터는 클래스 멤버 위주에 실험적 취급이었지만, Python 데코레이터는 문법설탕일 뿐이다:
`@retry(3)` 은 `flaky = retry(3)(flaky)` 와 같다.

```python
from functools import wraps

def retry(times: int):
    def deco(fn):
        @wraps(fn)                      # 이름·독스트링 보존 (안 붙이면 wrapper로 바뀐다)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    print(f"  시도 {attempt} 실패: {e}")
            raise RuntimeError(f"{fn.__name__} {times}회 실패")
        return wrapper
    return deco

@retry(times=3)
def flaky(): ...
```

이 3중 중첩(인자 → 함수 → 래퍼)이 데코레이터의 기본형이다. **2주차에 만들 재시도 클라이언트가
이 구조의 async 버전이다.**

알아둘 `functools`:

| 도구 | 용도 | 실측 |
| --- | --- | --- |
| `@wraps` | 래퍼가 원 함수 이름을 유지 | `flaky.__name__ == "flaky"` |
| `@lru_cache` | 메모이제이션 | 15.01ms → 0.00ms, `cache_info()`로 hit/miss 확인 |
| `partial(add, 10)` | 인자 고정 | `partial(add, 10)(5)` → 15 |

`@lru_cache`는 인자가 해시 가능해야 한다(dict·list 불가). 이 제약이 `frozen=True` dataclass를
쓰는 또 하나의 이유다.

---

## TS 경험이 그대로 먹히는 것 / 새로 배워야 하는 것

**그대로 먹힌다**: 구조적 타이핑 사고, 제너레이터/이터레이터 개념, async 멘탈모델(2주차),
유니온·리터럴 타입, 불변 데이터 선호, 고차함수.

**새로 배워야 한다**:
1. 타입은 체커를 돌려야 존재한다 (그리고 런타임에도 읽힌다 → FastAPI·Pydantic)
2. 던더 프로토콜 — Python에서 가장 큰 사고방식 차이
3. 가변 기본값 함정
4. `with` / 컨텍스트 매니저를 일상적으로 쓰는 습관
5. `list()` 대신 제너레이터를 기본값으로 두는 습관

## 다음 주로 넘기는 것

- 제너레이터 → `async`/`await`, 이벤트 루프 (2주차)
- `retry` 데코레이터 → 지수 백오프 + 세마포어 붙인 async HTTP 클라이언트 (2주차 직접 구현)
- 타입힌트 런타임 활용 → Pydantic·의존성 주입 (3주차)
- `yield` → SSE 스트리밍 (3주차)
