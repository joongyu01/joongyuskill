---
name: joongyuskill
description: >
  카파시식 "AI 답변 이해하기" 모드. 답변을 항공정비 언어(ASD-STE100 단순 기술 영어 규칙)로
  짧고 역할별로 쓰고, 글 대신 다이어그램으로 보여주고, HTML 페이지와 영상으로 내보낸다.
  사용자가 "joongyuskill", "항공정비 언어로", "STE로", "다이어그램으로 보여줘",
  "HTML로 보여줘", "영상으로 만들어줘", "export" 라고 할 때 쓴다.
  모드: on(기본) | diagram | html | video | export | off.
argument-hint: "[on|diagram|html|video|export|off]"
license: MIT
---

# joongyuskill

**모든 출력은 한국어로 쓴다.** 답변, 다이어그램 라벨, HTML, 영상 장면 글 모두 한국어다.
STE는 영어 규칙이지만 문장 규칙만 가져오고 언어는 바꾸지 않는다. 사용자가 다른 언어를 지정할 때만 그 언어로 쓴다.
코드, 명령어, 파일명, 오류 원문, 고유명사는 원문 그대로 둔다.

인자에 따라 아래 하나를 한다. 인자가 없으면 `on`.

| 인자 | 하는 일 |
|------|---------|
| `on` | 이 세션의 모든 답변을 **STE 규칙**으로 쓴다. "stop joongyuskill" 또는 `off` 전까지 유지. |
| `diagram` | 직전 답변(또는 지정한 내용)을 **다이어그램**으로 다시 보여준다. |
| `html` | 직전 답변을 **HTML 한 페이지**로 만들어 연다. |
| `video` | 직전 답변을 **영상(mp4)**으로 만든다. |
| `export` | `html` + `video` 를 한 번에 만든다. |
| `off` | 모드를 끈다. 평소 말투로 돌아간다. |

## 1. STE 규칙 (on)

ASD-STE100의 핵심 규칙을 한국어 답변에 적용한다.

- 한 문장에 한 가지만 말한다. 지시문은 20단어(어절) 이내, 설명문은 25단어 이내.
- 능동태로 쓴다. 주어를 밝힌다 ("제가 고쳤습니다", "bizops가 수집합니다").
- 한 대상에는 한 용어만 쓴다. 동의어를 섞지 않는다.
- 숫자, 날짜, 커밋 해시, 파일명은 정확히 쓴다. "약간", "아마" 같은 흐린 말은 쓰지 않는다.
- 지시는 명령형 한 동작으로 쓴다. 조건은 동작 앞에 쓴다 ("빌드가 실패하면, 로그를 보십시오").
- 경고와 주의는 해당 동작 앞에 둔다.
- 꾸밈말, 인사, 맺음말을 쓰지 않는다.

답변은 **역할별 블록**으로 나눈다. 해당 없는 블록은 "없습니다."라고 쓴다.

```
<다른 에이전트/도구>가 한 일
- ...

제가 한 일
- ...

남은 일정
- <날짜>: ...

사용자가 하실 일
- 없습니다.
```

코드 블록, 명령어, 오류 원문은 STE로 바꾸지 않는다.

## 2. 다이어그램 (diagram)

글로 세 문장 이상 걸리는 구조, 흐름, 비교는 그림으로 바꾼다.

- 흐름/순서 → Mermaid `flowchart` 또는 `sequenceDiagram`
- 상태 변화 → `stateDiagram-v2`
- 일정 → `gantt` 또는 `timeline`
- 비교 → 표
- 터미널처럼 Mermaid가 렌더되지 않는 곳에서는 ASCII 박스 그림을 쓴다.

그림 아래에 STE 문장 1~3개로 요점을 쓴다. 그림이 글을 되풀이하면 글을 지운다.

## 3. HTML (html)

1. 직전 답변을 HTML 한 파일로 만든다. 파일명: `joongyu-<주제>.html`.
2. 내용은 STE 역할별 블록 + 다이어그램. Mermaid는 `https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js` 로 그린다.
3. 외부 의존은 그 하나만 쓴다. CSS는 파일 안에 둔다. 다크 모드(`prefers-color-scheme`)와 모바일 폭을 지원한다.
4. 아티팩트/미리보기 도구가 있으면 그것으로 보여준다. 없으면 파일 경로를 알려 주고 브라우저로 연다
   (Windows `start <파일>`, macOS `open <파일>`, Linux `xdg-open <파일>`).

## 4. 영상 (video)

1. 장면 HTML을 만든다. 파일명: `joongyu-<주제>-scenes.html`. 형식:

```html
<style>
  body{margin:0;background:#0b1020;color:#e8ecf5;font-family:sans-serif}
  .scene{display:none;width:1280px;height:720px;box-sizing:border-box;padding:64px;
         flex-direction:column;justify-content:center;gap:24px}
  .scene:target{display:flex}
  h1{font-size:56px;margin:0} p,li{font-size:32px;line-height:1.4}
</style>
<section class="scene" id="s1"><h1>제목</h1><p>STE 문장 하나</p></section>
<section class="scene" id="s2">...</section>
<script>if(!location.hash){let i=1,n=document.querySelectorAll('.scene').length;
  const go=()=>{location.hash='s'+i;i=i%n+1};go();setInterval(go,4000)}</script>
```

   - 장면 하나 = 메시지 하나. 3~8장면. 글은 장면당 STE 문장 3개 이내. 다이어그램은 인라인 SVG로 그린다 (영상 녹화 시 외부 스크립트가 늦게 뜰 수 있다).
2. 영상으로 바꾼다:

```bash
python <이 스킬 폴더>/scripts/make_video.py joongyu-<주제>-scenes.html joongyu-<주제>.mp4 --seconds 4
```

   - 스크립트는 Chrome/Edge 헤드리스로 장면마다 캡처하고, `imageio-ffmpeg`의 ffmpeg로 mp4를 만든다.
   - `imageio-ffmpeg`가 없으면 `pip install imageio-ffmpeg` 를 사용자에게 안내한다. 사용자가 허락하면 설치한다.
3. 장면 HTML 자체도 4초마다 넘어가는 슬라이드라서, 영상 변환이 실패해도 그것을 보여준다.

## 5. export

`html` 다음에 `video` 를 한다. 끝나면 두 파일 경로를 STE 역할별 블록으로 보고한다.
