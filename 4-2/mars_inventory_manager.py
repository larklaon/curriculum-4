# mars_inventory_manager.py
# 목적: CSV 파일에서 적재물 목록을 읽어 위험 물품을 필터링하고 저장하는 프로그램

# ========== 파일 경로 설정 ==========
# 읽어올 CSV 파일의 이름
input_file = 'Mars_Base_Inventory_List.csv'

# 결과를 저장할 CSV 파일의 이름
output_file = 'Mars_Base_Inventory_danger.csv'

# ========== 1단계: CSV 파일 읽기 ==========
print('=== Mars 기지 적재물 목록 ===\n')

try:
    # try 블록: 오류가 발생할 수 있는 코드를 작성
    # 파일이 없거나, 읽기 권한이 없을 때 오류 처리를 위해 사용
    
    # open(): 파일을 여는 함수
    # 'r': read 모드 (읽기 전용)
    # encoding='utf-8': 한글이 깨지지 않도록 인코딩 설정
    # with 문: 파일을 자동으로 닫아주는 안전한 방법
    with open(input_file, 'r', encoding='utf-8') as file:
        
        # readlines(): 파일의 모든 줄을 읽어서 리스트로 반환
        # 각 줄이 리스트의 한 요소가 됨
        # 예: ['이름,수량,인화성\n', '산소탱크,10,0.9\n', ...]
        lines = file.readlines()
    
    # 읽어온 모든 줄을 화면에 출력
    for line in lines:
        # strip(): 줄 끝의 공백이나 줄바꿈 문자(\n)를 제거
        print(line.strip())
    
    print('\n=== CSV 파싱 시작 ===\n')
    
    # ========== 2단계: CSV 데이터를 파이썬 리스트로 변환 ==========
    
    # 적재물 정보를 저장할 빈 리스트 생성
    # 이 리스트에는 딕셔너리 형태로 각 항목이 저장됨
    inventory_list = []
    
    # 첫 번째 줄은 헤더(컬럼 이름)이므로 따로 저장
    # strip(): 앞뒤 공백 제거
    # split(','): 콤마를 기준으로 문자열을 나눠서 리스트로 만듦
    # 예: '이름,수량,인화성' -> ['이름', '수량', '인화성']
    header = lines[0].strip().split(',')
    
    # range(1, len(lines)): 1부터 마지막 줄까지 반복
    # 0번째 줄(헤더)은 건너뛰고 1번째 줄부터 처리
    for i in range(1, len(lines)):
        
        # i번째 줄을 가져와서 앞뒤 공백 제거
        line = lines[i].strip()
        
        # if line: 빈 줄이 아닌 경우에만 처리
        # 빈 줄이면 False, 내용이 있으면 True
        if line:
            
            # 콤마를 기준으로 문자열 분리
            # 예: '산소탱크,10,0.9' -> ['산소탱크', '10', '0.9']
            items = line.split(',')
            
            # 딕셔너리 형태로 데이터 저장 후 리스트에 추가
            # 딕셔너리: 키(key)와 값(value)으로 이루어진 자료구조
            # float(): 문자열을 실수(소수점 있는 숫자)로 변환
            inventory_list.append({
                'name': items[0],              # 이름 (문자열)
                'quantity': items[1],          # 수량 (문자열로 유지)
                'flammability': float(items[2]) # 인화성 지수 (실수로 변환)
            })
    
    # len(): 리스트의 길이(요소 개수)를 반환
    # f-string: 변수를 문자열에 포함시키는 방법
    print(f'총 {len(inventory_list)}개의 항목이 파싱되었습니다.\n')
    
    # ========== 3단계: 인화성 지수 기준으로 내림차순 정렬 ==========
    
    # sorted(): 리스트를 정렬하는 함수
    # key: 무엇을 기준으로 정렬할지 지정
    # lambda x: x['flammability']: 각 항목(x)의 'flammability' 값을 기준으로 정렬
    # lambda: 간단한 함수를 한 줄로 정의하는 방법
    # reverse=True: 내림차순 정렬 (큰 값부터)
    # reverse=False면 오름차순 (작은 값부터)
    sorted_inventory = sorted(inventory_list, 
                             key=lambda x: x['flammability'], 
                             reverse=True)
    
    print('=== 인화성 지수 기준 정렬 완료 ===\n')
    
    # ========== 4단계: 인화성 지수 0.7 이상인 항목만 필터링 ==========
    
    # 위험한 물품만 저장할 빈 리스트 생성
    dangerous_items = []
    
    # 정렬된 리스트의 각 항목을 하나씩 검사
    for item in sorted_inventory:
        
        # 인화성 지수가 0.7 이상인지 확인
        # >=: 크거나 같다
        if item['flammability'] >= 0.7:
            # 조건을 만족하면 위험 물품 리스트에 추가
            dangerous_items.append(item)
    
    # ========== 필터링 결과 화면에 출력 ==========
    print('=== 위험 물품 목록 (인화성 지수 >= 0.7) ===\n')
    
    # 헤더 출력
    print(f'{header[0]}, {header[1]}, {header[2]}')
    
    # 각 위험 물품의 정보 출력
    for item in dangerous_items:
        print(f'{item["name"]}, {item["quantity"]}, {item["flammability"]}')
    
    # ========== 5단계: 결과를 새로운 CSV 파일로 저장 ==========
    
    # 'w': write 모드 (쓰기 모드, 파일이 없으면 새로 생성)
    with open(output_file, 'w', encoding='utf-8') as file:
        
        # 헤더(컬럼 이름) 먼저 작성
        # write(): 파일에 문자열 쓰기
        # \n: 줄바꿈 문자
        file.write(f'{header[0]},{header[1]},{header[2]}\n')
        
        # 각 위험 물품의 데이터를 한 줄씩 작성
        for item in dangerous_items:
            file.write(f'{item["name"]},{item["quantity"]},{item["flammability"]}\n')
    
    print(f'\n위험 물품 목록이 {output_file}에 저장되었습니다.')

# ========== 예외 처리 ==========
# except: try 블록에서 오류가 발생했을 때 실행되는 코드

# FileNotFoundError: 파일을 찾을 수 없을 때 발생하는 오류
except FileNotFoundError:
    print(f'오류: {input_file} 파일을 찾을 수 없습니다.')

# Exception: 모든 종류의 오류를 잡음
# e: 오류 메시지를 담는 변수
except Exception as e:
    print(f'오류 발생: {e}')
