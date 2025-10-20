def caesar_cipher_decode(target_text):
    """입력된 텍스트를 시저 암호(전수 방식)로 해독하는 함수."""
    results = []

    # 0~25까지 모든 시프트 값을 적용하며 가능한 모든 해독 텍스트를 시도
    for shift in range(26):
        decoded_text = ''
        for ch in target_text:
            # 대문자인 경우 (A~Z / ASCII 코드 65~90)
            if 'A' <= ch <= 'Z':
                # ord() : 문자 → ASCII 코드(정수)
                # chr() : ASCII 코드(정수) → 문자
                # 예: 'B'(66)에서 shift=1이면 (66-65-1) % 26 + 65 = 65 → 'A'
                decoded_text += chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))

            # 소문자인 경우 (a~z / ASCII 코드 97~122)
            elif 'a' <= ch <= 'z':
                decoded_text += chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))

            # 알파벳이 아닌 문자(공백, 숫자, 기호 등)는 그대로 유지
            else:
                decoded_text += ch

        # 각 시프트 결과를 출력해서 사람이 직접 확인 가능하도록 함
        print(f'[{shift:02d}] {decoded_text}')
        results.append(decoded_text)

    return results


def main():
    """시저 암호 해독 프로그램의 메인 함수."""
    # 1) 암호문 파일(password.txt)을 읽기 시도
    try:
        with open('password.txt', 'r', encoding='utf-8') as file:
            cipher_text = file.read()
    except FileNotFoundError:
        # 파일이 존재하지 않으면 안내 메시지를 출력하고 종료
        print('오류: password.txt 파일을 찾을 수 없습니다.')
        return
    except OSError:
        # 파일 접근 중 일반 입출력 오류 발생 시
        print('오류: 파일을 읽는 중 문제가 발생했습니다.')
        return

    # 2) 모든 시프트(0~25)에 대해 복호화 수행
    all_results = caesar_cipher_decode(cipher_text)

    # 3) 사용자가 “정답으로 보이는 시프트 값”을 입력
    try:
        k = int(input('정답으로 보이는 자리수를 입력하세요 (0~25): '))
        # 입력 값이 0~25 범위를 벗어나면 오류 처리
        if not 0 <= k <= 25:
            print('오류: 0에서 25 사이의 값을 입력해야 합니다.')
            return
    except ValueError:
        # 정수가 아닌 값을 입력했을 경우
        print('오류: 숫자를 입력해야 합니다.')
        return

    # 4) 해독된 결과를 result.txt 파일에 저장
    try:
        with open('result.txt', 'w', encoding='utf-8') as file:
            file.write(all_results[k])
        print('result.txt 저장 완료')
    except OSError:
        # 파일 쓰기 중 오류 발생 시
        print('오류: 파일을 저장하는 중 문제가 발생했습니다.')


# 이 파일이 직접 실행될 때만 main()을 호출
if __name__ == '__main__':
    main()
