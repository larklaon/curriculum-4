# mars_inventory_manager.py
import csv

def manage_inventory():
    """Mars 기지 적재물 관리 및 위험 분석 함수"""
    input_filename = 'Mars_Base_Inventory_List.csv'
    output_filename = 'Mars_Base_Inventory_danger.csv'
    
    inventory = []
    
    try:
        # CSV 파일 읽기 및 출력
        with open(input_filename, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)
            print('CSV 내용:')
            print(header)
            
            for row in reader:
                print(row)
                inventory.append(row)
                
    except FileNotFoundError:
        print(f'오류: {input_filename} 파일을 찾을 수 없습니다.')
        return
    
    # 안전한 float 변환 함수
    def safe_float(value):
        try:
            return float(value)
        except ValueError:
            return -1
    
    # 인화성 지수 기준 내림차순 정렬
    inventory_sorted = sorted(inventory, key=lambda x: safe_float(x[4]), reverse=True)
    
    print('\n인화성 지수 기준 내림차순 정렬 결과:')
    for item in inventory_sorted:
        print(item)
    
    # 인화성 지수 0.7 이상 필터링
    filtered_inventory = [item for item in inventory_sorted 
                         if safe_float(item[4]) >= 0.7]
    
    print('\n인화성 지수 0.7 이상 위험물질:')
    for item in filtered_inventory:
        print(item)
    
    # 필터링 결과 CSV 저장
    try:
        with open(output_filename, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            for row in filtered_inventory:
                writer.writerow(row)
        print(f'\n위험물질 목록이 {output_filename}에 저장되었습니다.')
        
    except Exception as e:
        print(f'파일 저장 오류: {e}')

if __name__ == '__main__':
    manage_inventory()
