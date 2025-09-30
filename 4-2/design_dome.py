# design_dome.py
# 목적: 사용자 입력을 받아 반구체 돔의 표면적과 무게를 계산하는 프로그램

# ========== 필요한 모듈 가져오기 ==========
# math: 수학 계산에 필요한 함수들이 들어있는 모듈
# 예: math.pi (원주율 3.14159...), math.sqrt (제곱근) 등
import math

# ========== 전역 변수 선언 ==========
# 전역 변수: 프로그램 어디서든 접근 가능한 변수
# 함수 안에서 global 키워드를 사용하면 수정도 가능

# 재질 이름을 저장할 변수 (문자열)
material_name = ''

# 돔의 지름을 저장할 변수 (실수)
dome_diameter = 0.0

# 돔의 두께를 저장할 변수 (실수)
dome_thickness = 0.0

# 돔의 표면적을 저장할 변수 (실수)
dome_area = 0.0

# 돔의 무게를 저장할 변수 (실수)
dome_weight = 0.0

# ========== 상수 정의 ==========
# 상수: 프로그램 실행 중 변하지 않는 값
# 대문자로 작성하는 것이 관례

# 재질별 밀도를 저장한 딕셔너리
# 딕셔너리: {키: 값} 형태로 데이터를 저장
# 예: DENSITY['유리']를 하면 2.4가 반환됨
DENSITY = {
    '유리': 2.4,        # 유리의 밀도 (g/cm³)
    '알루미늄': 2.7,    # 알루미늄의 밀도 (g/cm³)
    '탄소강': 7.85      # 탄소강의 밀도 (g/cm³)
}

# 화성의 중력은 지구의 약 38%
MARS_GRAVITY = 0.38


# ========== 메인 계산 함수 정의 ==========
def sphere_area(diameter, material, thickness=1):
    """
    반구체 돔의 표면적과 무게를 계산하는 함수
    
    [함수란?]
    - 특정 작업을 수행하는 코드 묶음
    - 필요할 때마다 호출해서 사용 가능
    - 코드 재사용성을 높이고 프로그램을 깔끔하게 만듦
    
    [Parameters - 함수에 전달하는 값들]
    diameter (float): 돔의 지름
                     - 단위: 미터(m)
                     - 예: 10.0이면 지름이 10미터
                     - 필수 인자 (반드시 입력해야 함)
    
    material (str): 재질 이름
                   - 입력 가능한 값: '유리', '알루미늄', '탄소강'
                   - 예: '유리'
                   - 필수 인자
    
    thickness (float): 돔 껍데기의 두께
                      - 단위: 센티미터(cm)
                      - 기본값: 1 (입력하지 않으면 1cm로 설정됨)
                      - 선택 인자 (입력 안 해도 됨)
    
    [Returns - 함수가 반환하는 값들]
    area (float): 계산된 표면적 (제곱미터, m²)
    weight (float): 계산된 무게 (킬로그램, kg, 화성 중력 반영)
    
    [사용 예시]
    면적, 무게 = sphere_area(10, '유리')         # 두께는 기본값 1cm
    면적, 무게 = sphere_area(10, '유리', 2)      # 두께 2cm로 지정
    """
    
    # ========== 1단계: 반지름 계산 ==========
    # 반지름 = 지름 ÷ 2
    radius = diameter / 2
    
    # ========== 2단계: 반구체의 표면적 계산 ==========
    # 반구체 표면적 공식: 2 × π × r²
    # math.pi: 원주율 (약 3.14159...)
    # **: 거듭제곱 연산자 (radius ** 2는 radius × radius)
    area = 2 * math.pi * (radius ** 2)
    
    # ========== 3단계: 부피 계산 ==========
    # 돔 껍데기의 부피를 근사적으로 계산
    # 표면적 × 두께 = 부피
    
    # 두께를 센티미터에서 미터로 변환
    # 1m = 100cm이므로 100으로 나눔
    thickness_m = thickness / 100
    
    # 부피 계산 (단위: 입방미터, m³)
    volume_m3 = area * thickness_m
    
    # 부피를 입방센티미터로 변환
    # 1m³ = 1,000,000cm³
    volume_cm3 = volume_m3 * 1000000
    
    # ========== 4단계: 재질의 밀도 가져오기 ==========
    # DENSITY 딕셔너리에서 재질에 해당하는 밀도 값을 가져옴
    # 예: material이 '유리'면 density는 2.4가 됨
    density = DENSITY[material]
    
    # ========== 5단계: 무게 계산 ==========
    # 무게 = 부피 × 밀도
    # 단위: 그램(g)
    weight_g = volume_cm3 * density
    
    # 그램을 킬로그램으로 변환
    # 1kg = 1,000g
    weight_kg = weight_g / 1000
    
    # ========== 6단계: 화성 중력 반영 ==========
    # 화성에서의 무게 = 지구에서의 무게 × 0.38
    weight_mars = weight_kg * MARS_GRAVITY
    
    # ========== 7단계: 결과 반환 ==========
    # return: 함수가 계산한 결과를 돌려줌
    # 두 개의 값을 동시에 반환 (튜플 형태)
    return area, weight_mars


