# mars_inventory_manager.py
# 목적: CSV 파일에서 적재물 목록을 읽고,
#       인화성 지수 기준으로 정렬하고,
#       위험 물품(인화성 >= 0.7)을 별도로 저장하는 프로그램.

# ========== 파일 이름 설정 ==========
input_file = 'Mars_Base_Inventory_List.csv'     # 입력 CSV 파일 이름
output_file = 'Mars_Base_Inventory_danger.csv'  # 결과를 저장할 CSV 파일 이름

print('=== Mars 기지 적재물 목록 ===\n')

try:
    # ========== 1단계: 파일 읽기 ==========
    # open(): 파일을 여는 함수
    # 'r' -> 읽기 모드
    # encoding='utf-8': 한글 깨짐 방지
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()   # 전체 줄을 리스트 형태로 읽어오기
    
    # 원본 내용 출력
    for line in lines:
        print(line.strip())   # strip(): 양쪽 공백과 줄바꿈 제거
    
    print('\n=== CSV 파싱 시작 ===\n')
    
    # 결과를 저장할 리스트
    inventory_list = []
    
    # 첫 번째 줄은 헤더 (컬럼 이름들)
    header = lines[0].strip().split(',')
    
    # ========== 2단계: CSV 파싱 ==========
    # 1번째 줄부터 끝까지 순회
    for i in range(1, len(lines)):
        line = lines[i].strip()  # 공백 제거
        if not line:             # 빈 줄이면 건너뜀
            continue
        
        # 쉼표(,)로 데이터 분리
        items = line.split(',')
        
        # 인화성 값 추출 (CSV의 마지막 열이 항상 인화성 값)
        try:
            flammability_value = float(items[-1])  # 문자열 → 실수(float) 변환
        except ValueError:
            # 'Various' 같은 경우 숫자가 아니므로 건너뜀
            print(f"[주의] '{items[0]}' 항목은 인화성 값이 숫자가 아니어서 제외됩니다.")
            continue
        
        # 딕셔너리 형태로 저장 (이름과 인화성 값만 관리)
        inventory_list.append({
            'name': items[0],                         # 물질 이름
            'flammability': flammability_value        # 인화성 지수 (실수)
        })
    
    print(f'총 {len(inventory_list)}개의 항목이 파싱되었습니다.\n')
    
    # ========== 3단계: 인화성 지수 기준 정렬 ==========
    # sorted(): 리스트 정렬
    # key=lambda x: x['flammability'] → 인화성 지수를 기준으로 정렬
    # reverse=True → 내림차순 정렬
    sorted_inventory = sorted(
        inventory_list, 
        key=lambda x: x['flammability'], 
        reverse=True
    )
    
    print('=== 인화성 지수 기준 정렬 완료 ===\n')
    
    # ========== 4단계: 위험 물품 필터링 ==========
    # 리스트 컴프리헨션 사용 → 조건 맞는 항목만 추출
    # 조건: 인화성 지수가 0.7 이상
    dangerous_items = [item for item in sorted_inventory if item['flammability'] >= 0.7]
    
    print('=== 위험 물품 목록 (인화성 지수 >= 0.7) ===\n')
    print('Substance,Flammability')  # 출력 헤더
    
    # 위험 항목 출력
    for item in dangerous_items:
        print(f'{item["name"]},{item["flammability"]}')
    
    # ========== 5단계: 결과 파일 저장 ==========
    # 'w' -> 쓰기 모드, 기존 파일 있으면 내용 덮어쓰기
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('Substance,Flammability\n')   # 헤더 작성
        for item in dangerous_items:
            f.write(f'{item["name"]},{item["flammability"]}\n')
    
    print(f'\n위험 물품 목록이 {output_file}에 저장되었습니다.')

# ========== 예외 처리 ==========
# 파일을 못 찾았을 경우
except FileNotFoundError:
    print(f'오류: {input_file} 파일을 찾을 수 없습니다.')
# 그 외 모든 오류 처리
except Exception as e:
    print(f'오류 발생: {e}')
