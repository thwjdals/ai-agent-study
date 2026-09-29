print("=== A. 타입힌트는 런타임에 무시된다 ===")
def add(a: int, b: int) -> int:
    return a + b
print(add("1", "2"), "|", add.__annotations__)

print("=== B. Protocol = 구조적 타이핑 ===")
from typing import Protocol, runtime_checkable
@runtime_checkable
class Tokenizer(Protocol):
    def encode(self, text: str) -> list[int]: ...
class CharTokenizer:                      # Tokenizer를 상속하지 않았다
    def encode(self, text: str) -> list[int]:
        return [ord(c) for c in text]
def count(t: Tokenizer, text: str) -> int:
    return len(t.encode(text))
print(count(CharTokenizer(), "hi"), "|", isinstance(CharTokenizer(), Tokenizer))

print("=== C. 가변 기본값 함정 ===")
def append_bad(x, acc=[]):
    acc.append(x); return acc
print(append_bad(1), append_bad(2))
def append_ok(x, acc=None):
    acc = [] if acc is None else acc
    acc.append(x); return acc
print(append_ok(1), append_ok(2))

print("=== D. dataclass ===")
from dataclasses import dataclass, field, replace, asdict
@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str
    meta: dict[str, str] = field(default_factory=dict)
m = Message("user", "hi")
print(m)
print(replace(m, content="bye"), "|", asdict(m))
print(m == Message("user", "hi"))
try:
    m.role = "assistant"
except Exception as e:
    print(type(e).__name__, e)
try:
    m.typo = 1
except Exception as e:
    print(type(e).__name__, e)

print("=== E. 제너레이터 ===")
def chunks(text: str, size: int):
    for i in range(0, len(text), size):
        yield text[i : i + size]
g = chunks("abcdefg", 3)
print(type(g).__name__, "|", list(g), "|", list(g))   # 두 번째는 빈 리스트
import itertools, sys
def naturals():
    n = 0
    while True:
        yield n
        n += 1
print(list(itertools.islice(naturals(), 5)))
print(sum(len(c) for c in chunks("abcdefg", 3)))
print("메모리:", sys.getsizeof(chunks("x" * 10_000, 3)), "bytes vs list", sys.getsizeof(list(chunks("x" * 10_000, 3))))

print("=== F. 컨텍스트 매니저 ===")
import time
from contextlib import contextmanager, suppress
@contextmanager
def timed(label: str):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {(time.perf_counter() - t0) * 1000:.2f}ms")
with timed("sleep"):
    time.sleep(0.01)
class Tracked:
    def __enter__(self):
        print("enter"); return self
    def __exit__(self, exc_type, exc, tb):
        print("exit, 예외:", exc_type.__name__ if exc_type else None)
        return True                       # True = 예외 삼킴
with Tracked():
    raise ValueError("터졌다")
print("여기까지 온다")
with suppress(ZeroDivisionError):
    1 / 0
print("suppress도 같은 원리")

print("=== G. 데이터 모델 (던더) ===")
class TokenSeq:
    def __init__(self, ids):
        self._ids = list(ids)
    def __len__(self):
        return len(self._ids)
    def __getitem__(self, i):
        return self._ids[i]
    def __repr__(self):
        return f"TokenSeq({self._ids})"
s = TokenSeq([10, 20, 30, 40])
print(len(s), s[1], s[1:3], 20 in s, [x for x in s], s)

print("=== H. 일급함수·데코레이터 ===")
from functools import wraps, partial, lru_cache
def retry(times: int):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    print(f"  시도 {attempt} 실패: {e}")
            raise RuntimeError(f"{fn.__name__} {times}회 실패")
        return wrapper
    return deco
calls = {"n": 0}
@retry(times=3)
def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise IOError("타임아웃")
    return "성공"
print(flaky(), "| 이름 보존:", flaky.__name__)
@lru_cache(maxsize=None)
def slow_square(n: int) -> int:
    time.sleep(0.01)
    return n * n
with timed("캐시 전"):
    slow_square(12)
with timed("캐시 후"):
    slow_square(12)
print(slow_square.cache_info())
print(partial(add, 10)(5))
