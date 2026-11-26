# -*- coding: utf-8 -*-
"""
4-page A4 Technical Audit Data (Cold Practitioner Perspective) for:
- 8. 삼성AXI 심화2 최종프로젝트 (개선 · 4팀)
  1) SafePredict 3D 개선안 (신상아)
  2) 예지보전 시스템 AS-IS / TO-BE 개선안 (김지선)
  3) 팀 미리막음 피드백 반영 인프라 개선안 (구명회, 김윤준, 남유진, 백선병, 이인애)
  4) 배차의 민족 최종 개선안 (오주원, 방호원, 김지선, 신상아)
"""

AXI_ADV2_IMPROVED_PLANS = [
    {
        "out_pdf": "axi2_imp_01_SafePredict3D_개선안_신상아_피드백.pdf",
        "course_label": "삼성AXI 심화2 최종프로젝트 (개선) | 실무자 기술 감사 보고서",
        "title": "SafePredict-3D 피드백 개선안 (신상아)",
        "subtitle": "실무 엔지니어링 냉철 감사 · 타깃-원가 모순·랙 충돌 배제·미구현 초안·코어 결함 미조치 진단",
        "authors": "신상아",
        "file_count": "1개 (개선안 PDF 3p)",
        "review_date": "2026년 11월 26일",
        "grade_label": "FAIR / NEEDS WORK (B)",
        "score": 74,
        "sub_scores": [
            ("1. 랙 배치 데이터 외부화(layouts/*.json) 설계", 84),
            ("2. 타깃 고객(중소 현장) vs RTLS/LiDAR 원가 정합성", 64),
            ("3. 랙 충돌/NLOS 차폐·지게차 운전자 안전 반영도", 68),
            ("4. 기존 v1 핵심 결함(CTRV·FPR·.pt고정) 해결 여부", 66),
            ("5. 코드 구현 완료도 vs 계획 초안(Draft) 수준", 76),
        ],
        "exec_badge": "실무 감사 B (74점)",
        "strength_title": "Q&A 3대 지적을 직관적으로 구조화하고 SCENARIO_RACKS 외부화·동적 GridHelper 계획을 명확히 수립",
        "strength_body": "발표 직후 제기된 '물류센터 렌더링/다현장 확장/타깃 고객' 질문을 3페이지 안에 군더더기 없이 정리했습니다. app.py에 하드코딩된 SCENARIO_RACKS·SCENARIO_VIEW를 layouts/*.json으로 분리하고 floor 크기에 맞춰 Three.js GridHelper(30)와 카메라 최대거리(40)를 동적화하며, CAD(ezdxf)·WMS CSV·LiDAR·레이저 실측을 단일 스키마 [cx, cy, lx, ly]로 정규화한 설계 방향은 실무적으로 타당합니다.",
        "defect_title": "중소 현장 타깃-도입비 모순(Unit Economics 붕괴) · 랙/차폐 배제 · v1 코어 결함(직진열화·FPR) 전원 미해결",
        "defect_body": "3번에서 '분리 투자가 어려운 중소 물류창고·제조 현장'으로 고객을 좁혀놓고, 1~2번에서는 여전히 10Hz 실시간 RTLS/UWB 인프라(수천만 원대 구축·유지비)와 CAD·LiDAR 스캔을 전제해 단가 모순이 발생합니다. 또한 랙을 '시각화 전용(충돌·운전자 보호 제외)'으로 못 박아 사각지대 랙 충돌과 금속 랙의 UWB 차폐(NLOS)라는 핵심 현장 리스크를 배제했고, 모든 코드 변경은 미구현 '초안'이며 v1의 직진 +21.7% 열화·CTRV 미비교·FPR 부재·가중치 미저장은 전혀 다뤄지지 않았습니다.",
        "files_table": [
            ("SafePredict-3D_개선안_신상아.pdf", "PDF (개선안 3p)", "보완 필수 (B)", "layouts/*.json 설계는 합리적이나 미구현 초안이며 타깃-원가 모순 및 v1 핵심 결함 미조치"),
        ],
        "tech_sec_title": "2. 타깃 시장 정합성 · 랙 물리 모델링 및 구현 진척도 정밀 감사",
        "tech_blocks": [
            {
                "heading": "📌 [냉철한 실무 검증] 개선안 3개 항목의 현실 타당성 분석",
                "badge": "사업·기술 괴리",
                "badge_cls": "pill-red",
                "table": (
                    ["개선 항목", "개선안 제안 내용", "실무자 냉정 평가 (Blind Spot)", "현업 적용 조건"],
                    [
                        ["1. 실제 센터 렌더링", "CAD/LiDAR/실측 → JSON, 랙은 시각화만", "랙을 충돌·차폐 계산에서 빼면 랙 충돌·NLOS 오차가 그대로 누락됨", "랙 AABB 충돌 + NLOS 감쇠존 모델링"],
                        ["2. 다현장 확장", "layouts/*.json 신설·GridHelper 동적화(초안)", "코드 5단계 모두 미구현 문서 상태이며 스키마 검증·테스트 부재", "JSON Schema + pytest 즉시 PR 머지"],
                        ["3. 타깃 고객 재정의", "대형(쿠팡) 제외 → 중소 물류·제조 현장", "분리 투자도 못 하는 중소 현장에 UWB RTLS+LiDAR 도입은 비현실적", "단안 CCTV/저가 비콘 기반 ROI 재산정"],
                        ["v1 코어 결함", "언급 없음 (직진+21.7%·FPR·.pt·파일폴링)", "발표서 10p에서 자인한 핵심 기술 결함 4건이 개선안에서 통째로 실종", "CTRV 벤치마크·히스테리시스 동시 착수"],
                    ],
                ),
            },
            {
                "heading": "📌 [엔지니어링 핵심 지적] '문서상 개선안'을 '코드 증명'으로 전환해야 할 시점",
                "badge": "실행력 보완",
                "badge_cls": "pill-amber",
                "bullets": [
                    "<strong>중소 현장 TCO 역전 문제:</strong> 중소 창고는 전담 CAD/WMS 데이터조차 없는 경우가 많아 레이저 실측에 의존해야 하는데, 지게차 1~3대 현장에 10Hz RTLS 앵커+태그를 까는 비용은 물리적 라바콘/반사경·저가 근접센서 대비 ROI가 나오지 않습니다. 기존 CCTV RTSP 기반 비전+경량 추적 전환 등 원가 구조를 명시해야 합니다.",
                    "<strong>코너 사각지대의 본질은 '랙'입니다:</strong> 랙을 단순 배경 박스로 취급하면 지게차-랙 충돌(현장 빈발 사고)뿐 아니라 랙 뒤 작업자의 센서 가시선(LOS) 차단까지 무시됩니다.",
                ],
            },
        ],
        "fix_table": [
            ("고객·기술 정합성", "저예산 중소 창고 타깃에 고가 RTLS+LiDAR 파이프라인 전제", "소규모 현장용 저비용 센서(기존 CCTV/BLE AoA) BOM·구축 단가표 수립"),
            ("랙 물리 모델링", "랙을 화면 출력 전용으로 제한해 충돌·NLOS 사각지대 누락", "layouts/*.json 랙 좌표에 AABB 충돌판정 및 NLOS 노이즈 존 가중치 연동"),
            ("미구현 초안 해소", "layouts/·load_layout()·동적 GridHelper가 계획 표에만 존재", "실제 코드 반영 후 대면적(80×50m) 레이아웃 포함 pytest 케이스 추가"),
            ("v1 결함 종결", "직진 +21.7% 열화, CTRV 미비교, FPR, .pt 영속화 누락", "2차 개선안에는 반드시 CTRV 대비 벤치마크와 FPR 측정 결과 포함"),
        ],
        "fixes_code": [
            ("🔧 [Fix 1] layouts/*.json 랙 스키마에 충돌·차폐 속성 통합 + Pydantic 검증",
             "class RackSpec(BaseModel):  # [cx, cy, lx, ly] + 높이/차폐 계수로 충돌·NLOS 동시 반영\n    cx: float; cy: float; lx: float = Field(gt=0); ly: float = Field(gt=0)\n    nlos_sigma_m: float = 0.45  # 철제 랙 인접 시 RTLS 위치 오차 가중"),
            ("🔧 [Fix 2] 중소 현장 ROI 비교 기준 명확화 (RTLS vs 기존 CCTV 비전 트래킹)",
             "# 도입비 기준: RTLS 앵커·태그(약 1,500~3,000만 원) vs 기존 CCTV RTSP + Edge GPU(약 300만 원)\n# 타깃 현장의 지게차 대수·통로 폭·예산 상한을 기획서 앞단에 명문화할 것"),
        ],
        "strategies": [
            ("💰 1. 중소 현장 Unit Economics(도입 원가표) 먼저 계산하기", "사업 타당성", "pill-red", "센서 하드웨어·설치비·유지비를 포함한 1개 창고당 견적을 내야 고객 정의가 설득력을 얻습니다."),
            ("🧱 2. 랙을 충돌·차폐 객체로 승격", "안전 현실성", "pill-amber", "화면 배경이 아니라 랙 충돌 경보와 랙 뒤 NLOS 위치 불확실성 확장에 `racks` 데이터를 바로 쓰세요."),
            ("💻 3. 초안(Draft) 5단계의 실제 PR + 데모 캡처 첨부", "실행 증명", "pill-blue", "계획표 대신 실제 커밋 SHA, 80m 창고 JSON 렌더링 스크린샷, pytest 통과 로그를 제출하세요."),
            ("📉 4. v1 모델·인프라 결함 4종 리매핑", "기술 완결성", "pill-slate", "CTRV 벤치마크, FPR, `.pt` 고정, Redis Streams 전환을 통합 백로그로 묶어 우선순위를 잡으세요."),
        ],
        "checklist": [
            ("사업정합", "중소 현장 기준 센서 BOM·도입비(ROI) 산출", "RTLS vs 저가 센서/CCTV 원가 비교표 작성", "수정 필수", "pill-red"),
            ("구현완료", "layouts/*.json + load_layout() + 동적 GridHelper", "초안 5단계 실제 코드 반영 및 80m 현장 테스트", "수정 필수", "pill-red"),
            ("물리/안전", "랙 충돌 및 NLOS 오차 반경 반영", "작업자·운전자·랙 3자 충돌 및 FPR 정량 측정", "검증 필요", "pill-amber"),
            ("v1후속", "CTRV 베이스라인·.pt 고정·히스테리시스 통합", "직진 +21.7% 열화 및 경보 떨림 해소 확인", "수정 필수", "pill-red"),
        ],
    },
    {
        "out_pdf": "axi2_imp_02_SmartFactory_PdM_개선안_김지선_피드백.pdf",
        "course_label": "삼성AXI 심화2 최종프로젝트 (개선) | 실무자 기술 감사 보고서",
        "title": "예지보전 시스템 아키텍처 개선안 AS-IS vs TO-BE (김지선)",
        "subtitle": "실무 엔지니어링 냉철 감사 · 단일스트림 이종모델 도메인 시프트·로컬 Qwen3 벤치마크 부재 진단",
        "authors": "김지선",
        "file_count": "1개 (개선안 PDF 3p)",
        "review_date": "2026년 11월 26일",
        "grade_label": "GOOD (B+)",
        "score": 84,
        "sub_scores": [
            ("1. 폐쇄망 보안 전환(Gemini → Qwen3·Ollama/vLLM)", 90),
            ("2. 비동기 Kafka(factory.alerts) 워커 분리 설계", 88),
            ("3. 가상 PLC+DAQ 단일 스트림 현실성·도메인 정합", 76),
            ("4. CPU 환경 Qwen3-8B 추론 지연·RAG 검증 수치", 78),
            ("5. 아키텍처 실무 구현 진척도 & 문서 완성도", 84),
        ],
        "exec_badge": "실무 감사 B+ (84점)",
        "strength_title": "제조 폐쇄망(On-Premise) 보안 요구와 비동기 알림 워커 분리를 정확히 짚어낸 현실적 TO-BE 설계",
        "strength_body": "내부 설비 매뉴얼과 알림 이력을 퍼블릭 클라우드(Gemini API)로 보내는 기존 한계를 직시하고, OpenAI 호환 인터페이스로 Ollama/vLLM 기반 Qwen3(32B/8B)·Qwen3-Embedding(4B/0.6B) 온프레미스 전환과 pgvector 확장 경로를 잡은 판단이 정확합니다. 로컬 LLM 생성 지연이 실시간 진동 경보를 막지 않도록 Kafka(factory.alerts) 독립 워커로 비동기 분리한 점도 실무 감각이 뛰어납니다.",
        "defect_title": "이종 3개 모델(CWRU·IMS·C-MAPSS)의 단일 스트림 통합 전제 오류 & 로컬 LLM 실측 벤치마크 전무",
        "defect_body": "가장 치명적인 설계 맹점은 '가상 진동센서 단일 Kafka 토픽 → 공통 전처리 → 결함분류·이상감지·RUL 3개 모델 동시 입력' 구조입니다. CWRU(12~48kHz 베어링 진동), IMS(20kHz 베어링), C-MAPSS(터보팬 엔진 21종 저주파 열/압력 센서)는 물리 단위·샘플링 주파수·열화 물리 자체가 완전히 다릅니다. 또한 일반 PC CPU 환경의 4-bit Qwen3-8B tok/s·TTFT·RAG 정확도 실측치와 알림 폭주(Alarm Storm) 시 큐 적체 대응이 빠져 있고, 오탈자(DQA·겸함·클라우스·메뉴얼)가 다수 남아 있습니다.",
        "files_table": [
            ("예지보전_시스템_개선안_ASIS_TOBE_김지선.pdf", "PDF (개선안 3p)", "양호·보완 (B+)", "폐쇄망 Qwen3·비동기 워커 설계 우수. 이종 센서 스키마·CPU 실측·오탈자 보완 필요"),
        ],
        "tech_sec_title": "2. 단일 스트림 도메인 정합성 및 온프레미스 LLM 운영 병목 정밀 감사",
        "tech_blocks": [
            {
                "heading": "📌 [아키텍처 현실 검증] AS-IS → TO-BE 전환의 타당성 vs 숨은 함정",
                "badge": "설계 감사",
                "badge_cls": "pill-amber",
                "table": (
                    ["영역", "TO-BE 개선안 설계", "실무자 냉정 평가 (Risk)", "현업 보완 조치"],
                    [
                        ["센서 스트림", "가상 PLC+DAQ → 단일 Kafka 토픽 → 공통 전처리", "진동(20kHz) 1종으로 저주파 21채널 C-MAPSS RUL 추론 불가", "모달리티별 토픽/스키마 라우팅 분리"],
                        ["도메인 시프트", "합성/시뮬레이션 진동 → 기존 CWRU·IMS 모델 입력", "공진 대역·노이즈 플로어 불일치 시 3σ 이상감지 오탐 폭증", "Z-score 재보정 + 도메인 적응 검증"],
                        ["로컬 LLM", "Qwen3-8B(4-bit) / 0.6B 임베딩 (CPU/RAM)", "CPU에서 8B + 컨텍스트 생성은 수십 초 소요 · 실측 tok/s 없음", "실측 지연·RAM 점유·RAG Recall@k 제시"],
                        ["알림 큐", "Kafka(factory.alerts) 비동기 SOP 생성", "100대 설비 동시 경보 시 워커 병목으로 수십 분 지연 우려", "설비×결함유형 중복제거(Dedup) + TTL"],
                    ],
                ),
            },
            {
                "heading": "📌 [문서·엔지니어링 품질 점검] 실무 제출 전 즉시 교정할 3가지",
                "badge": "품질 게이트",
                "badge_cls": "pill-blue",
                "bullets": [
                    "<strong>이종 모델 강제 통합 지양:</strong> 단일 진동 스트림에는 '결함분류(FFT/Hilbert) + 이상감지(AE)'만 연결하고, RUL은 운전 사이클·온도/압력(PLC 레지스터)을 결합한 멀티모달 토픽으로 분리해야 물리적 타당성이 성립합니다.",
                    "<strong>CPU 로컬 LLM 실측 근거 필수:</strong> '수 초 지연'이라는 추정 대신, 실제 목표 PC에서 `Qwen3-8B-Q4`로 매뉴얼 3청크(1,500토큰) 입력 시 TTFT·총 생성시간·최대 RSS 메모리와 환각(Hallucination) 검증 결과를 표로 제시해야 합니다.",
                    "<strong>문서 오탈자 교정:</strong> 1p `DQA 시뮬레이터`→`DAQ 시뮬레이터`, `겸함 분류`→`결함 분류`, 3p `클라우스 서버`→`클라우드 서버`, `메뉴얼`→`매뉴얼` 등 엔터프라이즈 제안서 신뢰도를 깎는 오탈자를 일괄 수정하세요.",
                ],
            },
        ],
        "fix_table": [
            ("스트림 스키마", "단일 진동 스트림으로 진동(CWRU/IMS)과 비진동(C-MAPSS) 동시 추론 가정", "고주파 진동 토픽(`telemetry.vib`)과 저주파 공정/운전 토픽(`telemetry.proc`)으로 분리"),
            ("로컬 LLM 실측", "CPU 환경 Qwen3-8B 지연·메모리·정확도 실측 부재", "Ollama/llama.cpp 기준 tok/s, RAM, 응답시간 p95 및 JSON 스키마 준수율 벤치마크 추가"),
            ("알람 폭주 방지", "factory.alerts 워커의 중복 경보 폭주(Alarm Storm) 제어 없음", "동일 설비 10분 쿨다운·중복 키 머지 및 실패 시 규칙 기반 SOP 폴백 SLA(30s) 설정"),
            ("문서 오탈자", "DQA, 겸함, 클라우스, 메뉴얼 등 표기 오류 4건 이상 잔존", "전문 용어 및 한글 맞춤법 교정 후 PoC 실측 장표 1p 추가"),
        ],
        "fixes_code": [
            ("🔧 [Fix 1] 모달리티 분리형 Edge Collector 라우팅 & 설비별 기준선 보정",
             "if payload['modality'] == 'vibration_20khz':\n    producer.send('telemetry.vib', key=machine_id, value=fft_features)\nelif payload['modality'] == 'plc_1hz':\n    producer.send('telemetry.proc', key=machine_id, value=sensor_21ch)"),
            ("🔧 [Fix 2] SOP 에이전트 알람 폭주 디듀플리케이션 + 타임아웃 폴백",
             "dedup_key = f'sop:{machine_id}:{fault_code}'\nif redis.set(dedup_key, 1, nx=True, ex=600):  # 10분 내 동일 설비·결함 LLM 중복 호출 차단\n    sop = call_local_qwen(ctx, timeout=15.0) or rule_based_sop(fault_code)"),
        ],
        "strategies": [
            ("🔌 1. 1개라도 실제 Ollama/Qwen3 로컬 PoC 로그 확보", "실증 우선", "pill-green", "설계도에 그치지 말고 로컬 PC에서 `factory.alerts` 컨슈머가 Qwen3-8B로 SOP를 뱉는 실측 지연(초)을 첨부하세요."),
            ("🧭 2. 진동(베어링) vs 공정(터빈) 파이프라인 물리적 분리", "도메인 정합", "pill-blue", "물리량이 다른 데이터셋을 억지로 한 스트림에 묶지 않는 것이 엔지니어의 신뢰를 높입니다."),
            ("🛡️ 3. JSON Schema 강제 + 근거 청크 인용(Citation) 검증", "환각 통제", "pill-amber", "폐쇄망 경량 모델(8B Q4)은 수치 환각이 잦으므로 매뉴얼 페이지 번호 인용과 Pydantic 검증을 강제하세요."),
            ("📝 4. 오탈자 0건 문서 교정 및 pgvector 마이그레이션 기준 명기", "완성도", "pill-slate", "매뉴얼 1,000건 이상 전환 시 numpy→TimescaleDB pgvector HNSW 전환 임계점을 명시하세요."),
        ],
        "checklist": [
            ("도메인분리", "고주파 진동 vs 저주파 공정 토픽 및 전처리 분리", "CWRU/IMS/C-MAPSS 물리 단위·샘플링 불일치 해소", "수정 필수", "pill-red"),
            ("성능실측", "로컬 PC Qwen3-8B-Q4 tok/s · RAM · RAG Recall 측정", "알람 폭주 시 워커 적체 및 15s 타임아웃 폴백 검증", "검증 필요", "pill-amber"),
            ("문서품질", "DQA·겸함·클라우스·메뉴얼 오탈자 일괄 교정", "엔터프라이즈 제안서 기준 용어 통일", "수정 필수", "pill-amber"),
            ("보안/비동기", "폐쇄망 Qwen3 + Kafka(factory.alerts) 비동기 분리", "외부 API 유출 0건 및 실시간 경보 블로킹 차단 설계", "완료 확인", "pill-green"),
        ],
    },
    {
        "out_pdf": "axi2_imp_03_미리막음_개선안_피드백.pdf",
        "course_label": "삼성AXI 심화2 최종프로젝트 (개선) | 실무자 기술 감사 보고서",
        "title": "미리막음: 기업 첨부파일 검사 인프라 개선안 (구명회·김윤준·남유진·백선병·이인애)",
        "subtitle": "실무 엔지니어링 냉철 감사 · 코드 병목 정확 진단 vs 피크 부하·AWS 베어메탈 TCO·실측 검증 과제",
        "authors": "미리막음 (구명회, 김윤준, 남유진, 백선병, 이인애)",
        "file_count": "1개 (개선안 PDF 4p)",
        "review_date": "2026년 11월 26일",
        "grade_label": "EXCELLENT (A-)",
        "score": 89,
        "sub_scores": [
            ("1. 코드 병목 진단(CAPE 동기블로킹·캐시 미연결) 정확도", 94),
            ("2. S3·SQS·RDS Multi-AZ·멱등성/캐시 아키텍처", 92),
            ("3. 완료기준(DoD) · 실패 안전(Fail-Closed 보류) 원칙", 91),
            ("4. 피크 트래픽(출근시간) 용량 산정 & AWS 베어메탈 TCO", 81),
            ("5. 실측 부하/장애복구 실행 로그 확보 여부 (설계단계)", 83),
        ],
        "exec_badge": "실무 감사 A- (89점)",
        "strength_title": "4팀 개선안 중 유일하게 실제 코드 병목·RDS 상태 복구·Singleflight·DoD·용어집까지 현업 RFP 수준으로 정리",
        "strength_body": "기존 게이트웨이가 CAPE 제출 후 보고서까지 동기 대기해 게스트 슬롯을 놀리는 문제와, 존재하는 정적 캐시 코드를 통합 워커가 호출하지 않던 실수를 정확히 짚어냈습니다. S3+SQS+DLQ 비동기 분리, CAPE 제출/회수 디커플링, RDS PostgreSQL Multi-AZ 기반 재시작 복구, '같은 회사(테넌트) 내 SHA-256 + 검사버전·정책 일치' 조건부 캐시와 동시 중복요청 병합, 그리고 '미검사 파일 공개 0건·실패 시 보류' 원칙까지 실무 시큐리티 엔지니어 수준입니다.",
        "defect_title": "24시간 평균 기준 133슬롯 과소산정(피크 3~5배 누락) · AWS 베어메탈 KVM 비용(TCO) 외면 · 실측 로그 미첨부",
        "defect_body": "2쪽의 '하루 2만 건 × 400초 ÷ (86,400초 × 70%) ≈ 133슬롯' 계산은 24시간 균등 유입을 가정한 치명적 함정입니다. 기업 메일은 09~11시·14~16시에 하루 트래픽의 60~70%가 몰리므로 피크 기준 ~400슬롯이 필요하거나 우선순위 큐·SLA 분리가 없으면 오전 중 수십 분~수 시간 적체가 발생합니다. 또한 AWS 일반 EC2는 중첩 가상화(KVM)를 지원하지 않아 고가의 Bare Metal 인스턴스(`c7i.metal` 등) + Windows 라이선스 비용(월 수천만 원대)과 스냅샷 복원 IOPS 병목에 대한 경제성 검토가 빠졌고, 아직 실측 검증은 미실행 상태입니다.",
        "files_table": [
            ("팀 미리막음_피드백반영_개선안_구명회,김윤준,남유진,백선병,이인애.pdf", "PDF (개선안 4p)", "우수 (A-)", "아키텍처·캐시·DoD 완성도 최상. 피크 용량(3~5x)·베어메탈 TCO·실행 로그 보강 필요"),
        ],
        "tech_sec_title": "2. 분산 CAPE 파이프라인 · 피크 용량 산정 및 클라우드 TCO 정밀 감사",
        "tech_blocks": [
            {
                "heading": "📌 [실무 아키텍처 심층 감사] 설계 정합성 vs 운영 현실 장벽",
                "badge": "운영 검증 과제",
                "badge_cls": "pill-amber",
                "table": (
                    ["설계 영역", "개선안 제시 구조", "실무자 냉정 평가 (Gap)", "실운영 검증 포인트"],
                    [
                        ["용량 산정", "일 100만×2%×400s / (86,400×0.7) = 133슬롯", "출근 피크(3~5×) 미반영 · 400s 점유 시 오전 큐 지연 폭증", "피크 TPS 기준 슬롯/오토스케일 재산정"],
                        ["KVM 인프라", "전용 EC2 + KVM + CAPEv2 + Win 게스트", "EC2 중첩가상화 불가 → Bare Metal(`.metal`) + Win CAL 비용", "호스트당 적정 슬롯 수 및 월 TCO 산출"],
                        ["상태·캐시", "RDS Multi-AZ + 테넌트·정책·버전별 SHA-256 캐시", "동시 중복 병합·테넌트 격리 기준 모두 정확. TTL·무효화 규칙만 추가", "YARA/룰 업데이트 시 부분 재스캔 정책"],
                        ["증빙 상태", "정적 avg 4.6s / Excel CAPE ~400s (기존 수치)", "제출/회수 분리 후 2슬롯 겹침 로그·워커 킬 복구 테스트 미실행", "3쪽 DoD 3종 실측 로그 첨부"],
                    ],
                ),
            },
            {
                "heading": "📌 [현업 보안·인프라 리뷰] 기업 메일 게이트웨이 관점의 날카로운 체크포인트",
                "badge": "현업 기준 A-",
                "badge_cls": "pill-green",
                "bullets": [
                    "<strong>400초 동적 분석과 메일 SLA 충돌:</strong> 일반 기업 메일 사용자는 첨부 400초(6.7분) 대기를 견디지 못합니다. 본문 선전송 후 첨부 링크 치환(CDR/지연 다운로드) 또는 고위험 확장자·매크로 우선 큐(Fast Lane) 분리를 운영 정책에 명시해야 B2B 계약이 성사됩니다.",
                    "<strong>EBS/NVMe 스냅샷 복원 병목:</strong> 한 베어메탈 호스트에 Windows VM 8~16슬롯을 띄울 때 분석 종료 후 스냅샷 동시 롤백(Restore)이 발생하면 디스크 IOPS가 포화됩니다. 오버레이 qcow2 backing file + RAMDisk(`tmpfs`) 기반 복원 시간 실측이 필수입니다.",
                ],
            },
        ],
        "fix_table": [
            ("피크 용량 재산정", "24h 균등 가정(133슬롯)으로 오전 업무 피크 시 큐 대기시간 급증 위험", "피크 3.5배 기준 용량표 + '우선순위 큐(실시간 메일 vs 배치)' SLA 분리 설계 추가"),
            ("AWS 베어메탈 TCO", "`.metal` 인스턴스 단가, Windows 라이선스, NVMe qcow2 복원 병목 미산출", "호스트 스펙별(예: c7i.metal-24xl) 수용 슬롯 수·건당 원가(Unit Cost) 표기"),
            ("메일 UX 지연 해소", "400초 동적 검사 동안 메일 수신이 멈추면 현업 민원 폭주", "안전 본문 선배달 + 첨부 보류 링크(준비 완료 시 해제) 비동기 UX 정책 명기"),
            ("DoD 실증 완료", "제출·회수 분리 및 워커 킬 복구가 아직 계획 상태", "CAPE 2슬롯 동시 실행 타임스탬프 로그와 SIGKILL 복구 1회 실측 증빙 첨부"),
        ],
        "fixes_code": [
            ("🔧 [Fix 1] 피크 3.5배 반영 슬롯 계산 & 정적/동적 타임아웃 예산(Budget)",
             "peak_jobs_per_hour = (1_000_000 * 0.02 / 24) * 3.5   # ≈ 2,917건/시 (오전 피크)\nslots_needed = ceil((peak_jobs_per_hour * 400) / (3600 * 0.75))  # ≈ 432 슬롯 (또는 우선순위 큐+동적타임아웃 180s 단축)"),
            ("🔧 [Fix 2] Outbox + Lease 기반 워커 킬 무유실 복구 (RDS + SQS)",
             "UPDATE scan_jobs SET status='RUNNING', lease_until=NOW()+INTERVAL '120s' WHERE job_id=:id AND status='QUEUED';\n# 워커 SIGKILL 시 VisibilityTimeout 만료 후 재수신 → cape_task_id가 존재하면 재제출 대신 결과 폴링으로 복구"),
        ],
        "strategies": [
            ("📈 1. 피크 타임 용량 & 동적 분석 시간 단축(400s→120s) 레버 제시", "B2B 세일즈", "pill-green", "400초 고정이 아니라 악성 행위 조기 확정 시 VM 즉시 종료(Early Exit)로 슬롯 비용을 절반 이하로 줄이세요."),
            ("💵 2. Bare Metal(`c7i.metal`) 기반 건당 분석 원가(Unit Cost) 계산", "경제성", "pill-blue", "월 인프라 비용을 일 100만 건으로 나눈 '메일 1건당 보안 원가'를 제시하면 기업 CTO가 바로 반응합니다."),
            ("🧪 3. 2슬롯 병렬 겹침 + SIGKILL 카오스 테스트 로그 실측", "DoD 달성", "pill-amber", "3쪽에 적은 개발 완료 기준(중복접수·겹침로그·워커복구)을 실제 AWS/로컬 KVM에서 1회 돌린 로그를 붙이세요."),
            ("✉️ 4. CDR(무해화) 또는 지연 링크 UX로 400초 대기 체감 제거", "현업 UX", "pill-slate", "정적 검사 통과+매크로 무해화 본문을 먼저 전달하고 동적 판정 완료 시 원본을 푸는 운영안을 결합하세요."),
        ],
        "checklist": [
            ("피크/TCO", "피크 3~5배 슬롯 산정 & AWS `.metal` 원가 계산", "균등 133슬롯의 오전 병목 해소 및 건당 단가 확보", "수정 필수", "pill-amber"),
            ("실측증빙", "CAPE 2슬롯 실행시간 겹침 로그 & 워커 강제종료 복구", "3쪽 DoD 3개 항목 실제 테스트 로그 확보", "검증 필요", "pill-amber"),
            ("메일SLA", "400s 동적 대기 시 메일 선전달/조기종료 정책", "Early-Exit·우선순위 큐로 실무 체감 지연 축소", "보완 권고", "pill-blue"),
            ("설계품질", "코드 병목 진단·S3/SQS/RDS·테넌트 캐시·Fail-Closed", "4팀 개선안 중 아키텍처·보안·용어 정의 최상위 수준", "완료 확인", "pill-green"),
        ],
    },
    {
        "out_pdf": "axi2_imp_04_배차의민족_개선안_피드백.pdf",
        "course_label": "삼성AXI 심화2 최종프로젝트 (개선) | 실무자 기술 감사 보고서",
        "title": "배차의 민족 최종 발표 개선안 (오주원·방호원·김지선·신상아)",
        "subtitle": "실무 엔지니어링 냉철 감사 · '학습 계획서' vs '기술 증빙' 간극 및 논리적 FK·보안 취약점 진단",
        "authors": "배차의 민족 (오주원, 방호원, 김지선, 신상아)",
        "file_count": "1개 (개선안 PDF 11p)",
        "review_date": "2026년 11월 26일",
        "grade_label": "GOOD (B+)",
        "score": 80,
        "sub_scores": [
            ("1. 별첨 1·2(Phase 0~8 아키텍처·10테이블 ERD) 투명성", 88),
            ("2. Q&A 5대 약점 자가 진단 정직성 (2-1~2-5)", 85),
            ("3. 알고리즘·평가(비용행렬·ROC-AUC 실수치) 기술 깊이", 72),
            ("4. DB 무결성(논리적 FK)·인증 토큰 보안 설계", 73),
            ("5. '학습 의지 선언' 대신 실제 코드/실험 개선 반영도", 78),
        ],
        "exec_badge": "실무 감사 B+ (80점)",
        "strength_title": "Phase 0~8 풀스택 구조도와 실제 backend/models 기반 10테이블 ERD(행 수 실측 포함) 정리는 투명하고 우수",
        "strength_body": "11페이지에 달하는 분량 중 별첨 1(Phase 0~8 계층·데이터 흐름도)과 별첨 2(PostgreSQL 17 + PostGIS 3.5 ERD 및 2026-11-25 기준 실데이터 행 수 USERS 5·DRIVERS 18·ORDERS 26·AUDIT_LOGS 117)를 실제 코드와 대조해 투명하게 공개한 점이 돋보입니다. 발표 Q&A에서 답하지 못한 5대 영역(아키텍처 데이터 흐름, 헝가리안, 분류 평가지표, PostGIS, DB 연동)을 회피하지 않고 정확히 목록화했습니다.",
        "defect_title": "전체가 '개선 결과'가 아닌 '추가 학습 계획서'(~하고자 한다) · DB 외래키 미제약(논리적 FK) · 토큰/JSONB 보안 허점",
        "defect_body": "개선안 본문(2-1~2-5절)이 '원리를 추가로 학습하고 정리하고자 한다', '구체화할 계획이다'라는 미래형 학습 다짐으로 채워져 있을 뿐, 실제 헝가리안 비용행렬 수식(C_ij)·불균형(M≠N) 더미 처리·LightGBM 임계값(0.75)에서의 실측 ROC-AUC/PR-AUC/혼동행렬은 1건도 제시되지 않았습니다. 또한 별첨 2에 스스로 적시한 'FK는 DB 제약 조건 없이 코드 참조(논리적 FK)', 비밀번호 해시의 JSONB 혼재, AUTH_TOKENS 만료/폐기 컬럼 부재, 여전히 남아있는 Mock cf_score와 소규모 표본(26건) 기반 P95 0.0309s 외삽은 현업 DB/백엔드 리뷰에서 즉시 반려될 결함입니다.",
        "files_table": [
            ("최종 개선안_배차의 민족_오주원, 방호원, 김지선, 신상아.pdf", "PDF (개선안 11p)", "개선 필요 (B+)", "별첨 아키텍처·ERD는 우수하나 본문이 학습계획 수준이며 DB FK 미제약·실수치 부재"),
        ],
        "tech_sec_title": "2. 백엔드·DB 무결성 및 매칭 알고리즘 증빙 수준 정밀 감사",
        "tech_blocks": [
            {
                "heading": "📌 [냉철한 백엔드·DB 감사] 별첨 2 ERD와 본문 2-1~2-5절에서 드러난 기술 결함",
                "badge": "DB·알고리즘 보완",
                "badge_cls": "pill-red",
                "table": (
                    ["감사 영역", "개선안 현황 (11p 기준)", "실무자 냉정 평가 (Defect)", "필수 교정 수준"],
                    [
                        ["DB 무결성", "10테이블 모두 '논리적 FK' (DB 제약 없음)", "동시 배차·삭제 시 고아 레코드(Orphan) 및 정산 불일치 발생", "Alembic 마이그레이션으로 물리 FK 강제"],
                        ["인증·보안", "비번 해시 JSONB 저장 · AUTH_TOKENS 만료 부재", "타입 검증 불가 및 탈취 토큰 무효화(Revoke)·만료 TTL 불가", "전용 컬럼 + expires_at/revoked_at + 해시"],
                        ["매칭 수식", "헝가리안·분류지표 '추가 학습 계획'만 서술", "비용행렬 가중치식(C_ij)·LightGBM 실측 PR-AUC·FPR 0건", "수식 + 임계값별 Precision/Recall 표 첨부"],
                        ["성능 외삽", "ORDERS 26행·DRIVERS 18행 + Mock cf_score", "26건 DB 기준 P95 0.0309s는 인덱스/풀 부하 검증 불인정", "1만 기사·1,000주문 부하 + GIST 인덱스 검증"],
                    ],
                ),
            },
            {
                "heading": "📌 [작성 태도 및 문서 완성도 지적] '다짐형 문장'을 '근거 데이터'로 치환해야 함",
                "badge": "품질 개선",
                "badge_cls": "pill-amber",
                "bullets": [
                    "<strong>'학습하고자 한다' 반복의 역효과:</strong> 기술 개선안은 학생의 공부 계획표가 아니라 리뷰어가 요구한 증거 제출서입니다. 'Precision과 ROC-AUC의 차이를 이해하고자 한다' 대신 실제 프로젝트 validation set의 ROC-AUC 값과 임계값 0.75 vs 0.85 비교표를 바로 넣어야 합니다.",
                    "<strong>Idempotency·ACK가 아직 '검토 대상':</strong> 2쪽에서 Redis Streams 중복방지·ACK·재시도를 '향후 검토할 구조'로 미뤘는데, 결제/정산(`SETTLED`)과 연결된 물류 플랫폼에서 중복 이벤트 처리는 선택이 아니라 Phase 3 필수 요건입니다.",
                    "<strong>편집 오탈자:</strong> 2p 하단 `...기반 마련2-2. Hungarian Algorithm...` 줄바꿈 누락 오탈자를 교정하세요.",
                ],
            },
        ],
        "fix_table": [
            ("물리 FK·보안", "논리적 FK(무제약), JSONB 내 비번 해시, AUTH_TOKENS 만료 컬럼 부재", "DB ForeignKey 제약 복원, password_hash 전용 컬럼 분리, token SHA-256+expires_at 추가"),
            ("알고리즘 증빙", "헝가리안 비용행렬·불균형 배정·분류 혼동행렬 없이 개념 학습만 기술", "실제 `C_ij` 수식, 더미 패딩 코드, LightGBM 임계값(0.65/0.75/0.85) Precision·Recall 실측표 첨부"),
            ("부하·공간인덱스", "DRIVERS 18행·ORDERS 26행 환경과 Mock cf_score 잔존", "10,000건 시드 + `CREATE INDEX ... USING GIST(geom)` 적용 후 `EXPLAIN ANALYZE`·P95 재측정"),
            ("문서 문체/오탈자", "'~하고자 한다' 20회 이상 반복 및 2p `마련2-2.` 줄바꿈 오류", "완료형 기술 명세로 전면 개고 및 2p 줄바꿈 오탈자 수정"),
        ],
        "fixes_code": [
            ("🔧 [Fix 1] 논리적 FK 제거 → PostgreSQL 물리 FK + PostGIS GIST 공간 인덱스",
             "ALTER TABLE orders ADD CONSTRAINT fk_orders_driver FOREIGN KEY (driver_id) REFERENCES drivers(id);\nCREATE INDEX idx_drivers_geom_gist ON drivers USING GIST (geom);  -- ST_DWithin 전수 스캔 방지"),
            ("🔧 [Fix 2] 헝가리안 비용행렬(C_ij) & 불균형(M≠N) 더미 패딩 명시",
             "# C[i, j] = w1 * deadhead_km(i, j) - w2 * lgb_score(i, j) + penalty_if_ineligible\n# 주문(M) != 기사(N)일 때 scipy.optimize.linear_sum_assignment는 직사각 행렬을 지원하며 미배정 건은 재큐잉"),
        ],
        "strategies": [
            ("📊 1. '공부 계획' 삭제 → LightGBM 실측 ROC/PR-AUC 표 즉시 삽입", "최우선 수정", "pill-red", "개념 교과서 설명 5페이지를 절반으로 줄이고, 실제 모델 임계값별 오배차율·매칭률 수치를 채우세요."),
            ("🔐 2. DB 물리 FK & AUTH_TOKENS 만료/폐기 스키마 즉시 마이그레이션", "백엔드 무결성", "pill-red", "별첨 2 ERD에 '논리적 FK'라고 적혀 있는 한 시니어 DB 리뷰어를 절대 통과할 수 없습니다."),
            ("⚡ 3. 1만 건 더미 부하 + GIST 인덱스 EXPLAIN ANALYZE 첨부", "성능 입증", "pill-amber", "18명·26건 DB 수치가 아니라 실제 공간 인덱스가 타는 실행계획과 P95 지연을 증명하세요."),
            ("🔁 4. Redis Streams XACK + Consumer Group 재시도(XPENDING) 구현", "안정성", "pill-blue", "향후 검토로 두지 말고 멱등성 키(order_id+ts)와 XACK 처리를 코드로 마무리하세요."),
        ],
        "checklist": [
            ("DB/보안", "물리적 FK 제약 적용 & 비번/토큰 컬럼 분리·만료", "고아 레코드 방지 및 토큰 TTL·폐기 지원", "수정 필수", "pill-red"),
            ("알고리즘", "비용행렬(C_ij) 수식 & 임계값별 Precision/Recall 실측", "'학습 계획' 문장을 실제 실험 결과표로 대체", "수정 필수", "pill-red"),
            ("성능검증", "Mock cf_score 제거 + 1만 건 GIST 인덱스 P95 측정", "26건 소규모 표본 외삽 해소", "검증 필요", "pill-amber"),
            ("아키텍처", "Phase 0~8 구조도 및 10테이블 ERD 현행화", "실제 backend/models 기반 투명한 아키텍처 문서화", "완료 확인", "pill-green"),
        ],
    },
]
