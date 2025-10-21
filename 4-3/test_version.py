import random
import time
import json


class DummySensor:
    """화성 기지 환경 정보를 임시로 생성하는 더미 센서 클래스"""
    
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
        """주어진 범위 내에서 랜덤한 환경 값을 생성"""
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        """현재 센서 데이터를 반환"""
        return self.env_values


class MissionComputer:
    """더미 센서로부터 데이터를 받아 관리하는 미션 컴퓨터"""
    
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.sensor = DummySensor()  # DummySensor 인스턴스 생성

    def get_sensor_data(self):
        """5초마다 센서 값을 받아와 출력"""
        while True:
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()
            print(json.dumps(self.env_values, indent=4))
            time.sleep(5)


# 테스트 실행
if __name__ == '__main__':
    run_computer = MissionComputer()
    run_computer.get_sensor_data()
