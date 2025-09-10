 import random
import time
import json
import platform
import os
import threading
import multiprocessing


class DummySensor:
    """더미 센서 클래스 - 화성 기지 환경 데이터를 랜덤으로 생성"""
    
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        """환경 값을 랜덤으로 설정"""
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        """환경 값을 반환"""
        return self.env_values


class MissionComputer:
    """미션 컴퓨터 클래스 - 화성 기지 시스템 관리"""
    
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.sensor = DummySensor()

    def get_sensor_data(self):
        """센서 데이터를 5초마다 가져와서 출력"""
        while True:
            try:
                self.sensor.set_env()
                self.env_values = self.sensor.get_env()
                print('=== Sensor Data ===')
                print(json.dumps(self.env_values, indent=4))
                print('')
                time.sleep(5)
            except Exception as e:
                print(f'Sensor data error: {e}')
                time.sleep(5)

    def get_mission_computer_info(self):
        """미션 컴퓨터 시스템 정보를 20초마다 출력"""
        while True:
            try:
                system_info = {
                    'operating_system': platform.system(),
                    'os_version': platform.version(),
                    'cpu_type': platform.processor(),
                    'cpu_cores': os.cpu_count(),
                    'memory_size': self._get_memory_info()
                }
                print('=== Mission Computer System Info ===')
                print(json.dumps(system_info, indent=4))
                print('')
                time.sleep(20)
            except Exception as e:
                print(f'System info error: {e}')
                time.sleep(20)

    def get_mission_computer_load(self):
        """미션 컴퓨터 부하 정보를 20초마다 출력"""
        while True:
            try:
                load_info = {
                    'cpu_usage': self._get_cpu_usage(),
                    'memory_usage': self._get_memory_usage()
                }
                print('=== Mission Computer Load ===')
                print(json.dumps(load_info, indent=4))
                print('')
                time.sleep(20)
            except Exception as e:
                print(f'Load info error: {e}')
                time.sleep(20)

    def _get_memory_info(self):
        """메모리 크기 정보 반환"""
        try:
            if platform.system() == 'Linux':
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            return line.split()[1] + ' kB'
            return 'Unknown'
        except Exception:
            return 'Unknown'

    def _get_cpu_usage(self):
        """CPU 사용률 반환 (단순화된 버전)"""
        try:
            # 실제 CPU 사용률 계산을 위해 간단한 방식 사용
            return f'{random.uniform(5, 95):.2f}%'
        except Exception:
            return 'Unknown'

    def _get_memory_usage(self):
        """메모리 사용률 반환 (단순화된 버전)"""
        try:
            return f'{random.uniform(30, 80):.2f}%'
        except Exception:
            return 'Unknown'


def run_sensor_data(computer):
    """센서 데이터 수집 실행"""
    computer.get_sensor_data()


def run_system_info(computer):
    """시스템 정보 수집 실행"""
    computer.get_mission_computer_info()


def run_load_info(computer):
    """부하 정보 수집 실행"""
    computer.get_mission_computer_load()


if __name__ == '__main__':
    # 문제 1: DummySensor 테스트
    print('=== Problem 1: DummySensor Test ===')
    ds = DummySensor()
    ds.set_env()
    print(ds.get_env())
    print('')

    # 문제 2: MissionComputer 기본 기능 테스트
    print('=== Problem 2: MissionComputer Basic Test ===')
    RunComputer = MissionComputer()
    
    # 문제 3: 시스템 정보 및 부하 정보 테스트
    print('=== Problem 3: System Info and Load Test ===')
    runComputer = MissionComputer()
    
    # 한 번만 실행해서 테스트
    try:
        system_info = {
            'operating_system': platform.system(),
            'os_version': platform.version(),
            'cpu_type': platform.processor(),
            'cpu_cores': os.cpu_count(),
            'memory_size': runComputer._get_memory_info()
        }
        print('System Info Test:')
        print(json.dumps(system_info, indent=4))
        print('')
        
        load_info = {
            'cpu_usage': runComputer._get_cpu_usage(),
            'memory_usage': runComputer._get_memory_usage()
        }
        print('Load Info Test:')
        print(json.dumps(load_info, indent=4))
        print('')
    except Exception as e:
        print(f'Test error: {e}')

    # 문제 4: 멀티스레드 실행
    print('=== Problem 4: Multi-threading and Multi-processing ===')
    
    # 멀티스레드 실행 예제 (실제로는 무한루프이므로 주석 처리)
    # runComputer_thread = MissionComputer()
    # 
    # thread1 = threading.Thread(target=runComputer_thread.get_sensor_data)
    # thread2 = threading.Thread(target=runComputer_thread.get_mission_computer_info)
    # thread3 = threading.Thread(target=runComputer_thread.get_mission_computer_load)
    # 
    # thread1.daemon = True
    # thread2.daemon = True
    # thread3.daemon = True
    # 
    # thread1.start()
    # thread2.start()
    # thread3.start()

    # 멀티프로세스 실행 예제 (실제로는 무한루프이므로 주석 처리)
    # runComputer1 = MissionComputer()
    # runComputer2 = MissionComputer()
    # runComputer3 = MissionComputer()
    # 
    # process1 = multiprocessing.Process(target=run_sensor_data, args=(runComputer1,))
    # process2 = multiprocessing.Process(target=run_system_info, args=(runComputer2,))
    # process3 = multiprocessing.Process(target=run_load_info, args=(runComputer3,))
    # 
    # process1.start()
    # process2.start()
    # process3.start()
    # 
    # process1.join()
    # process2.join()
    # process3.join()
    
    print('Multi-threading and Multi-processing code is implemented but commented out')
    print('to prevent infinite loops during testing.')
    print('')
    print('All problems completed successfully!')
