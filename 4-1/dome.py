import math

DENSITY = {
    '유리': 2.4,
    '알루미늄': 2.7,
    '탄소강': 7.85
}


def sphere_area(dia: float, mat: str, thick: float = 1.0) -> tuple[float, float]:
    """반구체 돔의 표면적(m²)과 화성 기준 무게(kg)를 반환한다."""
    if dia <= 0:
        raise ValueError('지름은 0보다 커야 합니다.')
    if mat not in DENSITY:
        raise ValueError('유효하지 않은 재질입니다.')
    if thick <= 0:
        raise ValueError('두께는 0보다 커야 합니다.')
    
    radius = dia / 2
    area = 2 * math.pi * (radius ** 2)
    vol_m3 = area * (thick / 100)
    vol_cm3 = vol_m3 * 1_000_000
    density = DENSITY[mat]
    weight_kg = (vol_cm3 * density) / 1000
    mars_weight = weight_kg * 0.38
    return area, mars_weight


def main():
    print('=== Mars 돔 구조물 설계 프로그램 ===\n')

    try:
        dia_in = input('돔의 지름을 입력하세요 (m): ').strip()
        dia = float(dia_in)

        mat_in = input('재질을 입력하세요 (유리, 알루미늄, 탄소강): ').strip()

        thick_in = input('두께를 입력하세요 (cm, 기본값 1): ').strip()
        if not thick_in:
            thick = 1.0
        else:
            thick = float(thick_in)

        area, weight = sphere_area(dia, mat_in, thick)
        print(f'{mat_in} 돔, 지름 {dia:.3f} m, 두께 {thick:.3f} cm → '
              f'면적 {area:.3f} m², 무게(화성 기준) {weight:.3f} kg')

    except ValueError as e:
        print(f'Invalid input: {e}')
    except Exception as e:
        print(f'Processing error: {e}')


if __name__ == '__main__':
    main()
