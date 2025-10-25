def decode_caesar(text):
    out = []
    for shift in range(26):
        dec = ''
        for ch in text:
            if 'A' <= ch <= 'Z':
                dec += chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
            elif 'a' <= ch <= 'z':
                dec += chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))
            else:
                dec += ch
        print(f'[{shift:02d}] {dec}')
        out.append(dec)
    return out


with open('password.txt', 'r', encoding='utf-8') as f:
    cipher = f.read()

cands = decode_caesar(cipher)

idx = int(input('정답으로 보이는 자리수를 입력하세요 (0~25): '))
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write(cands[idx])

print('result.txt 저장 완료')
