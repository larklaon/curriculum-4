import numpy as np

def read_csv(filename):
    """
    CSV 파일을 읽어 구조화된 numpy 배열로 반환하는 함수입니다.
    
    Parameters:
    - filename (str): 읽을 CSV 파일 경로
    
    Returns:
    - numpy structured array: 각 행에 부품명(parts)와 strength를 필드로 가진 배열
    """
    # delimiter=',': 쉼표(,)로 구분된 CSV 포맷
    # skip_header=1: 첫 줄(헤더)을 건너뜀
    # dtype: 구조화 배열로 각 컬럼 타입 지정 (문자열 최대 50자, float64)
    # encoding='utf-8-sig': BOM(바이트순서표시자) 처리를 위한 인코딩 설정
    # np.genfromtxt()는 Python의 NumPy 라이브러리에서 제공하는 함수로, 텍스트 파일(주로 CSV 파일)을 읽어서 NumPy 배열로 변환해주는 함수.
    return np.genfromtxt(filename, delimiter=',', skip_header=1,
                       dtype=[('parts', 'U50'), ('strength', 'f8')],
                       encoding='utf-8-sig')


def main():
    # 각 CSV 파일 경로
    file1 = 'mars_base_main_parts-001.csv'
    file2 = 'mars_base_main_parts-002.csv'
    file3 = 'mars_base_main_parts-003.csv'

    # 결과를 저장할 CSV 파일 이름
    output_file = 'parts_to_work_on.csv'

    try:
        print('=== Mars 부품 데이터 통합 분석 시작 ===\n')
        
        # 1. 세 CSV 파일을 읽어서 구조화된 numpy 배열로 저장
        arr1 = read_csv(file1)
        arr2 = read_csv(file2)
        arr3 = read_csv(file3)

        print(f'{file1} 읽기 완료: {arr1.shape}')
        print(f'{file2} 읽기 완료: {arr2.shape}')
        print(f'{file3} 읽기 완료: {arr3.shape}\n')

        # 2. 부품명(parts) 배열 가져오기 (첫 번째 파일 기준)
        # 모든 파일의 부품명이 동일하다고 가정합니다.
        parts_names = arr1['parts']

        # 3. strength 데이터만 추출하여 float 배열로 변환
        strength1 = arr1['strength']
        strength2 = arr2['strength']
        strength3 = arr3['strength']

        # 4. 세 strength 배열을 모아서 2차원 배열 생성
        # vstack: 배열을 수직으로 쌓아서 (3, 100)의 행렬 생성
        # 각 행은 다른 CSV 파일의 strength 값, 각 열은 부품별 데이터
        all_strengths = np.vstack((strength1, strength2, strength3))

        # 5. 각 부품별 strength의 평균을 계산 (열 단위)
        # axis=0 => 행들을 평균 내어 각 열별 평균을 구함 (즉 부품별 평균)
        # mean 메서드는 NumPy 배열 내의 원소들의 산술 평균(Arithmetic Mean), 즉 모든 값을 더한 후 값의 개수로 나눈 결과를 계산하는 함수.
        averages = np.mean(all_strengths, axis=0)

        # 6. 평균값 출력
        print('부품별 평균 strength 값:')
        for i, avg in enumerate(averages):
            print(f'  {parts_names[i]}: {avg:.3f}')
        print()

        # 7. 평균 strength가 50 미만인 부품의 인덱스 찾기
        low_avg_indices = np.where(averages < 50)[0]

        # 8. 필터링된 부품명과 평균 strength 값 추출
        filtered_parts = parts_names[low_avg_indices]
        filtered_avgs = averages[low_avg_indices]

        print(f'작업이 필요한 부품 수: {len(filtered_parts)}\n')

        # 9. 결과를 CSV 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            # 헤더 작성
            f.write('part,average_strength\n')
            
            # 각 부품명과 평균 값 한 줄씩 기록
            # zip() 함수는 두 리스트/배열을 한 쌍씩 묶어줍
            for part, avg in zip(filtered_parts, filtered_avgs):
                f.write(f'{part},{avg:.3f}\n')

        print(f'{output_file}에 저장 완료!')

    except Exception as e:
        # 예외가 발생하면 오류 메시지 출력
        print('오류 발생:', e)


# 이 파일이 직접 실행될 때만 main() 실행
if __name__ == '__main__':
    main()
