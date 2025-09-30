# design_dome.py
# -----------------------------------------------------------------------------
# 목적:
#   - 반구체(돔) 구조물의 표면적과 무게를 계산하는 프로그램
#   - 사용자로부터 지름과 재질을 입력받아 계산 결과를 반복적으로 출력
#   - 잘못된 입력에 대한 예외 처리 및 종료 조건 구현
#   - 결과는 소수점 3자리까지 출력, 화성 중력(지구의 0.38배) 반영
# -----------------------------------------------------------------------------

import math  # 수학 함수(파이) 사용을 위한 표준 라이브러리


def sphere_area(diameter, material, thickness=1):
    """
    반구체 돔의 표면적과 무게를 계산하는 함수

    파라미터:
        diameter (float): 돔의 지름 (단위: m)
        material (str): 재질명 ('glass', 'aluminum', 'carbon_steel')
        thickness (float): 두께 (단위: cm, 기본값 1)

    반환값:
        tuple: (면적, 화성에서의 무게)
            면적: 반구 표면적 (단위: m^2, 소수점 3자리)
            무게: 화성 중력 적용 무게 (단위: kg, 소수점 3자리)
    """
    # 각 재질별 밀도 (g/cm³)
    material_density = {
        'glass': 2.4,         # 유리
        'aluminum': 2.7,      # 알루미늄
        'carbon_steel': 7.85  # 탄소강
    }

    # 입력값 검증: 지름, 두께는 0보다 커야 함
    if diameter <= 0:
        raise ValueError('지름은 0보다 커야 합니다.')
    if thickness <= 0:
        raise ValueError('두께는 0보다 커야 합니다.')
    if material not in material_density:
        raise ValueError('지원되지 않는 재질입니다.')

    # 반지름 계산 (지름의 절반)
    radius = diameter / 2.0

    # 반구 표면적 공식: 2 * pi * r^2
    area = 2 * math.pi * radius * radius

    # 두께(cm)를 m 단위로 변환 (1cm = 0.01m)
    thickness_m = thickness / 100.0

    # 부피 계산: 표면적 * 두께 (m³)
    volume_m3 = area * thickness_m

    # 밀도 변환: g/cm³ → kg/m³ (1g/cm³ = 1000kg/m³)
    density_kg_m3 = material_density[material] * 1000

    # 무게 계산: 부피 * 밀도 (kg)
    weight_kg = volume_m3 * density_kg_m3

    # 화성 중력 적용 (지구의 0.38배)
    mars_gravity_factor = 0.38

    weight_mars_kg = weight_kg * mars_gravity_factor

    # 소수점 3자리로 반올림하여 반환
    return round(area, 3), round(weight_mars_kg, 3)


def main():
    """
    메인 실행 함수
    - 사용자로부터 지름과 재질을 입력받아 돔의 면적과 무게를 계산
    - 잘못된 입력에 대한 예외 처리
    - 반복 실행 및 종료 조건 구현
    """
    print('Mars 돔 구조물 설계 프로그램')
    print('=' * 40)

    while True:
        try:
            # 사용자로부터 지름 입력 (문자열로 입력받아 float 변환)
            diameter_input = input('\n지름(m)을 입력하세요 (종료: 0 또는 음수): ')
            diameter = float(diameter_input)

            # 종료 조건: 0 이하 입력 시 프로그램 종료
            if diameter <= 0:
                print('프로그램을 종료합니다.')
                break

            # 재질 선택 안내 및 입력
            print('재질을 선택하세요:')
            print('1. glass (유리)')
            print('2. aluminum (알루미늄)')
            print('3. carbon_steel (탄소강)')

            material_input = input('재질을 입력하세요: ').strip().lower()

            # 지원하지 않는 재질 입력 시 안내 후 반복
            if material_input not in ['glass', 'aluminum', 'carbon_steel']:
                print('잘못된 재질입니다. 다시 입력해주세요.')
                continue

            # 두께는 기본값 1cm로 고정 (문제 요구사항)
            thickness = 1

            # 면적, 무게 계산 함수 호출
            area, weight = sphere_area(diameter, material_input, thickness)

            # 재질명 한글 변환 딕셔너리
            material_korean = {
                'glass': '유리',
                'aluminum': '알루미늄',
                'carbon_steel': '탄소강'
            }

            # 결과 출력 (문제에서 제시한 형식)
            print(f'\n계산 결과:')
            print(f'재질 ⇒ {material_korean[material_input]}, '
                  f'지름 ⇒ {int(diameter)}, '
                  f'두께 ⇒ {thickness}, '
                  f'면적 ⇒ {area}, '
                  f'무게 ⇒ {weight} kg')

        except ValueError as e:
            # 숫자 변환 실패 등 ValueError 발생 시 안내
            if 'could not convert' in str(e):
                print('올바른 숫자를 입력하세요.')
            else:
                print(f'입력 오류: {e}')
        except Exception as e:
            # 예기치 못한 모든 예외 처리
            print(f'예상치 못한 오류: {e}')

# 이 파일을 직접 실행할 때만 main() 함수가 동작하도록 함
if __name__ == '__main__':
    main()
