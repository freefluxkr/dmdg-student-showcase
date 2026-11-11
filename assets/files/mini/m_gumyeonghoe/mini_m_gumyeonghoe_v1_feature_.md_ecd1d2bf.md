V1 기준으로만 정리하면 아래 27개입니다.

## V1 = 27 Features

### 1. V0 기본 4개
| Feature | 의미 |
|---|---|
| `has_certificate` | 인증서 존재 여부 |
| `has_pe_warning` | PE 파싱 경고 존재 여부 |
| `general_entropy` | 파일 전체 엔트로피 |
| `import_api_count` | import API 함수 개수 |

### 2. GENERAL_STRINGS 5개
| Feature | 의미 |
|---|---|
| `general_size` | 파일 전체 크기 |
| `strings_numstrings` | 추출 문자열 개수 |
| `strings_avlength` | 문자열 평균 길이 |
| `strings_entropy` | 문자열 영역 엔트로피 |
| `strings_printables` | 출력 가능한 문자 수 |

### 3. HEADER 6개
| Feature | 의미 |
|---|---|
| `header_missing` | PE Header 누락/파싱 실패 여부 |
| `number_of_sections` | PE Header에 기록된 Section 수 |
| `sizeof_code` | 코드 영역 크기 |
| `sizeof_image` | 메모리 로드 시 전체 이미지 크기 |
| `sizeof_headers` | PE Header 영역 크기 |
| `address_of_entrypoint` | 프로그램 시작 코드 위치 |

### 4. SECTION_OVERLAY 7개
| Feature | 의미 |
|---|---|
| `section_missing` | Section 정보 누락 여부 |
| `section_count` | 실제 파싱된 Section 개수 |
| `mean_section_entropy` | Section entropy 평균 |
| `max_section_entropy` | 가장 높은 Section entropy |
| `overlay_size` | PE 구조 뒤 추가 데이터 크기 |
| `overlay_size_ratio` | 전체 파일 대비 Overlay 비율 |
| `overlay_entropy` | Overlay 데이터 entropy |

### 5. IMPORT 1개
| Feature | 의미 |
|---|---|
| `import_library_count` | import하는 DLL 개수 |

### 6. AUTHENTICODE 3개
| Feature | 의미 |
|---|---|
| `cert_count` | 인증서 개수 |
| `self_signed` | 자체 서명 인증서 여부 |
| `parse_error` | 인증서 파싱 오류 여부 |

### 7. WARNING 1개
| Feature | 의미 |
|---|---|
| `warning_count` | PE 파싱 경고 개수 |

## V1 성능

```text
Accuracy  : 0.8377
Precision : 0.8236
Recall    : 0.8595
F1        : 0.8412
ROC-AUC   : 0.9171
PR-AUC    : 0.9146
FPR       : 0.1841
FNR       : 0.1405
FP        : 5,522
FN        : 4,216
```

모델은 당시 `Logistic Regression`, threshold `0.5` 기준이었습니다.

핵심은 V1이 **PE 구조 + 문자열 + 인증서 + Import + Warning을 한 번에 27개로 확장해서 본 첫 전체 Feature 세트**였다는 점입니다.