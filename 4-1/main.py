# json 모듈을 가져옵니다 (파이썬 내장 모듈)
import json

def main():
    """
    메인 함수 - 로그 분석 프로그램의 핵심 기능
    함수란: 특정 작업을 수행하는 코드 묶음
    """
    
    # 변수 선언: 읽어올 로그 파일의 이름을 저장
    filename = 'mission_computer_main.log'
    
    # try-except 구문: 오류가 발생할 수 있는 코드를 안전하게 실행
    try:
        # 파일을 읽기 모드('r')로 열고, UTF-8 인코딩으로 읽습니다
        # with 구문: 파일을 자동으로 닫아주는 안전한 방법
        with open(filename, 'r', encoding='utf-8') as file:
            # file.read(): 파일의 모든 내용을 하나의 문자열로 읽어옵니다
            log_content = file.read()
        
        # print(): 화면에 텍스트를 출력하는 함수
        print('=== 로그 파일 전체 내용 ===')
        print(log_content)  # 읽어온 파일 전체 내용을 출력
        
        # 문자열 처리:
        # .strip(): 앞뒤 공백과 줄바꿈 제거
        # .split('\n'): 줄바꿈 문자를 기준으로 문자열을 나누어 리스트로 만듦
        # [1:]: 리스트의 첫 번째 요소(헤더)를 제외하고 나머지만 가져옴
        lines = log_content.strip().split('\n')[1:]
        
        # 빈 리스트 생성: 처리된 로그 데이터를 저장할 공간
        logs_list = []
        
        # for 반복문: lines 리스트의 각 줄을 하나씩 처리
        for line in lines:
            # 문자열을 콤마(,)로 나누되, 최대 3개 부분으로만 나눕니다
            # split(',', 2): 처음 2개 콤마만으로 나누어서 최대 3개 부분 생성
            parts = line.split(',', 2)
            
            # if 조건문: parts 리스트의 길이가 3 이상인지 확인
            # len(): 리스트나 문자열의 길이를 구하는 함수
            if len(parts) >= 3:
                # 리스트 인덱싱: [0]은 첫 번째, [2]는 세 번째 요소
                datetime = parts[0]    # 날짜/시간 부분
                message = parts[2]     # 실제 메시지 내용 (parts[1]은 event 타입이므로 건너뜀)
                
                # .append(): 리스트에 새로운 요소를 추가하는 메서드
                logs_list.append([datetime, message])
        
        # 처리 결과 출력
        print('\n=== 원본 로그 리스트 ===')
        # \n: 줄바꿈 문자 (새 줄로 이동)
        
        # for 반복문으로 리스트의 각 요소를 출력
        for log in logs_list:
            print(log)  # 각 로그 항목 출력 [날짜시간, 메시지] 형태
        
        # sorted() 함수: 리스트를 정렬하는 함수
        # key=lambda x: x[0]: 정렬 기준을 각 항목의 첫 번째 요소(날짜시간)로 설정
        # lambda: 간단한 함수를 한 줄로 정의하는 방법
        # reverse=True: 내림차순 정렬 (최신 시간이 먼저 오도록)
        logs_list_sorted = sorted(logs_list, key=lambda x: x[0], reverse=True)
        
        print('\n=== 시간 역순 정렬된 로그 리스트 ===')
        for log in logs_list_sorted:
            print(log)
        
        # 딕셔너리 생성: {키: 값} 형태의 데이터 구조
        # 딕셔너리 컴프리헨션: 한 줄로 딕셔너리를 만드는 방법
        # {log[0]: log[1] for log in logs_list_sorted}의 의미:
        # - logs_list_sorted의 각 log에 대해
        # - log[0](날짜시간)을 키로, log[1](메시지)을 값으로 하는 딕셔너리 생성
        logs_dict = {log[0]: log[1] for log in logs_list_sorted}
        
        # JSON 파일 저장을 위한 try-except (중첩된 예외 처리)
        try:
            # JSON 파일을 쓰기 모드('w')로 열기
            with open('mission_computer_main.json', 'w', encoding='utf-8') as json_file:
                # json.dump(): 파이썬 객체를 JSON 파일로 저장
                # ensure_ascii=False: 한글 등 유니코드 문자를 그대로 저장
                # indent=2: JSON 파일을 보기 좋게 들여쓰기 2칸으로 포맷팅
                json.dump(logs_dict, json_file, ensure_ascii=False, indent=2)
            
            print('\n=== JSON 파일 저장 완료 ===')
            print('파일명: mission_computer_main.json')
            
        # JSON 저장 중 오류 발생 시 처리
        except Exception as json_error:
            # f-string: 문자열 안에 변수 값을 넣는 방법 f'{변수명}'
            print(f'JSON 파일 저장 중 오류 발생: {json_error}')
    
    # 파일을 찾을 수 없는 경우의 예외 처리
    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
    
    # 파일 인코딩 문제가 있는 경우의 예외 처리
    except UnicodeDecodeError:
        print(f'오류: {filename} 파일 디코딩 중 문제가 발생했습니다.')
    
    # 그 외 모든 예외를 처리하는 일반적인 예외 처리
    except Exception as e:
        print(f'예상치 못한 오류가 발생했습니다: {e}')

# 파이썬 프로그램의 진입점
# 이 파일이 직접 실행될 때만 main() 함수를 호출
if __name__ == '__main__':
    main()  # 메인 함수 실행



# 시작
# ↓
# 로그 파일 읽기 (open, read)
# ↓
# 전체 내용 출력 (print)
#  ↓
# CSV 데이터를 리스트로 변환 (strip, split, append)
#  ↓
# 원본 리스트 출력 (print)
#  ↓
# 시간 역순 정렬 (sorted)
#  ↓
# 정렬된 리스트 출력 (print)
#  ↓
# 딕셔너리로 변환 (딕셔너리 컴프리헨션) (간단하게 딕셔너리를 만들기 위한 방법)
#  ↓
# JSON 파일로 저장 (json.dump)
#  ↓
# 종료

