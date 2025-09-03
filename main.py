import json

def main():
    """메인 함수 - 로그 분석 프로그램"""
    # 로그 파일 읽기
    filename = 'mission_computer_main.log'
    
    try:
        # 파일 읽기 및 전체 내용 출력
        with open(filename, 'r', encoding='utf-8') as file:
            log_content = file.read()
        
        print('=== 로그 파일 전체 내용 ===')
        print(log_content)
        
        # 헤더 제거 후 줄별로 처리
        lines = log_content.strip().split('\n')[1:]
        
        # 콤마로 분할하여 리스트 생성
        logs_list = []
        for line in lines:
            parts = line.split(',', 2)  # 최대 3개로 분할
            if len(parts) >= 3:
                datetime = parts[0]
                event = parts[1]
                message = parts[2]
                logs_list.append([datetime, message])
        
        # 원본 리스트 출력
        print('\n=== 원본 로그 리스트 ===')
        for log in logs_list:
            print(log)
        
        # 시간 역순으로 정렬
        logs_list_sorted = sorted(logs_list, key=lambda x: x[0], reverse=True)
        
        print('\n=== 시간 역순 정렬된 로그 리스트 ===')
        for log in logs_list_sorted:
            print(log)
        
        # 사전 객체로 변환
        logs_dict = {log[0]: log[1] for log in logs_list_sorted}
        
        # JSON 파일로 저장
        try:
            with open('mission_computer_main.json', 'w', encoding='utf-8') as json_file:
                json.dump(logs_dict, json_file, ensure_ascii=False, indent=2)
            print('\n=== JSON 파일 저장 완료 ===')
            print('파일명: mission_computer_main.json')
        except Exception as json_error:
            print(f'JSON 파일 저장 중 오류 발생: {json_error}')
        
        # 보너스: 위험 키워드 필터링
        danger_keywords = ['explosion', 'unstable', 'oxygen']
        dangerous_logs = []
        
        for log in logs_list:
            message_lower = log[1].lower()
            for keyword in danger_keywords:
                if keyword in message_lower:
                    dangerous_logs.append(log)
                    break
        
        if dangerous_logs:
            print('\n=== 위험 키워드 포함 로그 ===')
            for log in dangerous_logs:
                print(log)
            
            # 위험 로그를 파일로 저장
            try:
                with open('dangerous_logs.txt', 'w', encoding='utf-8') as danger_file:
                    for log in dangerous_logs:
                        danger_file.write(f'{log[0]}: {log[1]}\n')
                print('위험 로그가 dangerous_logs.txt에 저장되었습니다.')
            except Exception as danger_error:
                print(f'위험 로그 저장 중 오류: {danger_error}')
        
        # 보너스: 검색 기능
        search_term = input('\n검색할 키워드를 입력하세요 (Enter로 건너뛰기): ')
        if search_term.strip():
            search_logs(search_term, 'mission_computer_main.json')
    
    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
    except UnicodeDecodeError:
        print(f'오류: {filename} 파일 디코딩 중 문제가 발생했습니다.')
    except Exception as e:
        print(f'예상치 못한 오류가 발생했습니다: {e}')

def search_logs(search_term, json_filename):
    """JSON 파일에서 키워드 검색"""
    try:
        with open(json_filename, 'r', encoding='utf-8') as file:
            logs_dict = json.load(file)
        
        print(f'\n=== "{search_term}" 검색 결과 ===')
        found_count = 0
        
        for datetime, message in logs_dict.items():
            if search_term.lower() in message.lower():
                print(f'{datetime}: {message}')
                found_count += 1
        
        if found_count == 0:
            print('검색 결과가 없습니다.')
        else:
            print(f'총 {found_count}개의 결과를 찾았습니다.')
    
    except FileNotFoundError:
        print(f'{json_filename} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'검색 중 오류 발생: {e}')

if __name__ == '__main__':
    main()
