# mars_parts_analyzer.py
import numpy as np
import csv

def analyze_mars_parts():
    """Mars 부품 데이터 통합 분석 함수"""
    
    file_names = [
        'mars_base_main_parts-001.csv',
        'mars_base_main_parts-002.csv', 
        'mars_base_main_parts-003.csv'
    ]
    
    all_parts_names = []
    all_strengths = []
    
    try:
        # 각 CSV 파일에서 데이터 읽기
        for i, file_name in enumerate(file_names):
            print(f'{file_name} 읽는 중...')
            
            with open(file_name, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                
                names = []
                strengths = []
                
                for row in reader:
                    names.append(row[0])
                    try:
                        strengths.append(float(row[1]))
                    except ValueError:
                        strengths.append(np.nan)
                
                all_parts_names.append(names)
                all_strengths.append(strengths)
        
        # NumPy 배열로 변환
        arr1 = np.array(all_strengths[0])
        arr2 = np.array(all_strengths[1]) 
        arr3 = np.array(all_strengths[2])
        
        print(f'arr1 형태: {arr1.shape}')
        print(f'arr2 형태: {arr2.shape}')
        print(f'arr3 형태: {arr3.shape}')
        
        # 세 배열을 병합하여 parts ndarray 생성
        parts = np.vstack((arr1, arr2, arr3))
        print(f'병합된 parts 형태: {parts.shape}')
        
        # 항목별 평균값 계산 (NaN 값 무시)
        mean_values = np.nanmean(parts, axis=0)
        
        print('\n항목별 평균 강도:')
        for i, (name, avg) in enumerate(zip(all_parts_names[0], mean_values)):
            print(f'{name}: {avg:.3f}')
        
        # 평균값이 50보다 작은 항목 필터링
        indices_below_50 = np.where(mean_values < 50)[0]
        
        filtered_names = [all_parts_names[0][i] for i in indices_below_50]
        filtered_means = [mean_values[i] for i in indices_below_50]
        
        print(f'\n평균 강도 50 미만 항목: {len(filtered_names)}개')
        
        # parts_to_work_on.csv로 저장 (예외 처리 포함)
        output_file = 'parts_to_work_on.csv'
        try:
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['parts', 'average_strength'])
                
                for name, avg in zip(filtered_names, filtered_means):
                    writer.writerow([name, round(avg, 3)])
            
            print(f'{output_file} 저장 완료!')
            
        except PermissionError:
            print(f'오류: {output_file} 파일에 쓰기 권한이 없습니다.')
        except Exception as e:
            print(f'파일 저장 오류: {e}')
            
    except FileNotFoundError as e:
        print(f'파일을 찾을 수 없습니다: {e}')
    except Exception as e:
        print(f'데이터 처리 오류: {e}')

if __name__ == '__main__':
    analyze_mars_parts()
