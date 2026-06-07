# Research Agent Skill

`research-agent`는 Codex에서 사용할 수 있는 portable Skill입니다. 사용자의 research project repo 안에서 현재 상태를 파악하고, 연구를 `Motivation -> Method -> Experiments -> HTML brief -> Slides` 흐름으로 정리하거나 함께 진행하도록 돕습니다.

빈 repo에서는 먼저 `goal instruction discussion`을 통해 연구 자동화 목표를 정리할 수 있고, 이미 official baseline repo를 clone해서 Method 수정과 Experiments까지 진행한 repo에서는 `Existing Project Import`로 지금까지의 작업을 research-agent 형식에 맞게 정리할 수 있습니다.

## 주요 기능

- 현재 repo가 `empty_repo`, `existing_user_project`, `official_baseline`, `baseline_working_project`, `partial_research_agent_project` 중 무엇인지 inspect합니다.
- 빈 repo에서는 `/goal`에 붙여 넣을 수 있는 `goal instruction` 후보를 discussion 후 추천합니다.
- 이미 작업한 baseline repo에서는 기존 Method 변경사항, baseline/proposed Experiments, result artifacts를 수집해 `project_import` stage로 정리합니다.
- `01_motivation`, `02_method`, `03_experiments`, `04_slides` stage를 명시적으로 나누어 관리합니다.
- Motivation report는 영어/한국어 버전을 모두 지원하고, 자료 검색에 사용한 tool/MCP usage provenance를 기록하도록 설계되어 있습니다.
- 최종 결과를 `research/research-brief.html`로 정리하고, `slides-grab` 기반 HTML-first slides와 PDF export를 생성합니다.

## 설치

먼저 skill repo를 clone합니다.

```bash
git clone https://github.com/hybyun0121/research-codex-skill.git
cd research-codex-skill
```

Codex가 skill을 찾을 수 있도록 등록합니다. 개발하거나 자주 업데이트할 예정이면 symlink 방식을 추천합니다.

```bash
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$CODEX_SKILLS_DIR"
ln -sfn "$(pwd)/skills/research-agent" "$CODEX_SKILLS_DIR/research-agent"
```

copy 방식으로 self-contained install을 하고 싶다면 아래처럼 등록할 수 있습니다.

```bash
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$CODEX_SKILLS_DIR"
rm -rf "$CODEX_SKILLS_DIR/research-agent"
cp -R "$(pwd)/skills/research-agent" "$CODEX_SKILLS_DIR/research-agent"
```

등록이 되었는지 확인합니다.

```bash
ls -l "${CODEX_HOME:-$HOME/.codex}/skills/research-agent/SKILL.md"
```

그 다음 Codex를 restart하거나 새 Codex session을 열어 skill list를 refresh합니다.

## 기본 사용법

실제로 연구를 진행할 project repo로 이동한 뒤 Codex를 실행합니다.

```bash
cd <your-research-project>
codex
```

Codex에서 아래처럼 실행합니다.

```text
$research-agent
```

또는 Codex surface가 지원한다면 `/skills`에서 `research-agent`를 선택할 수 있습니다.

`research-agent`는 먼저 repo를 inspect하고, 현재 상태에 따라 다음 workflow 중 하나로 들어갑니다.

| Repo 상태 | 동작 |
|---|---|
| `empty_repo` | `goal instruction discussion`을 할지 물어본 뒤 Motivation으로 진행 |
| `existing_user_project` | 기존 project 내용을 파악하고 필요한 stage부터 진행 |
| `official_baseline` | baseline 구조와 paper/eval pipeline을 파악한 뒤 연구 방향 정리 |
| `baseline_working_project` | 이미 수정/실험한 baseline repo로 보고 `Existing Project Import`를 제안 |
| `partial_research_agent_project` | 기존 `.research-agent/state.json`을 기준으로 이어서 진행 |

## 빈 Repo에서 시작하기

아직 code나 research question이 없는 repo에서는 `research-agent`가 먼저 `goal instruction discussion`을 제안합니다.

```bash
mkdir my-new-research
cd my-new-research
codex
```

```text
$research-agent
```

이 flow에서는 user와 discussion을 통해 다음 내용을 정리합니다.

- 연구 domain 또는 seed research question
- 자동화하고 싶은 범위
- toy experiment budget
- code 변경 허용 여부
- report/slides output expectation

discussion이 끝나면 여러 개의 `goal instruction` 후보를 추천하고, user가 하나를 선택하거나 merge/customize할 수 있게 합니다. 선택된 결과는 아래 파일로 저장됩니다.

```text
.research-agent/goal_instruction.md
.research-agent/goal_command.txt
.research-agent/goal_instruction.json
```

최종 사용 방식은 `goal` skill을 열고, 생성된 `goal instruction`을 `/goal` 뒤에 붙여 넣는 형태를 의도합니다.

```text
/goal <generated goal instruction>
```

## 이미 작업한 Baseline Repo 정리하기

official baseline GitHub repo를 연구실 서버나 로컬에 clone한 뒤, 그 위에 본인 Method를 적용하고 baseline/proposed Experiments까지 진행한 경우에도 같은 방식으로 실행합니다.

```bash
cd <your-modified-baseline-project>
codex
```

```text
$research-agent
```

repo 안에서 다음 signal이 발견되면 `baseline_working_project`로 분류하고 `Existing Project Import`를 제안합니다.

