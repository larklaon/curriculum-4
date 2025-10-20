import math

DENSITY = {
    '유리': 2.4,
    '알루미늄': 2.7,
    '탄소강': 7.85
}

MARS_GRAVITY = 0.38


def calculate_dome(diameter, material, thickness=1.0):
    """반구체 돔의 표면적과 화성 중력 기준 무게 계산"""
    radius = diameter / 2
    area = 2 * math.pi * (radius ** 2)
    volume_m3 = area * (thickness / 100)
    volume_cm3 = volume_m3 * 1_000_000
    density = DENSITY[material]
    weight_kg = (volume_cm3 * density) / 1000
    return area, weight_kg * MARS_GRAVITY


def main():
    print('=== Mars 돔 구조물 설계 프로그램 ===\n')

    while True:
        print('돔 설계를 시작합니다. 종료하려면 "quit"을 입력하세요.\n')
        diameter_input = input('돔의 지름을 입력하세요 (m): ').strip()

        if diameter_input.lower() == 'quit':
            print('프로그램을 종료합니다.')
            break

        try:
            diameter = float(diameter_input)
        except ValueError:
            print('입력 오류: 숫자를 입력해야 합니다.\n')
            continue

        if diameter <= 0:
            print('입력 오류: 지름은 0보다 커야 합니다.\n')
            continue

        material = input('재질을 입력하세요 (유리, 알루미늄, 탄소강): ').strip()
        if material not in DENSITY:
            print('입력 오류: 지원하지 않는 재질입니다.\n')
            continue

        thickness_input = input('두께를 입력하세요 (cm, 기본값 1): ').strip()
        if not thickness_input:
            thickness = 1.0
        else:
            try:
                thickness = float(thickness_input)
            except ValueError:
                print('입력 오류: 두께는 숫자여야 합니다.\n')
                continue
            if thickness <= 0:
                print('입력 오류: 두께는 0보다 커야 합니다.\n')
                continue

        area, weight = calculate_dome(diameter, material, thickness)
        print('\n=== 계산 결과 ===')
        print(f'재질: {material}')
        print(f'지름: {diameter:.2f} m')
        print(f'두께: {thickness:.2f} cm')
        print(f'표면적: {area:.3f} m²')
        print(f'무게 (화성 기준): {weight:.3f} kg\n')
        print('-' * 50 + '\n')


if __name__ == '__main__':
    main()
