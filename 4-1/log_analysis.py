from datetime import datetime

def vtime(ts: str) -> bool:
    try:
        datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def read_log(fname: str = 'mission_computer_main.log') -> str:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print('파일열기 오류: 파일이 존재하지 않습니다.')
        return
    except UnicodeDecodeError:
        print('디코딩 오류: UTF-8 형식을 확인하세요.')
        return

def main():
    data = read_log()
    if not data:
        return

    lines = data.strip().split('\n')
    if len(lines) < 2:

        return

    header = lines[0]
    items = lines[1:]
    if header != 'timestamp,event,message':
        print('로그포맷 오류: 헤더가 잘못되었습니다.')
        return

    lst = []
    tuple_lst = []
    for entry in items:
        cols = entry.split(',', 2)
        if len(cols) != 3 or not vtime(cols[0]):
            print('로그포맷 오류:')
            return
        lst.append(cols[0] + ',' + cols[2])
        temp = (cols[0], cols[2])
        tuple_lst.append(temp)


    print(data)

    print(tuple_lst)

    rev = sorted(lst, reverse=True)
    tuple_rev = sorted(tuple_lst, reverse=True)

    print(tuple_rev)

    try:
        dic = {i.split(',', 1)[0]: i.split(',', 1)[1] for i in rev}
    except Exception as e:
        print('처리단계 오류: 딕셔너리 변환 실패.', e)
        return

    print(dic)

if __name__ == '__main__':
    main()
