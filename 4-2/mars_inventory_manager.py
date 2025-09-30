# mars_inventory_manager.py
# -----------------------------------------------------------------------------
# 목적:
#   - 'Mars_Base_Inventory_List.csv' 파일을 읽어 화면에 출력한다.
#   - 각 행을 콤마(,) 기준으로 파싱하여 Python 리스트로 보관한다.
#   - 'Flammability'(인화성 지수) 기준으로 내림차순 정렬한다.
#   - 인화성 지수가 0.7 이상인 항목만 필터링하여 별도로 출력한다.
#   - 필터링 결과를 'Mars_Base_Inventory_danger.csv' 파일로 CSV 형식 저장한다.
# -----------------------------------------------------------------------------

import csv  # CSV 파일을 편리하게 읽고 쓸 수 있는 표준 라이브러리 모듈


def safe_float(text):
    """
    주어진 문자열을 실수(float)로 변환한다.
    - 변환이 가능한 경우: float 값 반환
    - 변환이 불가능한 경우(예: 'Various'): None 반환

    파라미터:
        text (str): 숫자일 수도 있고 아닐 수도 있는 문자열

    반환값:
        float 또는 None
    """
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def format_number_or_text(value):
    """
    숫자처럼 보이는 문자열이면 소수점 세 자리까지 포맷팅해서 문자열로 반환하고,
    숫자가 아니면 원래 문자열을 그대로 반환한다.

    - 출력 요구사항: 모든 숫자 출력은 소수점 이하 3자리까지 제한
    - 예: '0.98765' -> '0.988', '2' -> '2.000', 'Various' -> 'Various'

    파라미터:
        value (str): 원본 문자열

    반환값:
        str: 포맷팅된 문자열 또는 원본 문자열
    """
    num = safe_float(value)
    if num is None:
        return value
    return f'{num:.3f}'


def read_inventory(csv_path):
    """
    CSV 파일에서 재고(인벤토리) 데이터를 읽어온다.

    동작:
        1) 파일을 UTF-8 인코딩으로 연다.
        2) csv.reader로 한 줄씩 읽는다.
        3) 첫 줄은 헤더로 분리하여 header 변수에 저장한다.
        4) 이후 각 행(row)은 리스트 상태 그대로 records 리스트에 추가한다.
        5) 읽은 내용을 화면에 그대로 출력한다(요구사항: 파일 내용을 읽어 출력).

    예외 처리:
        - 파일이 없으면 FileNotFoundError를 잡아 사용자에게 알리고, (header, records)를 (None, [])로 반환
        - 그 외 예외는 Exception으로 잡아 메시지를 출력하고, (None, []) 반환

    파라미터:
        csv_path (str): 입력 CSV 파일 경로

    반환값:
        tuple(list[str] | None, list[list[str]]):
            (header, records)
            header: CSV 헤더(리스트) 또는 None
            records: CSV 본문 데이터(각 행이 리스트) 목록
    """
    header = None
    records = []

    try:
        # 파일 열기 (읽기 모드, UTF-8 인코딩)
        with open(csv_path, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)

            # 첫 행은 헤더
            header = next(reader)

            # 화면 출력: 헤더
            print('===== CSV 헤더 =====')
            print(header)

            # 화면 출력: 본문 각 행
            print('\n===== CSV 원본 내용 (각 행을 리스트로 표시) =====')
            for row in reader:
                print(row)
                records.append(row)

    except FileNotFoundError:
        print(f'오류: 파일을 찾을 수 없습니다 -> {csv_path}')
        return None, []
    except Exception as e:
        print(f'오류: CSV 읽기 중 문제가 발생했습니다 -> {e}')
        return None, []

    return header, records


def sort_by_flammability_desc(records, flammability_col_index=4):
    """
    인화성 지수(Flammability) 기준으로 내림차순 정렬한다.

    동작:
        - 각 행의 인화성 지수 문자열을 숫자로 변환한다.
        - 숫자로 변환 가능한 행만 해당 값으로 정렬한다.
        - 변환 불가능(None)인 값은 아주 작은 값으로 간주하여 끝쪽(하위)로 보낸다.

    구현 상세:
        - 정렬 키 함수에서 safe_float로 숫자 변환을 시도한다.
        - None이면 -1.0 같은 작은 값으로 대체하여 정렬 순위가 뒤로 가게 한다.
        - reverse=True로 내림차순 정렬한다.

    파라미터:
        records (list[list[str]]): CSV 본문 데이터
        flammability_col_index (int): 'Flammability' 컬럼의 인덱스 (기본값 4)

    반환값:
        list[list[str]]: 정렬된 새 리스트 (원본은 변경하지 않음)
    """
    def sort_key(row):
        num = safe_float(row[flammability_col_index])
        return num if num is not None else -1.0

    # 파이썬의 sorted는 원본을 건드리지 않고 새 리스트를 반환한다.
    sorted_records = sorted(records, key=sort_key, reverse=True)
    return sorted_records


