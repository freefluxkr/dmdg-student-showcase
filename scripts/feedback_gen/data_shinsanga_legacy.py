# -*- coding: utf-8 -*-
"""
4-page A4 Technical Audit Data (Cold Practitioner Perspective) for the remaining 4
Shin Sang-ah-involved legacy projects across Stage 1, Mini, and Final Planning:
  1) s1_midterm: Card-FDS-N 중간점검 코드·파이프라인
  2) s1_card_fds: CARD-FDS-N (1차 프로젝트 최종)
  3) m_shinsanga: NASA IMS 기반 베어링 예지보전(PdM)
  4) p_baemin: 배차의 민족 2차 최종 기획서
"""

SHINSANGA_LEGACY_PLANS = [
    {
        "project_id": "s1_midterm",
        "out_pdf": "s1_midterm_Card-FDS-N_중간점검_피드백.pdf",
        "course_label": "DMDG AI·데이터 심화 2기 (1차 중간점검) | 실무자 기술 재감사 보고서",
        "title": "금융 이상거래 탐지 및 알림 서비스 (Card-FDS-N) 중간점검",
        "subtitle": "실무 엔지니어링 냉철 재감사 · 노트북 재현성 붕괴(2/3 실패)·SMOTENC 역설·시간분할 누락 진단",
        "authors": "오주원 · 김지선 · 신상아 · 이인애",
        "file_count": "총 5개 (IPYNB 3건, DOCX 1건, PDF 1건)",
        "review_date": "2026년 11월 26일 (실무 재감사)",
        "grade_label": "FAIR / NEEDS WORK (B)",
        "score": 74,
        "sub_scores": [
            ("1. 누수 차단 분할 & 하이퍼파라미터 튜닝(고도화버전)", 86),
            ("2. 노트북 재현성·실행 무결성 (2/3건 런타임 크래시)", 58),
            ("3. SMOTENC 전후 PR-AUC 검증 해석 타당성", 68),
            ("4. 시간순 분할(Temporal Split) · Velocity 피처 반영", 72),
            ("5. 파이프라인 장표 & 팀 협업 정리", 84),
        ],
        "exec_badge": "실무 재감사 B (74점)",
        "strength_title": "고도화버전(1).ipynb의 Train-only 스케일링 원칙과 16조합 튜닝(Val PR-AUC 0.8073)은 기본기 충족",
        "strength_body": "제출 노트북 중 `고도화버전 (1).ipynb`는 정답 누수 컬럼을 사전에 제거하고 Train 세트에서만 RobustScaler를 적합하는 데이터 누수 차단 원칙을 지켰습니다. 또한 16개 하이퍼파라미터 조합 탐색과 Soft Voting 앙상블(Val PR-AUC 0.8073, Test PR-AUC 0.7820)로 1차 모델링 베이스라인을 확보한 점은 인정됩니다.",
        "defect_title": "제출 노트북 3종 중 2종 실행 크래시 · SMOTENC 적용 시 PR-AUC 하락 역설 오독 · 시간분할/Velocity 피처 부재",
        "defect_body": "실무 코드 리뷰 기준으로 제출된 3개 노트북 중 2개가 `Restart & Run All`조차 통과하지 못한 상태입니다(`card.ipynb` Cell 76 `NameError: X_test_scaled`, `notification_261021.ipynb` Cell 75 `ModuleNotFoundError: gtts` 및 Cell 93 Streamlit 시작 실패). 게다가 브리핑 문서 5쪽 수치상 SMOTENC 적용 시 Test PR-AUC가 오히려 하락(0.7503→0.7426, F1 0.7221→0.7224)했는데도 'SMOTENC가 더 적합하다'고 반대 결론을 내렸으며, 시간순 분할과 카드별 단기 빈도(Velocity) 피처도 빠져 있습니다.",
        "files_table": [
            ("고도화버전 (1).ipynb", "IPYNB (핵심)", "양호 (B+)", "누수 차단·16조합 튜닝·Val PR-AUC 0.8073 확보. 단, 무작위 층화분할 한계"),
            ("card.ipynb", "IPYNB (추론)", "실행 실패 (C)", "Cell 76 `X_test_scaled` NameError 크래시로 서빙 지연시간 근거 소실"),
            ("notification_261021.ipynb", "IPYNB (알림)", "실행 실패 (C)", "셀 역순 실행(`gtts` 미설치) 및 Cell 93 Streamlit RuntimeError 발생"),
            ("카드 거래 이상탐지 브리핑.pdf", "PDF (7p)", "해석 오류 (B)", "SMOTENC 적용 후 PR-AUC 하락 수치를 보고도 SMOTENC 채택 결론"),
        ],
        "tech_sec_title": "2. 제출 노트북 재현성 · SMOTENC 역설 및 FDS 피처 감사",
        "tech_blocks": [
            {
                "heading": "📌 [냉철한 실험·코드 감사] 중간점검 산출물에서 확인된 4대 실무 결함",
                "badge": "PR 반려 사유",
                "badge_cls": "pill-red",
                "table": (
                    ["감사 항목", "브리핑/노트북 실제 상태", "실무자 냉정 평가 (Defect)", "필수 교정 조치"],
                    [
                        ["노트북 실행성", "3개 중 2개(`card`, `notification`) 런타임 에러", "재실행 안 되는 노트북 제출은 현업 코드리뷰 즉시 반려 대상", "제출 전 Kernel Restart & Run All"],
                        ["SMOTENC 역설", "미적용 PR-AUC 0.7503 vs 적용 0.7426 (Test)", "PR-AUC는 떨어졌는데 임계값 0.5 고정 Recall만 보고 우위 오판", "원본 + class_weight + threshold 튜닝"],
                        ["데이터 분할", "Train/Val/Test 무작위 층화분할(Stratified)", "카드 사기는 시간축 드리프트가 핵심 — 미래 거래가 학습에 혼입", "기준일 기준 Time-based Split 전환"],
                        ["피처 엔지니어링", "단건 거래 속성만 사용 (Velocity 0건)", "연속 소액결제·심야 다회 승인 등 FDS 핵심 시계열 패턴 부재", "카드별 10m/1h/24h 롤링 집계 추가"],
                    ],
                ),
            },
            {
                "heading": "📌 [실험 결과 해석 오류 정밀 지적] SMOTENC vs Threshold Tuning",
                "badge": "ML 방법론 교정",
                "badge_cls": "pill-amber",
                "bullets": [
                    "<strong>임계값 0.50의 착시:</strong> LightGBM에서 SMOTENC를 쓰면 양성 사전확률(Prior)이 3.68%→30%로 부풀어 예측 확률 자체가 위로 이동합니다. Threshold 0.50에서 Recall이 0.6339→0.6572로 오른 것은 모델이 좋아져서가 아니라 임계값이 낮아진 효과일 뿐이며, 실제 순수 변별력(PR-AUC)은 0.7503→0.7426으로 하락했습니다.",
                    "<strong>가상 오버샘플링 폐기 권고:</strong> 트리기반 부스팅(LightGBM/XGBoost)에서는 왜곡된 합성 샘플을 만드는 SMOTENC보다 원본 분포에서 `scale_pos_weight`와 비즈니스 비용 기반 임계값(Threshold)을 조정하는 것이 확률 캘리브레이션에 훨씬 유리합니다.",
                ],
            },
        ],
        "fix_table": [
            ("재현성 결함", "`card.ipynb`(NameError) 및 `notification_261021.ipynb`(gtts/Streamlit 에러)", "단일 `requirements.txt` + `Restart & Run All` 무오류 통과 후 Git 커밋"),
            ("오버샘플링 오독", "SMOTENC 적용 시 PR-AUC 하락(0.7503→0.7426)을 무시하고 SMOTENC 채택", "SMOTENC 미적용 원본 + Threshold 0.35~0.55 스윕으로 공정 비교(동일 Recall 기준 Precision)"),
            ("시간 누수 위험", "거래 시계열 순서를 무시한 무작위 층화분할 사용", "과거 70% Train → 직후 10% Val → 최신 20% Out-of-Time Test 분할로 변경"),
            ("Velocity 부재", "건별 단일 행 피처만 존재해 연쇄 이상결제 포착 한계", "카드ID·가맹점별 최근 10분/1시간 거래횟수·누적금액·금액Z점수 파생 추가"),
        ],
        "fixes_code": [
            ("🔧 [Fix 1] 공정 비교 원칙 — SMOTENC vs 원본 + Threshold Calibration (동일 Recall 기준)",
             "p_raw, r_raw, _ = precision_recall_curve(y_val, lgb_raw.predict_proba(X_val)[:, 1])\n# 동일 Recall(예: 0.70)에서 원본 모델과 SMOTENC 모델의 Precision 비교 후 PR-AUC 높은 쪽 채택"),
            ("🔧 [Fix 2] Out-of-Time 분할 + 카드별 단기 Velocity 피처 생성",
             "df = df.sort_values(['card_id', 'tx_ts'])\ndf['tx_cnt_1h'] = df.groupby('card_id').rolling('1h', on='tx_ts')['amount'].count().values"),
        ],
        "strategies": [
            ("🔁 1. 'Restart & Run All' 통과 노트북만 제출하는 PR 규율 확립", "엔지니어링 기본", "pill-red", "실행 순서가 꼬인 셀(`execution_count` 역전)과 전역 상태 의존 코드는 즉시 정리하세요."),
            ("📉 2. SMOTENC 대신 `scale_pos_weight` + Probability Calibration", "모델 정확도", "pill-amber", "Recall을 높이려면 합성 노이즈를 넣기 전에 원본 모델의 threshold를 낮춰 비교부터 하세요."),
            ("⏱️ 3. 단기 빈도(Velocity)·직전 거래 경과시간 피처 반드시 추가", "FDS 본질", "pill-blue", "카드 FDS의 성능 절반 이상은 단건 금액이 아니라 최근 10분~1시간 내 이상 빈도에서 나옵니다."),
            ("📅 4. Out-of-Time 평가셋으로 드리프트 내성 입증", "실전 검증", "pill-green", "무작위 분할 점수가 아니라 미래 시점 거래에 대한 PR-AUC 유지율을 최종 성적표로 제시하세요."),
        ],
        "checklist": [
            ("코드실행", "노트북 3종 `Restart & Run All` 에러 0건 통과", "`card.ipynb` NameError · `notification` gtts/포트 충돌 해결", "수정 필수", "pill-red"),
            ("모델비교", "원본 threshold 조정 vs SMOTENC 동일 Recall 비교", "PR-AUC 하락 원인 규명 및 최적 모델 재선정", "수정 필수", "pill-red"),
            ("피처/분할", "Out-of-Time 분할 + 10m/1h Velocity 피처 반영", "시계열 미래 누수 차단 및 FDS 도메인 피처 보강", "검증 필요", "pill-amber"),
            ("기초체력", "누수 컬럼 제거 · Train-only 스케일링 · 16조합 튜닝", "`고도화버전 (1).ipynb` 파이프라인 원칙 유지", "완료 확인", "pill-green"),
        ],
    },
    {
        "project_id": "s1_card_fds",
        "out_pdf": "s1_card_fds_CARD-FDS-N_피드백.pdf",
        "course_label": "DMDG AI·데이터 심화 2기 (1차 프로젝트 최종) | 실무자 기술 재감사 보고서",
        "title": "CARD-FDS-N (카드 이상거래 탐지 및 알림 서비스)",
        "subtitle": "실무 엔지니어링 냉철 재감사 · 합성데이터(3.68%) 한계·시니어 UX 알람피로·Velocity/규정 부재 진단",
        "authors": "오주원 · 김지선 · 신상아 · 이인애",
        "file_count": "총 3개 (발표 PDF 12p + Updated PDF + URL)",
        "review_date": "2026년 11월 26일 (실무 재감사)",
        "grade_label": "FAIR / NEEDS WORK (B)",
        "score": 77,
        "sub_scores": [
            ("1. 누수 차단·PR-AUC 지표 선정 & FastAPI 서빙", 86),
            ("2. 실금융 데이터 현실성(3.68% 합성 vs 0.05% 실전)", 68),
            ("3. 시계열 분할 & 카드별 Velocity·행동 피처 깊이", 70),
            ("4. 시니어 UX 안전성(주의 TTS 알람피로·인증연계)", 71),
            ("5. 금융 규제(여전법) 감사 추적성 & 문서 정확도", 82),
        ],
        "exec_badge": "실무 재감사 B (77점)",
        "strength_title": "PR-AUC 중심 평가, Train-only SMOTENC 원칙, SHAP+FastAPI(<200ms)까지 기본 파이프라인 구조는 탄탄",
        "strength_body": "불균형 탐지에서 Accuracy 함정을 배제하고 PR-AUC·Minority F1과 Threshold 스윕을 적용했으며, FastAPI 기반 <200ms 추론 목표와 SHAP 상위 근거 출력을 연결했습니다. 취약계층 금융 보호라는 문제 정의와 시각·청각 보조 UI 프로토타입까지 1차 팀 프로젝트로서 완성하려는 노력은 분명합니다.",
        "defect_title": "온실형 합성데이터(사기율 3.68%)·무작위 분할 · 고령자 공포 유발 '주의 TTS 팝업' · Velocity/규정 엔진 부재",
        "defect_body": "AI Hub 합성데이터의 이상비율 3.68%는 실제 카드사(0.01~0.1%) 대비 30~300배 높아 모델 난이도가 비현실적으로 낮고, 적대적 회피(1달러 테스트·스머핑)가 전무하며, Train+Val 통합 후 무작위 층화분할(70/10/20)로 시간 인과성까지 훼손했습니다. 서비스 단에서도 30~55% '주의' 구간에 고령자 대상 대형 팝업·TTS 음성 경고를 띄우면 알람 피로와 금융 공포만 유발합니다. P3 기술표에 존재하지 않는 scikit-learn 함수 `pr_auc_score`를 기재한 오기도 수정해야 합니다.",
        "files_table": [
            ("CARD-FDS-N 프로젝트_Updated.pdf", "PDF (최종 12p)", "보완 필요 (B)", "합성 3.68%·무작위분할·Velocity 부재·주의 TTS 역효과·`pr_auc_score` 오기"),
            ("1차 프로젝트_URL 주소.txt", "TXT (배포/코드)", "양호 (확인)", "FastAPI/Streamlit/GitHub 연동 구성 확인"),
        ],
        "tech_sec_title": "2. 금융권 FDS 실무 기준 정밀 재감사 (데이터·피처·UX·컴플라이언스)",
        "tech_blocks": [
            {
                "heading": "📌 [냉철한 금융 FDS 감사] 상용 카드 FDS 기준과의 4대 핵심 괴리",
                "badge": "현업 갭(Gap)",
                "badge_cls": "pill-red",
                "table": (
                    ["평가 영역", "현재 구현 (Updated.pdf)", "금융권 실무 냉정 평가 (Defect)", "현업 적용 필수 요건"],
                    [
                        ["데이터/분할", "AI Hub 3.68% · 통합 후 무작위 70/10/20", "실제 사기(0.05%) 대비 70배 과잉 · 미래 거래 혼입", "Out-of-Time 분할 + 0.1% 다운샘플 스트레스"],
                        ["핵심 피처", "승인금액·한도·심야 등 단건 정적 피처", "카드별 단기 빈도(10분 내 다중결제)·이동속도(Geo) 부재", "Redis/Feast 온라인 Velocity 피처 서빙"],
                        ["고령자 UX", "30~55% '주의' 시 대형 팝업 + TTS 경고", "오탐 20~30% 구간 TTS 남발 → 알람 피로·실사기 무시", "무마찰(FIDO/ARS 추가인증) 우선 · 85%+만 차단"],
                        ["규제/문서", "SHAP 단독 설명 · `pr_auc_score` 오기(P3)", "금감원 설명의무는 사후 SHAP이 아닌 규칙·사유코드 요구", "Rule Engine 결합 + `average_precision_score`"],
                    ],
                ),
            },
            {
                "heading": "📌 [비용 기반 최적화 부재] F1 최대화가 아니라 기대 손실(Expected Loss) 최소화",
                "badge": "비즈니스 지표",
                "badge_cls": "pill-amber",
                "bullets": [
                    "<strong>모든 사기 금액은 같지 않습니다:</strong> 5천 원 소액 오탐과 500만 원 거액 미탐을 같은 가중치로 취급하는 F1-Score 최대화는 실무 FDS와 맞지 않습니다. `거래금액 × 미탐률` vs `오탐 CS·이탈 비용`을 반영한 Cost-Sensitive Threshold 최적화가 필수입니다.",
                    "<strong>라이브러리에 없는 함수명 기재:</strong> P3 기술스택 표의 `Scikit-learn (pr_auc_score)`는 존재하지 않는 API입니다(`average_precision_score` 또는 `auc(recall, precision)`). 기술 면접 시 즉각 감점 요인이 되므로 정확히 수정하세요.",
                ],
            },
        ],
        "fix_table": [
            ("시간분할·극불균형", "통합 후 무작위 분할 + 비현실적 사기비율 3.68%에서만 검증", "Out-of-Time 시간순 분할 + Test 양성비율 0.1% 재보정(Calibration) 테스트 추가"),
            ("시니어 UX 재설계", "'주의(30~55%)' 구간까지 대형 팝업·TTS 음성 경보 발송", "주의 구간은 백엔드 무마찰 추가인증(ARS/생체인증), 위험(85%+)만 지연+보호자 알림"),
            ("온라인 Velocity 피처", "단건 행 피처만 사용해 연속 소액 스머핑/해외 점프 탐지 불가", "카드별 10분·1시간 누적건수/금액 및 직전 결제 대비 물리적 이동속도 파생 추가"),
            ("규정·문서 오기", "사후 SHAP 단독 설명 및 P3 `pr_auc_score` 미존재 함수명 표기", "여신전문금융업법 룰 엔진(선차단 코드) 결합 + `average_precision_score` 정정"),
        ],
        "fixes_code": [
            ("🔧 [Fix 1] F1 대신 금액 가중 기대손실(Expected Financial Loss) 기반 임계값 t* 산출",
             "loss = np.where((y_true==1)&(y_pred==0), amount, 0).sum() + np.where((y_true==0)&(y_pred==1), 5000, 0).sum()\n# 미탐 1건의 실제 거래금액 손실과 오탐 1건의 고객 마찰비용(5,000원)을 균형 최적화"),
            ("🔧 [Fix 2] 고위험군 차등 제어 정책 (알람 피로 제거용 3-Tier Action)",
             "if prob >= 0.85 or rule_hit: action = 'HOLD_AND_GUARDIAN_VOICE'  # 즉시 보류+고령자 음성확인\nelif prob >= 0.45: action = 'SILENT_STEP_UP_ARS'  # 팝업 공포 대신 1회 ARS/FIDO 확인"),
        ],
        "strategies": [
            ("💳 1. '금액 가중 손실절감액(원)'을 핵심 성과 지표로 추가", "비즈니스 임팩트", "pill-green", "PR-AUC 0.80보다 '10만 건당 부정결제 방어액 OOO만 원 vs 오탐 차단율 0.X%'가 현업 설득력이 큽니다."),
            ("👵 2. 시니어 보호는 '소리치는 팝업'이 아니라 '가족 안심승인·지연결제'", "UX 고도화", "pill-amber", "주의 구간 TTS를 없애고 고액/해외 거래 시 10분 지연+지정 보호자 승인 워크플로우로 전환하세요."),
            ("⚡ 3. Redis 기반 10분/1시간 Velocity 피처 서빙 레이어 구현", "아키텍처", "pill-blue", "FastAPI 추론 시 단건 JSON만 받지 말고 카드별 최근 거래 카운터를 Redis에서 조인해 200ms 안에 추론하세요."),
            ("📝 4. 기술스택 오기(`pr_auc_score`) 정정 & Out-of-Time 평가 재기록", "신뢰도 정비", "pill-slate", "발표서 3·5쪽의 API 오기와 분할 방식을 고쳐 포트폴리오 기술 신뢰도를 방어하세요."),
        ],
        "checklist": [
            ("데이터/지표", "Out-of-Time 분할 + 0.1% 스트레스 + 금액가중 손실 평가", "무작위 분할·3.68% 온실 데이터 편향 제거", "수정 필수", "pill-red"),
            ("UX/규정", "주의 구간 TTS 제거(무마찰 추가인증) + 룰엔진 하이브리드", "고령자 알람피로 해소 및 법규 사유코드 매핑", "수정 필수", "pill-red"),
            ("피처/오기", "카드별 Velocity 피처 추가 & `pr_auc_score` 오기 정정", "단건 피처 한계 극복 및 문서 기술 정확도 확보", "검증 필요", "pill-amber"),
            ("기본파이프라인", "Train-only 전처리 · SHAP · FastAPI <200ms 서빙", "누수 차단 및 서빙 레이턴시 기준 유지", "완료 확인", "pill-green"),
        ],
    },
    {
        "project_id": "m_shinsanga",
        "out_pdf": "mini_신상아_베어링예지보전_피드백.pdf",
        "course_label": "DMDG AI·데이터 심화 2기 (미니 프로젝트) | 실무자 기술 재감사 보고서",
        "title": "NASA IMS 기반 베어링 예지보전(PdM) 시스템",
        "subtitle": "실무 엔지니어링 냉철 재감사 · RUL 모델 전면 붕괴(R² -191)·대리라벨 한계·97% 시점 사후경보 진단",
        "authors": "신상아",
        "file_count": "총 1개 (발표 PDF 11p + Render/Streamlit 배포)",
        "review_date": "2026년 11월 26일 (실무 재감사)",
        "grade_label": "FAIR / NEEDS WORK (B)",
        "score": 73,
        "sub_scores": [
            ("1. 실패 실험 투명 보고 & Render/Streamlit 실배포", 88),
            ("2. RUL 예측 모델 성능 (BiLSTM·RF·Ridge 전면 실패)", 54),
            ("3. 결함 분류(RF) 교차 베어링/시험 일반화 입증도", 68),
            ("4. MAD×5 경보 리드타임(97.3% 경과) & 오경보(FPR) 검증", 70),
            ("5. 베어링 결함주파수(BPFO/BPFI) 포락선 물리 진단", 74),
        ],
        "exec_badge": "실무 재감사 B (73점)",
        "strength_title": "실패한 RUL 실험 수치를 숨기지 않고 정직하게 보고한 점과 FastAPI(Render)+Streamlit Cloud 실배포는 긍정적",
        "strength_body": "NASA IMS Test 1~3(9,464파일, 20kHz) 원본 TXT에서 RMS·Kurtosis·Crest Factor·FFT/STFT를 직접 처리하고 Render(FastAPI)+Streamlit Cloud까지 배포한 실행력은 좋습니다. 특히 BiLSTM이 단순 기준보다 나빴음(57.50h vs 38.21h)과 교차 시험 RUL R² 음수 발산을 미화하지 않고 명시한 점은 엔지니어링 태도 측면에서 신뢰할 만합니다.",
        "defect_title": "예지보전의 핵심인 RUL 모델 전면 붕괴(R² -133~-191) · 동일 베어링 대리라벨 과적합 · 수명 97.3% 시점의 늦은 경보",
        "defect_body": "실무 PdM 관점에서 본 프로젝트는 '예지보전 모델'이 사실상 작동하지 않은 상태입니다. (1) BiLSTM MAE(57.50h)가 평균 예측 같은 단순 기준(38.21h)보다 50% 나쁘고, 교차 시험 RUL 회귀는 RF R² -133.45~-191.30·Ridge R² -0.864로 완전히 붕괴했습니다. 이는 정상 구간까지 선형 카운트다운(`마지막시각-현재시각`)으로 라벨링하고 설비별 진동 오프셋을 정규화하지 않았기 때문입니다. (2) RF 분류 97.35%도 동일 베어링 내부 대리 라벨에 대한 회고적 평가여서 타 베어링 일반화가 미입증되었으며, (3) Test 3 MAD×5 경보(6,151/6,324번째, 수명 97.3% 경과)는 정비 리드타임 확보에 너무 늦고 정상 베어링 오경보율(FPR) 평가도 없습니다.",
        "files_table": [
            ("베어링예지보전_신상아.pdf", "PDF (발표서 11p)", "보완 필수 (B)", "실배포·정직 보고는 우수하나 RUL 전면 실패(R² -191)·교차분류 미검증·97.3% 지연경보"),
        ],
        "tech_sec_title": "2. RUL 실패 원인 · 대리라벨 일반화 한계 및 경보 리드타임 정밀 감사",
        "tech_blocks": [
            {
                "heading": "📌 [냉철한 PdM 모델 감사] 발표된 전 모듈의 실무 가용성 평가",
                "badge": "모델 재구축 필요",
                "badge_cls": "pill-red",
                "table": (
                    ["모듈", "발표 수치 & 평가 조건", "실무자 냉정 평가 (Failure Mode)", "교정 엔지니어링 해법"],
                    [
                        ["BiLSTM RUL", "1st 내부 MAE 57.50h (단순기준 38.21h)", "학습 모델이 상수/선형 기준선보다 50% 부정확 — 사용 불가", "FPT(열화 시작점) 탐지 후 구간 RUL 학습"],
                        ["RF/Ridge RUL", "1st→2nd RF R² -133/-191 · Ridge -0.86", "절대 RMS/시간 스케일이 다른 시험 간 비정규화 외삽 붕괴", "초기 정상기준 대비 비율(RMS/RMS₀) 정규화"],
                        ["RF 결함분류", "동일 베어링 시간블록 Acc 97.35% (F1 0.88)", "같은 베어링의 인접 시간대 복제 효과 — 새 설비 일반화 0%", "Leave-One-Bearing-Out 교차검증 필수"],
                        ["MAD×5 경보", "Test 3 6,151/6,324 (4/16 21:52 최초경보)", "전체 수명 97.3% 소진 후 경보 · 정상 베어링 FPR 미측정", "포락선(Hilbert) BPFO 에너지 + 단조추세"],
                    ],
                ),
            },
            {
                "heading": "📌 [물리·신호처리 맹점] 왜 R² -191이 나왔고, 왜 단순 RMS 경보는 늦는가",
                "badge": "도메인 원인 규명",
                "badge_cls": "pill-amber",
                "bullets": [
                    "<strong>선형 대리 RUL의 치명적 오류:</strong> 베어링 수명 초기 80%는 진동이 일정한 정상 상태인데, 타겟을 `T_end - t`로 두면 동일한 정상 진동 입력에 대해 1,000시간과 200시간을 동시에 맞추라는 모순된 학습을 강제해 회귀 모델이 발산합니다. 열화 시작점(FPT) 이후만 RUL 또는 Health Index(HI)로 정의해야 합니다.",
                    "<strong>초기 결함은 RMS가 아니라 포락선(Envelope) 스펙트럼에 먼저 뜹니다:</strong> Test 2/3 외륜 결함은 전체 RMS가 MAD×5를 넘기 수십 시간 전에 이미 BPFO(Ball Pass Frequency Outer) 고조파 피크에서 포착됩니다.",
                ],
            },
        ],
        "fix_table": [
            ("RUL 타겟 재정의", "전체 수명을 `마지막시각 - t`로 선형 라벨링해 정상 구간 학습 붕괴", "초기 300개 기준 이탈 시점(FPT) 이후만 0~1 Health Index(HI) 또는 구간 RUL 학습"),
            ("설비 간 스케일 정규화", "원시 특징값 그대로 다른 Test(베어링·하중 차이)에 적용해 R² -191 발산", "모든 특징을 각 베어링 초기 정상 구간 중앙값 대비 상대비(`x / median_init`)로 정규화"),
            ("교차 일반화 검증", "동일 베어링 내부 시간블록 Acc 97.35%를 모델 성능으로 오인 가능", "Test 1 외륜/내륜 학습 → Test 2/3 미지 베어링 평가(LOBO-CV) 성능 보고"),
            ("조기경보 리드타임", "Test 3 97.3% 시점(6,151/6,324)에서야 경보 · 정상 베어링 FPR 미측정", "Hilbert 포락선 + BPFO 대역 에너지 기반 조기경보 및 Test 1/2/3 정상채널 FPR=0% 검증"),
        ],
        "fixes_code": [
            ("🔧 [Fix 1] 시험 간 스케일 편차 제거 — 초기 정상구간 기준 상대 특징 정규화",
             "baseline = feat_df.iloc[:300].median()  # 설비/센서별 고유 진동 오프셋 제거\nnorm_feat = (feat_df - baseline) / (feat_df.iloc[:300].mad() + 1e-6)"),
            ("🔧 [Fix 2] Hilbert 포락선 기반 베어링 결함주파수(BPFO) 조기 스코어 산출",
             "env = np.abs(hilbert(bandpass(sig, 2000, 8000, fs=20000)))\n# 236Hz(IMS BPFO) ±5Hz 대역 진폭 추적으로 RMS MAD×5보다 앞선 조기경보 달성"),
        ],
        "strategies": [
            ("🩺 1. '회귀 RUL 폐기 → Health Index(열화지수) + 단조 열화모델' 전환", "핵심 처방", "pill-red", "데이터 3개(Run-to-Failure 3건)로 딥러닝 RUL을 맞추려는 시도를 멈추고 HI/트렌드 외삽으로 선회하세요."),
            ("🔊 2. Hilbert 포락선 BPFO/BPFI 주파수 추적 추가", "도메인 깊이", "pill-amber", "시연의 FFT 워터폴을 단순 시각화에 그치지 말고 결함 특성주파수 피크 탐지로 연결하세요."),
            ("🧪 3. 정상 베어링(Test 1 B1·B2, Test 2 B2~B4) 오경보율(FPR) 표 추가", "안전 검증", "pill-blue", "고장 난 베어링만 보지 말고, 정상 베어링 9개 채널에서 MAD×5 경보가 몇 번 울리는지 반드시 증명하세요."),
            ("📐 4. 메인 PC 재확인 미루지 말고 단일 재현 스크립트로 실험 확정", "엔지니어링", "pill-slate", "발표서 7쪽의 '메인 PC 재확인 필요' 같은 미완결 표기를 없애고 단일 파이프라인 수치로 통일하세요."),
        ],
        "checklist": [
            ("RUL재설계", "초기구간 상대정규화 + FPT 이후 Health Index 전환", "단순기준(38.21h) 및 R² 음수 발산(-191) 완전 해소", "수정 필수", "pill-red"),
            ("일반화/FPR", "Leave-One-Bearing-Out 교차검증 & 정상채널 FPR 측정", "동일 베어링 내 회고적 97.35% 착시 제거", "수정 필수", "pill-red"),
            ("조기경보", "Hilbert 포락선 BPFO 추적으로 경보 시점 앞당김", "Test 3 97.3%(6,151) 대비 최소 24~72시간 선행 경보 확보", "검증 필요", "pill-amber"),
            ("배포/투명성", "Render FastAPI + Streamlit Cloud 배포 & 실패 수치 투명 공개", "웹 시연 환경 구축 및 정직한 한계 기술", "완료 확인", "pill-green"),
        ],
    },
    {
        "project_id": "p_baemin",
        "out_pdf": "final_배차의민족_기획서_피드백.pdf",
        "course_label": "DMDG AI·데이터 심화 2기 (2차 최종 기획안) | 실무자 기획 재감사 보고서",
        "title": "배차의 민족 · 자동 화물 기사 매칭 플랫폼 개발 기획서",
        "subtitle": "실무 엔지니어링 냉철 재감사 · 3주(21일) 과잉 스코프·문서 내부 모순·정량 KPI 부재 진단",
        "authors": "오주원 · 신상아 · 김지선 · 방호원",
        "file_count": "총 1개 (기획서 PDF 9p)",
        "review_date": "2026년 11월 26일 (실무 재감사)",
        "grade_label": "FAIR / NEEDS WORK (B)",
        "score": 75,
        "sub_scores": [
            ("1. 물류 도메인 문제 정의 & KTDB·운임표 원천 확보", 86),
            ("2. 3주(21일) 일정 대비 스코프 현실성 (15종+ 과적)", 62),
            ("3. 기술스택·아키텍처 문서 일관성 (Redis/Celery 모순)", 68),
            ("4. 6.1절 정량 KPI·SLA 수치 구체성 (수치 0건)", 66),
            ("5. R&R 분산 균형 & 현장/안전 UX 고려", 76),
        ],
        "exec_badge": "실무 재감사 B (75점)",
        "strength_title": "KTDB 화물 O/D(2020~2024)·운임표 기반 시뮬레이션 설계 및 적재·매칭·관제 통합 아이디어는 우수",
        "strength_body": "화물 배차의 고질적 문제(적재 불가·공차 운행·무단 재위탁·정산 불투명)를 정확히 짚고, KTDB 실데이터(O/D Excel 5종×2)와 카고차량 운임표를 근거로 가상 시뮬레이터를 설계한 점은 실무 감각이 좋습니다. 국세청 진위확인, FSM 감사로그, Extreme Point 3D 적재 가이드까지 비즈니스 시나리오 구성력은 탄탄합니다.",
        "defect_title": "3주(21일) 4인 팀에 상용 기술 15종+ 과다 투입 · 문서 내 Redis/Celery 자기모순 · 정량 KPI 0건 · PM 단일 병목",
        "defect_body": "PM/테크리드 시선에서 이 기획서는 '3주(21일)짜리 프로젝트에 6개월 치 상용 풀스택을 다 우겨넣은 전형적 과잉 스코프(Over-scoping)'입니다. FastAPI·PostGIS·OSRM·Extreme Point·CF·LightGBM·헝가리안·FSM·Redis Streams·Celery·SHA-256·PG 에스크로·Pydeck·Three.js 모바일 3D·Gemini·플랫폼 등록 서류까지 한꺼번에 넣다 보니, 실제로 3.2절 표(7쪽)에는 `(기획 전용: Redis, Celery)`라고 적어 앞선 Phase 0~3(Redis Lock·Celery·Streams 필수 서술)과 정면으로 모순됩니다. 6.1절 정량 목표도 수치 없이 '수 초 이내·감소·최소화'뿐이고, 5.1절 R&R은 오주원 1인에게 PM+AI 전 엔진을 몰아넣었으며, 2.3절에는 '컬럼 검토 후 확정' 같은 미확정 메모가 남아 있습니다.",
        "files_table": [
            ("배차의 민족_오주원_신상아, 김지선, 방호원.pdf", "PDF (기획서 9p)", "보완 필수 (B)", "문제정의·KTDB는 우수하나 21일 과잉 스코프·스택 자기모순·KPI 수치 0건·R&R 편중"),
        ],
        "tech_sec_title": "2. WBS 실현가능성 · 문서 자기모순 및 R&R 병목 정밀 감사",
        "tech_blocks": [
            {
                "heading": "📌 [냉철한 PM/테크리드 감사] 3주 실행 시 높은 확률로 좌초할 4대 리스크",
                "badge": "스코프 경보",
                "badge_cls": "pill-red",
                "table": (
                    ["감사 영역", "기획서 현재 내용", "실무 PM 냉정 평가 (Risk)", "현업 WBS 교정안"],
                    [
                        ["일정 vs 범위", "3주(21일) 내 15종+ 기술·법적서류 일괄 구현", "3주차에 통합 디버깅 불가능 → 전부 Mock/껍데기 전락 위험", "MVP(적재+매칭+관제) / Stretch 분리"],
                        ["문서 모순", "Phase 0~3 Celery/Redis vs 7p `(기획 전용)`", "핵심 비동기/락 아키텍처가 구현 대상인지 문서만인지 불명확", "구현(Docker 포함) vs 제외 범위 명문화"],
                        ["정량 KPI", "6.1절 '수 초 이내, 감소, 최소화' (수치 0개)", "성공 기준(Acceptance Criteria)이 없으면 QA 합격 판정 불가", "매칭 P95<1s·공차 15%↓ 수치 고정"],
                        ["R&R 편중", "오주원 = PM + WBS + 보고서 + AI매칭 전 엔진", "핵심 4개 알고리즘(EP·CF·LGBM·헝가리안)이 1인 병목에 갇힘", "EP/CF/LGBM/헝가리안 팀원 분산"],
                    ],
                ),
            },
            {
                "heading": "📌 [현장 도메인·컴플라이언스 맹점] 실제 화물 운송 프로세스 간과 사항",
                "badge": "도메인 보완",
                "badge_cls": "pill-amber",
                "bullets": [
                    "<strong>화물차 OSRM 기본 프로파일 위험:</strong> 일반 OSRM 승용차 라우팅을 그대로 쓰면 화물차 통과 불가 고가/저상 교량·중량제한 도로로 안내됩니다. OSRM 커스텀 프로파일 또는 T-Map 화물차 경로 API 제약을 사전 명시해야 합니다.",
                    "<strong>차주 안전 UX 및 미확정 문구:</strong> 주행 중 차주의 Three.js·수락 버튼 조작은 도로교통법 위반 및 대형 사고 위험이 있으므로 '정차 상태/음성 수락' 제약을 걸어야 하며, 2.3절의 '컬럼 검토 후 확정' 같은 초안 메모는 착수 전 삭제해야 합니다.",
                ],
            },
        ],
        "fix_table": [
            ("MVP 스코프 컷", "21일 일정에 상용 플랫폼 전 기능(PG·법적서류·CF·Gemini 등) 동시 추진", "P0 핵심 3축(3D적재+PostGIS/LGBM/헝가리안+관제)만 구현, PG/국세청/CF는 Mock 고정"),
            ("스택 모순 해소", "Phase 0~3(Redis/Celery 핵심 서술) vs 3.2절 `(기획 전용: Redis, Celery)` 충돌", "실제 Docker Compose에 올릴 컴포넌트와 Phase 2 이후 이관 대상을 1개 표로 통일"),
            ("정량 KPI 명문화", "6.1절 기대효과가 정성 문구('감소', '최소화')로만 작성됨", "배차 P95 < 1.0s, 공차거리 -15%, 거절률 < 15%, GPS 유실 0% 4대 SLA 수치 고정"),
            ("1인 병목 분산", "오주원 1인에게 PM과 AI/적재/매칭 4대 알고리즘 일괄 집중", "Extreme Point(방호원/김지선) · LightGBM(신상아) 등 알고리즘 구현 R&R 분할"),
        ],
        "fixes_code": [
            ("🔧 [Fix 1] 6.1절 정량 목표(Acceptance Criteria) & Mock 경계 표준 명세",
             "SLA_TARGETS = {\n    'match_round_p95_sec': 1.0, 'deadhead_reduction_pct': 15.0,\n    'order_create_p95_sec': 0.5, 'gps_drop_rate_pct': 0.0\n}  # 3주 MVP 통과 기준"),
            ("🔧 [Fix 2] 3주 WBS 현실화 — Week 1~3 Go/No-Go 게이트 설정",
             "# W1: PostGIS + O/D Mock + 202 주문API | W2: EP + LGBM + 헝가리안 | W3: 관제UI + 동시성부하\n# Gate 실패 시 PG정산·국세청·Gemini 자연어 기능은 즉시 Freeze하고 핵심 매칭 안정화 우선"),
        ],
        "strategies": [
            ("✂️ 1. 과감한 Scope Cut(P0 vs P2)으로 '작동하는 코어' 먼저 사수", "PM 최우선", "pill-red", "15개 기술을 얕게 연결하다가 주문 API가 3초씩 걸리는 것보다, 5개 핵심 모듈을 빠르게 돌리는 게 낫습니다."),
            ("📏 2. 6.1절 KPI 숫자 확정 및 검증 테스트 케이스 1:1 매핑", "검증 규율", "pill-amber", "시뮬레이터 벤치마크가 목표 숫자를 넘었는지(Pass/Fail) 판정할 수 있는 기준표를 지금 고정하세요."),
            ("⚖️ 3. 알고리즘 구현 R&R 재분배로 단일 실패점(SPOF) 제거", "팀 운영", "pill-blue", "PM이 아키텍처·통합·보고서까지 맡고 AI 4종까지 코딩하면 2주차에 전체 일정이 마비됩니다."),
            ("🚛 4. 화물차 전용 도로 제약 & 주행 중 UI 잠금 정책 명문화", "현장 안전", "pill-green", "물류 도메인 특화 기획서답게 차주 안전 잠금(정차 시 조작)과 차량 높이/톤수 제한 라우팅을 명시하세요."),
        ],
        "checklist": [
            ("스코프/R&R", "3주 MVP 스코프 축소 & 오주원 1인 AI 병목 분산", "P0 코어 우선순위 확정 및 알고리즘 역할 분담", "수정 필수", "pill-red"),
            ("문서일관성", "3.2절 `(기획 전용: Redis, Celery)` 모순 및 2.3절 미확정 문구 수정", "아키텍처 본문과 기술스택 표 100% 일치", "수정 필수", "pill-red"),
            ("정량KPI", "6.1절 배차속도·공차감소·거절률 목표 수치 명문화", "모호한 정성 표현 제거 및 QA 판정 기준 확보", "보완 필요", "pill-amber"),
            ("원천/문제", "KTDB 2020~2024 O/D · 운임표 기반 문제정의", "실데이터 기반 수요 시뮬레이터 근거 확보", "완료 확인", "pill-green"),
        ],
    },
]
