# mars_parts_analyzer.py
# 목적: 여러 CSV 파일의 부품 데이터를 통합하고 평균값을 기준으로 분석하는 프로그램

# ========== 필요한 모듈 가져오기 ==========
# numpy: 수치 계산을 위한 강력한 라이브러리
# 배열(array) 연산, 통계 계산 등을 빠르고 쉽게 할 수 있음
# 별칭(alias) 'np'로 사용 (관례적으로 np를 많이 씀)
import numpy as np

# ========== 파일 경로 설정 ==========
# 읽어올 CSV 파일 3개의 경로
file1 = 'mars_base_main_parts-001.csv'
file2 = 'mars_base_main_parts-002.csv'
file3 = 'mars_base_main_parts-003.csv'

# 결과를 저장할 파일 경로
output_file = 'parts_to_work_on.csv'

# ========== 메인 실행 코드 (예외 처리 포함) ==========
try:
    # try 블록: 오류가 발생할 수 있는 모든 코드를 여기에 작성
    
    print('=== Mars 부품 데이터 통합 분석 시작 ===\n')
    
    # ========== 1단계: CSV 파일을 NumPy 배열로 읽기 ==========
    print('CSV 파일을 읽는 중...')
    
    # np.genfromtxt(): CSV 파일을 읽어 NumPy 배열로 변환하는 함수
    # 
    # [Parameters - 함수에 전달하는 값들]
    # - 첫 번째 인자: 파일 경로 (문자열)
    # - delimiter: 데이터를 구분하는 문자 (CSV는 콤마 ',')
    # - skip_header: 건너뛸 줄 수 (1이면 첫 번째 줄을 건너뜀)
    #                헤더(컬럼 이름)를 제외하고 데이터만 읽기 위함
    #
    # [Returns]
    # - NumPy ndarray: 2차원 배열 (행렬과 비슷)
    #   예: [[1, 2, 3],
    #        [4, 5, 6],
    #        [7, 8, 9]]
    
    arr1 = np.genfromtxt(file1, delimiter=',', skip_header=1)
    arr2 = np.genfromtxt(file2, delimiter=',', skip_header=1)
    arr3 = np.genfromtxt(file3, delimiter=',', skip_header=1)
    
    # shape: 배열의 모양(크기)을 보여주는 속성
    # (행 개수, 열 개수) 형태로 표시
    # 예: (10, 5)면 10행 5열
    print(f'{file1} 읽기 완료: {arr1.shape}')
    print(f'{file2} 읽기 완료: {arr2.shape}')
    print(f'{file3} 읽기 완료: {arr3.shape}\n')
    
    # ========== 2단계: 세 배열을 하나로 병합 ==========
    print('배열 병합 중...')
    
    # np.vstack(): 배열을 수직(vertical)으로 쌓는 함수
    # 
    # [사용법]
    # np.vstack((배열1, 배열2, 배열3, ...))
    # 
    # [예시]
    # arr1 = [[1, 2],    arr2 = [[5, 6],
    #         [3, 4]]             [7, 8]]
    # 
    # vstack 결과 = [[1, 2],
    #                [3, 4],
    #                [5, 6],
    #                [7, 8]]
    #
    # [주의]
    # - 모든 배열의 열(column) 개수가 같아야 함
    # - 괄호가 두 개 (()) 필요함
    parts = np.vstack((arr1, arr2, arr3))
    
    print(f'병합 완료: {parts.shape}\n')
    
    # ========== 3단계: 항목별(열별) 평균값 계산 ==========
    print('항목별 평균값 계산 중...')
    
    # np.mean(): 평균을 계산하는 함수
    # 
    # [Parameters]
    # - 첫 번째 인자: 계산할 배열
    # - axis: 계산 방향을 지정
    #   * axis=0: 열(column) 방향으로 계산 (각 열의 평균)
    #   * axis=1: 행(row) 방향으로 계산 (각 행의 평균)
    #   * axis 없음: 전체 평균
    #
    # [예시]
    # 배열 = [[1, 2, 3],
    #         [4, 5, 6]]
    # 
    # axis=0 결과: [2.5, 3.5, 4.5]  (각 열의 평균)
    #               ↑    ↑    ↑
    #             1+4  2+5  3+6
    #              /2   /2   /2
    #
    # axis=1 결과: [2, 5]  (각 행의 평균)
    averages = np.mean(parts, axis=0)
    
    # enumerate(): 인덱스와 값을 동시에 반환하는 함수
    # 
    # [예시]
    # for i, avg in enumerate([10, 20, 30]):
    #     print(i, avg)
    # 출력:
    # 0 10
    # 1 20
    # 2 30
    print('평균값:')
    for i, avg in enumerate(averages):
        # :.2f는 소수점 2자리까지 표시
        print(f'  항목 {i+1}: {avg:.2f}')
    print()
    
    # ========== 4단계: 평균값이 50보다 작은 항목만 필터링 ==========
    print('평균값이 50 미만인 항목 필터링 중...')
    
    # np.where(): 조건을 만족하는 인덱스를 찾는 함수
    # 
    # [사용법]
    # np.where(조건)
    # 
    # [예시]
    # arr = [10, 60, 30, 80, 20]
    # indices = np.where(arr < 50)
    # 결과: [0, 2, 4]  (10, 30, 20의 인덱스)
    #
    # [0]를 붙이는 이유:
    # where()는 튜플로 결과를 반환하므로 첫 번째 요소를 가져옴
    low_avg_indices = np.where(averages < 50)[0]
    
    # 슬라이싱을 사용한 열 선택
    # parts[:, indices]: 
    # - ':' = 모든 행 선택
    # - 'indices' = 특정 열들만 선택
    #
    # [예시]
    # parts = [[1, 2, 3, 4],
    #          [5, 6, 7, 8]]
    # indices = [0, 2]
    # 결과 = [[1, 3],
    #         [5, 7]]
    parts_to_work_on = parts[:, low_avg_indices]
    
    print(f'필터링 완료: {parts_to_work_on.shape}\n')
    
    # ========== 5단계: 결과를 CSV 파일로 저장 ==========
    print(f'결과를 {output_file}에 저장 중...')
    
    # 헤더(컬럼 이름) 생성
    # join(): 리스트의 요소들을 하나의 문자열로 합치는 함수
    # 
    # [예시]
    # ','.join(['a', 'b', 'c']) -> 'a,b,c'
    # 
    # [리스트 컴프리헨션]
    # [식 for 변수 in 반복가능객체]
    # 
    # [예시]
    # [f'항목{i+1}' for i in [0, 2, 4]]
    # -> ['항목1', '항목3', '항목5']
    header = ','.join([f'항목{i+1}' for i in low_avg_indices])
    
    # np.savetxt(): NumPy 배열을 텍스트 파일로 저장하는 함수
    # 
    # [Parameters]
    # - fname: 파일 이름 (문자열)
    # - X: 저장할 배열
    # - delimiter: 구분자 (CSV는 콤마)
    # - header: 헤더(첫 줄) 문자열
    # - comments: 헤더 앞에 붙을 주석 문자 (''로 설정하여 제거)
    # - fmt: 숫자 형식
    #   * '%.2f' = 소수점 2자리까지
    #   * '%d' = 정수
    #   * '%s' = 문자열
    np.savetxt(output_file, parts_to_work_on, delimiter=',', 
               header=header, comments='', fmt='%.2f')
    
    print(f'저장 완료!\n')
    
    # ========== 분석 결과 요약 출력 ==========
    print('=== 분석 결과 요약 ===')
    print(f'전체 데이터 행 수: {parts.shape[0]}')
    print(f'전체 항목 수: {parts.shape[1]}')
    print(f'작업이 필요한 항목 수: {parts_to_work_on.shape[1]}')
    # +1을 하는 이유: 인덱스는 0부터 시작하지만 항목 번호는 1부터 시작
    print(f'작업이 필요한 항목 번호: {low_avg_indices + 1}')

# ========== 예외 처리 ==========

# FileNotFoundError: 파일을 찾을 수 없을 때
# 예: 파일 이름이 잘못되었거나, 파일이 존재하지 않을 때
except FileNotFoundError as e:
    print(f'오류: 파일을 찾을 수 없습니다 - {e}')

# PermissionError: 파일 접근 권한이 없을 때
# 예: 읽기 전용 폴더에 저장하려고 할 때
except PermissionError:
    print(f'오류: {output_file} 파일에 쓰기 권한이 없습니다.')

# ValueError: 데이터 형식이 잘못되었을 때
# 예: CSV에 숫자가 아닌 값이 있어서 배열로 변환 실패
except ValueError as e:
    print(f'오류: 데이터 형식이 올바르지 않습니다 - {e}')

# Exception: 위에서 처리하지 못한 모든 예외
except Exception as e:
    print(f'예상치 못한 오류 발생: {e}')