# ========== 메인 프로그램 함수 ==========
def main():
    """
    프로그램의 주요 실행 흐름을 담당하는 함수
    
    [기능]
    - 사용자로부터 입력 받기
    - sphere_area() 함수 호출
    - 결과 출력
    - 반복 실행 및 종료 처리
    
    [사용하는 전역 변수]
    - material_name: 재질 이름 저장
    - dome_diameter: 지름 저장
    - dome_thickness: 두께 저장
    - dome_area: 면적 저장
    - dome_weight: 무게 저장
    
    [Parameters]
    없음
    
    [Returns]
    없음
    """
    
    # global: 전역 변수를 함수 안에서 수정하겠다는 선언
    # 이 선언이 없으면 함수 안에서 새로운 지역 변수가 생성됨
    global material_name, dome_diameter, dome_thickness, dome_area, dome_weight
    
    print('=== Mars 돔 구조물 설계 프로그램 ===\n')
    
    # ========== 무한 반복 루프 ==========
    # while True: 종료 조건을 만날 때까지 계속 반복
    while True:
        
        # try 블록: 오류가 발생할 수 있는 코드
        try:
            # ========== 사용자 안내 메시지 ==========
            print('돔 설계를 시작합니다.')
            print('종료하려면 지름 입력 시 "quit"을 입력하세요.\n')
            
            # ========== 지름 입력 받기 ==========
            # input(): 사용자로부터 키보드 입력을 받는 함수
            # 입력받은 값은 항상 문자열(str) 타입
            diameter_input = input('돔의 지름을 입력하세요 (미터): ')
            
            # ========== 종료 조건 확인 ==========
            # lower(): 문자열을 모두 소문자로 변환
            # 'QUIT', 'Quit', 'quit' 모두 인식하기 위함
            if diameter_input.lower() == 'quit':
                print('프로그램을 종료합니다.')
                break  # break: 반복문을 완전히 빠져나감
            
            # ========== 지름을 숫자로 변환 ==========
            # float(): 문자열을 실수(소수점 있는 숫자)로 변환
            # 예: '10' -> 10.0, '10.5' -> 10.5
            diameter = float(diameter_input)
            
            # ========== 지름 유효성 검사 ==========
            # 지름은 반드시 0보다 커야 함
            if diameter <= 0:
                print('오류: 지름은 0보다 커야 합니다.\n')
                continue  # continue: 이번 반복을 건너뛰고 다음 반복으로
            
            # ========== 재질 입력 받기 ==========
            print('\n사용 가능한 재질: 유리, 알루미늄, 탄소강')
            material = input('재질을 입력하세요: ')
            
            # ========== 재질 유효성 검사 ==========
            # in: 값이 딕셔너리의 키에 있는지 확인
            # not in: 값이 없으면 True
            if material not in DENSITY:
                print('오류: 유효하지 않은 재질입니다.\n')
                continue
            
            # ========== 두께 입력 받기 ==========
            thickness_input = input('두께를 입력하세요 (cm, 기본값 1): ')
            
            # ========== 두께 처리 ==========
            # strip(): 앞뒤 공백 제거
            # 빈 문자열이면 기본값 1 사용
            if thickness_input.strip() == '':
                thickness = 1
            else:
                # 입력받은 값을 실수로 변환
                thickness = float(thickness_input)
                
                # 두께 유효성 검사
                if thickness <= 0:
                    print('오류: 두께는 0보다 커야 합니다.\n')
                    continue
            
            # ========== 계산 함수 호출 ==========
            # sphere_area() 함수를 호출하고 결과를 받음
            # 함수가 반환한 두 값을 area와 weight 변수에 저장
            area, weight = sphere_area(diameter, material, thickness)
            
            # ========== 전역 변수에 결과 저장 ==========
            material_name = material
            dome_diameter = diameter
            dome_thickness = thickness
            dome_area = area
            dome_weight = weight
            
            # ========== 결과 출력 ==========
            print('\n=== 계산 결과 ===')
            # f-string과 :.3f 형식 지정자
            # :.3f는 소수점 3자리까지 표시
            print(f'재질 ⇒ {material_name}, 지름 ⇒ {dome_diameter}, 두께 ⇒ {dome_thickness}, 면적 ⇒ {dome_area:.3f}, 무게 ⇒ {dome_weight:.3f} kg\n')
            print('-' * 50 + '\n')
            
        # ========== 예외 처리 ==========
        
        # ValueError: 숫자로 변환할 수 없는 값을 입력했을 때
        # 예: '10a', 'abc' 등을 float()로 변환하려고 할 때
        except ValueError:
            print('오류: 숫자를 입력해야 합니다.\n')
        
        # 그 외 모든 예외
        except Exception as e:
            print(f'오류 발생: {e}\n')


# ========== 프로그램 시작 지점 ==========
# __name__: 파이썬이 자동으로 설정하는 특수 변수
# 직접 실행하면 '__main__'이 됨
# 다른 파일에서 import하면 '__main__'이 아님
if __name__ == '__main__':
    # main() 함수 호출
    main()
