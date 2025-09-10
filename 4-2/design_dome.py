import math

def sphere_area(diameter, material, thickness=1):
    """
    반구체 돔의 표면적과 무게를 계산하는 함수
    
    Args:
        diameter: 지름 (m)
        material: 재질 ('glass', 'aluminum', 'carbon_steel')
        thickness: 두께 (cm, 기본값: 1)
    
    Returns:
        tuple: (면적, 화성에서의 무게)
    """
    # 재질별 밀도 (g/cm³)
    material_density = {
        'glass': 2.4,
        'aluminum': 2.7,
        'carbon_steel': 7.85
    }
    
    # 입력값 검증
    if diameter <= 0:
        raise ValueError('지름은 0보다 커야 합니다.')
    
    if material not in material_density:
        raise ValueError('지원되지 않는 재질입니다.')
    
    if thickness <= 0:
        raise ValueError('두께는 0보다 커야 합니다.')
    
    # 반지름 계산
    radius = diameter / 2.0
    
    # 반구 표면적 계산: 2πr²
    area = 2 * math.pi * radius * radius
    
    # 두께를 m 단위로 변환
    thickness_m = thickness / 100.0
    
    # 부피 계산 (표면적 × 두께)
    volume_m3 = area * thickness_m
    
    # 밀도를 kg/m³로 변환 (g/cm³ → kg/m³)
    density_kg_m3 = material_density[material] * 1000
    
    # 무게 계산
    weight_kg = volume_m3 * density_kg_m3
    
    # 화성 중력 적용 (지구의 0.38배)
    mars_gravity_factor = 0.38
    weight_mars_kg = weight_kg * mars_gravity_factor
    
    return round(area, 3), round(weight_mars_kg, 3)

def main():
    """메인 실행 함수"""
    print('Mars 돔 구조물 설계 프로그램')
    print('=' * 40)
    
    while True:
        try:
            # 지름 입력
            diameter_input = input('\n지름(m)을 입력하세요 (종료: 0 또는 음수): ')
            diameter = float(diameter_input)
            
            if diameter <= 0:
                print('프로그램을 종료합니다.')
                break
            
            # 재질 입력
            print('재질을 선택하세요:')
            print('1. glass (유리)')
            print('2. aluminum (알루미늄)')
            print('3. carbon_steel (탄소강)')
            
            material_input = input('재질을 입력하세요: ').strip().lower()
            
            if material_input not in ['glass', 'aluminum', 'carbon_steel']:
                print('잘못된 재질입니다. 다시 입력해주세요.')
                continue
            
            # 두께 (고정값 1cm)
            thickness = 1
            
            # 계산 수행
            area, weight = sphere_area(diameter, material_input, thickness)
            
            # 재질명 한글 변환
            material_korean = {
                'glass': '유리',
                'aluminum': '알루미늄', 
                'carbon_steel': '탄소강'
            }
            
            # 결과 출력
            print(f'\n계산 결과:')
            print(f'재질 ⇒ {material_korean[material_input]}, '
                  f'지름 ⇒ {int(diameter)}, '
                  f'두께 ⇒ {thickness}, '
                  f'면적 ⇒ {area}, '
                  f'무게 ⇒ {weight} kg')
            
        except ValueError as e:
            if 'could not convert' in str(e):
                print('올바른 숫자를 입력하세요.')
            else:
                print(f'입력 오류: {e}')
        except Exception as e:
            print(f'예상치 못한 오류: {e}')

if __name__ == '__main__':
    main()