def filter_by_flammability(records, threshold=0.7, flammability_col_index=4):
    """
    인화성 지수(Flammability)가 주어진 기준(threshold) 이상인 행만 필터링한다.

    파라미터:
        records (list[list[str]]): CSV 본문 데이터
        threshold (float): 하한 기준값 (기본값: 0.7)
        flammability_col_index (int): 'Flammability' 컬럼 인덱스 (기본값 4)

    반환값:
        list[list[str]]: 인화성 지수가 기준 이상인 행들의 리스트
    """
    filtered = []
    for row in records:
        num = safe_float(row[flammability_col_index])
        if num is not None and num >= threshold:
            filtered.append(row)
    return filtered


def print_table(records, header=None):
    """
    표 형태로 보기 좋게 출력한다.
    - 숫자는 소수점 3자리로 맞추고, 숫자가 아니면 원문 그대로 출력한다.
    - 'Weight (g/cm³)', 'Specific Gravity', 'Flammability' 같은 수치열을 자동 포맷한다.

    파라미터:
        records (list[list[str]]): 출력할 데이터 행 목록
        header (list[str] | None): 헤더가 있으면 먼저 출력
    """
    # 인덱스 기준으로 포맷 대상 열을 지정
    numeric_cols = {1, 2, 4}  # Weight, Specific Gravity, Flammability

    if header:
        print(' | '.join(header))

    for row in records:
        display_row = []
        for idx, cell in enumerate(row):
            if idx in numeric_cols:
                display_row.append(format_number_or_text(cell))
            else:
                display_row.append(cell)
        print(' | '.join(display_row))


def save_csv(csv_path, header, records, numeric_cols=None):
    """
    주어진 데이터(records)를 CSV 파일로 저장한다.
    - 저장 전 숫자열은 소수점 3자리로 문자열 포맷팅한다.
    - 파일 쓰기 과정 전체를 예외 처리로 감싼다.

    파라미터:
        csv_path (str): 저장할 파일 경로
        header (list[str]): CSV 헤더
        records (list[list[str]]): 저장할 데이터 행들
        numeric_cols (set[int] | None): 숫자 포맷팅을 적용할 열 인덱스 집합
                                        None이면 빈 집합으로 처리

    반환값:
        bool: 저장 성공 여부 (True/False)
    """
    if numeric_cols is None:
        numeric_cols = set()

    try:
        # newline='' 옵션은 csv.writer가 줄바꿈을 이중으로 넣지 않도록 방지
        with open(csv_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)

            # 헤더 먼저 쓰기
            writer.writerow(header)

            # 각 행을 순회하며 숫자열 포맷 후 쓰기
            for row in records:
                out_row = []
                for idx, cell in enumerate(row):
                    if idx in numeric_cols:
                        out_row.append(format_number_or_text(cell))
                    else:
                        out_row.append(cell)
                writer.writerow(out_row)

        print(f'저장 완료: {csv_path}')
        return True

    except PermissionError:
        print(f'오류: 쓰기 권한이 없어 저장할 수 없습니다 -> {csv_path}')
        return False
    except FileNotFoundError:
        # 상위 경로가 없는 등 경로 문제가 있을 수 있음
        print(f'오류: 경로를 찾을 수 없어 저장할 수 없습니다 -> {csv_path}')
        return False
    except Exception as e:
        print(f'오류: CSV 저장 중 문제가 발생했습니다 -> {e}')
        return False


def manage_inventory():
    """
    문제 1 전체 흐름을 담당하는 메인 함수.

    단계:
        1) 원본 CSV 읽기 + 화면 출력
        2) 리스트(행 목록)를 인화성 지수 기준 내림차순 정렬
        3) 정렬 결과를 화면에 표 형태로 출력
        4) 인화성 지수 0.7 이상 행만 필터링
        5) 필터링 결과를 화면에 표 형태로 출력
        6) 필터링 결과를 'Mars_Base_Inventory_danger.csv'로 저장
    """
    input_path = 'Mars_Base_Inventory_List.csv'
    output_path = 'Mars_Base_Inventory_danger.csv'

    # 1) CSV 읽기 (헤더, 본문)
    header, records = read_inventory(input_path)

    # 헤더를 읽지 못했거나 데이터가 비어 있으면 종료
    if header is None or not records:
        print('처리할 데이터가 없습니다. 프로그램을 종료합니다.')
        return

    # 2) 인화성 지수 기준 내림차순 정렬
    sorted_records = sort_by_flammability_desc(records, flammability_col_index=4)

    # 3) 정렬 결과 화면 출력
    print('\n===== 인화성 지수 기준 내림차순 정렬 결과 (상위부터) =====')
    print_table(sorted_records, header=header)

    # 4) 인화성 지수 0.7 이상 필터링
    danger_records = filter_by_flammability(sorted_records, threshold=0.7, flammability_col_index=4)

    # 5) 필터링 결과 화면 출력
    print('\n===== 인화성 지수 0.7 이상 위험물질 목록 =====')
    if danger_records:
        print_table(danger_records, header=header)
    else:
        print('기준(0.7) 이상에 해당하는 항목이 없습니다.')

    # 6) 필터링 결과 CSV 저장 (숫자 포맷 대상 열: 1, 2, 4)
    numeric_cols = {1, 2, 4}  # Weight, Specific Gravity, Flammability
    _ = save_csv(output_path, header, danger_records, numeric_cols=numeric_cols)


# 이 스크립트를 직접 실행하는 경우에만 main 함수를 호출한다.
# 다른 모듈에서 import 할 때는 자동 실행되지 않는다.
if __name__ == '__main__':
    manage_inventory()
