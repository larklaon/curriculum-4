# mars_parts_analyzer.py
# -----------------------------------------------------------------------------
# 목적:
#   - 세 개의 CSV 파일에서 부품 데이터를 읽어 NumPy 배열로 변환
#   - 세 배열을 병합하여 하나의 ndarray(parts) 생성
#   - 각 부품별 평균값 계산
#   - 평균값이 50 미만인 항목만 필터링하여 CSV로 저장
# -----------------------------------------------------------------------------

import numpy as np  # 수치 계산 및 배열 처리를 위한 표준 라이브러리
import csv          # CSV 파일 입출력용 표준 라이브러리


def analyze_mars_parts():
    """
    Mars 부품 데이터 통합 분석 함수

    단계:
        1) 세 개의 CSV 파일에서 부품명과 강도 데이터를 읽어옴
        2) 각 파일의 데이터를 NumPy 배열(arr1, arr2, arr3)로 변환
        3) 세 배열을 세로로 병합하여 parts ndarray 생성
        4) 각 부품별 평균값 계산 (NaN 값은 무시)
        5) 평균값이 50 미만인 항목만 필터링
        6) 필터링 결과를 'parts_to_work_on.csv'로 저장 (예외 처리 포함)
        7) 모든 과정에서 상세한 예외 처리 및 안내 메시지 출력
    """
    # 분석 대상 CSV 파일 목록 (파일명은 문제에서 제시된 그대로 사용)
    file_names = [
        'mars_base_main_parts-001.csv',
        'mars_base_main_parts-002.csv',
        'mars_base_main_parts-003.csv'
    ]

    # 각 파일에서 읽은 부품명과 강도값을 저장할 리스트
    all_parts_names = []  # 각 파일의 부품명 리스트
    all_strengths = []    # 각 파일의 강도값 리스트

    try:
        # 1) 각 CSV 파일에서 데이터 읽기
        for i, file_name in enumerate(file_names):
            print(f'{file_name} 읽는 중...')

            with open(file_name, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # 첫 줄은 헤더(예: ['parts', 'strength'])

                names = []     # 부품명 저장 리스트
                strengths = [] # 강도값 저장 리스트

                for row in reader:
                    # 부품명은 첫 번째 열, 강도값은 두 번째 열
                    names.append(row[0])
                    try:
                        # 강도값을 float으로 변환 (숫자가 아닐 경우 np.nan으로 처리)
                        strengths.append(float(row[1]))
                    except ValueError:
                        strengths.append(np.nan)

                # 각 파일의 부품명, 강도값 리스트를 전체 리스트에 추가
                all_parts_names.append(names)
                all_strengths.append(strengths)

        # 2) NumPy 배열로 변환 (각 파일별 강도값 리스트 → 1차원 배열)
        arr1 = np.array(all_strengths[0])
        arr2 = np.array(all_strengths[1])
        arr3 = np.array(all_strengths[2])

        print(f'arr1 형태: {arr1.shape}')  # (부품 개수,)
        print(f'arr2 형태: {arr2.shape}')
        print(f'arr3 형태: {arr3.shape}')

        # 3) 세 배열을 세로로 병합 (vstack: 행 방향으로 쌓기)
        # 결과: (3, 부품 개수) 형태의 2차원 배열
        parts = np.vstack((arr1, arr2, arr3))
        print(f'병합된 parts 형태: {parts.shape}')

        # 4) 각 부품별 평균값 계산 (axis=0: 열 방향, NaN 값은 무시)
        mean_values = np.nanmean(parts, axis=0)

        print('\n항목별 평균 강도:')
        for i, (name, avg) in enumerate(zip(all_parts_names[0], mean_values)):
            print(f'{name}: {avg:.3f}')

        # 5) 평균값이 50 미만인 항목 인덱스 찾기
        indices_below_50 = np.where(mean_values < 50)[0]

        # 해당 인덱스의 부품명과 평균값만 추출
        filtered_names = [all_parts_names[0][i] for i in indices_below_50]
        filtered_means = [mean_values[i] for i in indices_below_50]

        print(f'\n평균 강도 50 미만 항목: {len(filtered_names)}개')

        # 6) parts_to_work_on.csv로 저장 (예외 처리 포함)
        output_file = 'parts_to_work_on.csv'
        try:
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                # 헤더 작성
                writer.writerow(['parts', 'average_strength'])

                # 각 부품명과 평균값을 소수점 3자리로 포맷하여 저장
                for name, avg in zip(filtered_names, filtered_means):
                    writer.writerow([name, round(avg, 3)])

            print(f'{output_file} 저장 완료!')

        except PermissionError:
            # 파일 쓰기 권한이 없을 때
            print(f'오류: {output_file} 파일에 쓰기 권한이 없습니다.')
        except Exception as e:
            # 기타 파일 저장 오류
            print(f'파일 저장 오류: {e}')

    except FileNotFoundError as e:
        # 입력 파일이 없을 때
        print(f'파일을 찾을 수 없습니다: {e}')
    except Exception as e:
        # 데이터 처리 중 기타 예외
        print(f'데이터 처리 오류: {e}')


# 이 파일을 직접 실행할 때만 분석 함수가 동작하도록 함
if __name__ == '__main__':
    analyze_mars_parts()