- official paper/citation/README signal
- train/eval/benchmark script
- user modified files 또는 untracked files
- `results/`, `runs/`, `logs/`, `wandb/`, `tensorboard/` 같은 experiment artifact directory
- `.csv`, `.json`, `.jsonl`, `.tsv`, `.log`, `.md` 형태의 result summary 후보

Import를 선택하면 아래 내용을 정리합니다.

- baseline identity
- official paper/repo evidence
- user modification evidence
- proposed Method 후보 파일
- train/eval pipeline
- baseline vs proposed result artifact 후보
- stage별 reconstruction plan
- user confirmation이 필요한 open questions

생성되는 주요 파일은 다음과 같습니다.

```text
.research-agent/project_import.json
research/project-import.md
```

그 후 confirmed evidence를 바탕으로 아래 stage artifacts를 재구성합니다.

```text
research/motivation.md
research/motivation.ko.md
research/method.md
research/experiments.md
research/research-brief.html
```

## Stage 구조

Skill 내부 구조는 다음처럼 구성되어 있습니다.

```text
skills/research-agent/
├── goal-instructor/
│   ├── instructions/
│   ├── schemas/
│   └── templates/
├── repo-ingestion/
│   ├── instructions/
│   ├── schemas/
│   └── templates/
├── stages/
│   ├── 01_motivation/
│   ├── 02_method/
│   ├── 03_experiments/
│   └── 04_slides/
├── instructions/
├── schemas/
├── scripts/
└── templates/
```

각 stage의 역할은 다음과 같습니다.

| Stage | 목적 |
|---|---|
| `01_motivation` | related work landscape, novelty gap, worth solving 기준, Motivation report 작성 |
| `02_method` | proposed Method 구체화, mathematical formulation, rigor review, pseudocode/visualization |
| `03_experiments` | benchmark plan, hyperparameter sweep, leaderboard, qualitative analysis 설계 |
| `04_slides` | `slides-grab` 기반 professor-facing English slides, PDF/PNG export, infographic-style visual report |

## Slides Workflow

Slides는 기본적으로 `slides-grab` HTML-first workflow를 따릅니다. PowerPoint를 직접 만드는 방식이 아니라, slide별 HTML을 만들고 이를 viewer/PDF/PNG로 export하는 방식입니다.

기본 output은 다음과 같습니다.

```text
slides/
├── slide-01.html
├── slide-02.html
├── assets/
├── viewer.html
├── out-png/
└── research-presentation.pdf
```

PPTX export는 `slides-grab convert` 기반의 optional/experimental artifact로 취급합니다.

```text
slides/research-presentation.pptx
```

## Research Repo에 생성되는 파일

`research-agent`는 사용자의 project repo 안에 최소한의 관리 파일과 report 파일만 생성합니다.

```text
.research-agent/
├── state.json
├── config.json
├── repo_profile.json
├── project_import.json
├── decisions.jsonl
├── goal_instruction.md
├── goal_command.txt
└── goal_instruction.json
research/
├── status.md
├── project-import.md
├── motivation.md
├── motivation.ko.md
├── method.md
├── experiments.md
└── research-brief.html
slides/
├── slide-01.html
├── slide-02.html
├── assets/
├── viewer.html
├── out-png/
└── research-presentation.pdf
```

상황에 따라 일부 파일은 생성되지 않을 수 있습니다. 예를 들어 `project_import.json`은 `Existing Project Import`를 선택했을 때 의미가 있고, `goal_instruction.*` 파일은 빈 repo에서 goal discussion을 선택했을 때 의미가 있습니다.

## Skill 업데이트

symlink 방식으로 설치했다면 skill repo에서 pull만 하면 됩니다.

```bash
cd <path-to>/research-codex-skill
git pull
```

그 다음 Codex를 restart하거나 새 session을 열어 skill metadata를 refresh합니다.

copy 방식으로 설치했다면 pull 후 다시 복사합니다.

```bash
cd <path-to>/research-codex-skill
git pull

CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
rm -rf "$CODEX_SKILLS_DIR/research-agent"
cp -R "$(pwd)/skills/research-agent" "$CODEX_SKILLS_DIR/research-agent"
```

## Optional Vendor Install

특정 research repo 안에 skill을 vendor로 포함하고 싶다면 아래처럼 복사할 수 있습니다.

```bash
cd <your-research-project>
mkdir -p .agents/skills
cp -R <path-to>/research-codex-skill/skills/research-agent .agents/skills/
codex
```

그 다음 동일하게 실행합니다.

```text
$research-agent
```

다만 일반적인 사용에서는 `~/.codex/skills/research-agent` 등록 방식을 추천합니다. 여러 project repo에서 같은 skill을 재사용하기 쉽기 때문입니다.

## Safety

`research-agent`는 credential이나 private file을 읽거나 요약하거나 수정하지 않도록 설계되어 있습니다.

읽지 않아야 하는 파일 예시는 다음과 같습니다.

- `.env`, `.env.*`
- `*.pem`, `*.key`
- `id_rsa`, `id_ed25519`
- filename에 `token`, `secret`, `credential`, `password`가 들어간 파일
- checkpoints, model weights, raw datasets, large binary artifacts

또한 user가 명시적으로 요청하지 않는 한 baseline implementation file을 수정하지 않고, 먼저 report/state reconstruction을 수행합니다.
