# joongyuskill

카파시가 말한 "AI 답변 이해하기" 4가지를 Claude Code 명령어 하나로.

1. **항공정비 언어(ASD-STE100)** — 짧은 문장, 능동태, 역할별 블록(누가 한 일 / 제가 한 일 / 남은 일정 / 사용자가 하실 일)
2. **다이어그램** — 글 대신 Mermaid/ASCII 그림
3. **HTML** — 답변을 한 페이지로
4. **영상** — 장면 HTML → mp4

## 설치

```
/plugin marketplace add joongyu01/joongyuskill
/plugin install joongyuskill@joongyuskill
```

### Codex

```bash
codex plugin marketplace add joongyu01/joongyuskill
codex plugin add joongyuskill@joongyuskill
```

Codex 앱은 설치 후 재시작하면 됩니다. Codex에서는 `$joongyuskill export` 처럼 부르거나 "joongyuskill export 해줘"라고 말하면 됩니다.

## 사용

| 명령 | 동작 |
|------|------|
| `/joongyuskill` | STE 모드 켜기 (세션 내내) |
| `/joongyuskill diagram` | 직전 답변을 다이어그램으로 |
| `/joongyuskill html` | 직전 답변을 HTML로 |
| `/joongyuskill video` | 직전 답변을 mp4로 |
| `/joongyuskill export` | HTML + mp4 |
| `/joongyuskill off` | 끄기 |

영상은 Chrome 또는 Edge와 `pip install imageio-ffmpeg` 가 필요합니다.

## 예시 (STE 모드)

```
bizops가 한 일
- 검색어 수가 46개에서 58개로 늘었습니다.

제가 한 일
- 위키 inbox 항목을 완료 표시했습니다. 커밋은 25a273c입니다.

남은 일정
- 10-29 중간 점검: 10-24 기준선과 비교합니다.

사용자가 하실 일
- 없습니다.
```

MIT License
