# My Contribution

## Project

GreenGuard AMR Navigation

## Main Responsibility

저는 GreenGuard 팀 프로젝트에서 TurtleBot4 기반 AMR 자율주행 및 순찰 제어를 담당했습니다.

제가 담당한 범위는 객체 탐지 모델 개발이나 웹/DB 구현이 아니라, AMR이 실제 환경에서 맵을 생성하고, 위치를 추정하고, waypoint를 따라 순찰할 수 있도록 구성하는 Navigation 부분입니다.

## Contributions

### 1. Map Structure Design

스마트팜 테스트 환경에서 TurtleBot4가 안정적으로 이동할 수 있도록 맵 구조를 설계했습니다.

주요 작업은 다음과 같습니다.

- TurtleBot4가 이동할 수 있는 통로 구조 확인
- 순찰이 필요한 구간 설정
- 로봇 회전과 이동이 가능한 waypoint 후보 위치 확인
- 추후 Nav2 순찰 경로로 사용할 수 있는 맵 구조 구성

### 2. SLAM Mapping

TurtleBot4와 연결된 Ubuntu Linux PC에서 SLAM을 실행하여 실내 맵을 생성했습니다.

주요 작업은 다음과 같습니다.

- TurtleBot4와 RPLIDAR 기반 SLAM 실행
- RViz2를 이용한 맵 생성 상태 확인
- teleop 명령어를 이용한 수동 이동
- 생성된 맵의 품질 확인
- Localization과 Nav2에서 사용할 최종 맵 생성

### 3. False Loop Closure Problem Solving

맵 생성 과정에서 False Loop Closure 문제가 발생했습니다.

이 문제를 해결하기 위해 맵 구조를 조정하고 slam.yaml 파라미터를 수정했습니다.

수정한 주요 내용은 다음과 같습니다.

- minimum_travel_distance를 0.0에서 0.15로 변경
- minimum_travel_heading을 0.0에서 0.12로 변경
- loop_search_maximum_distance를 3.0에서 1.5로 변경
- loop_match_minimum_chain_size를 10에서 15로 변경
- loop_match_maximum_variance_coarse를 3.0에서 1.5로 변경
- loop_match_minimum_response_coarse를 0.35에서 0.50으로 변경
- loop_match_minimum_response_fine을 0.45에서 0.60으로 변경

이를 통해 불안정한 loop closure 후보를 줄이고, SLAM 맵 생성 안정성을 개선했습니다.

### 4. Localization and Nav2 Setup

생성한 맵을 기반으로 Localization과 Nav2를 실행하여 TurtleBot4가 맵 상에서 자신의 위치를 추정하고 목표 지점까지 이동할 수 있도록 구성했습니다.

주요 작업은 다음과 같습니다.

- 생성된 맵을 기반으로 Localization 실행
- RViz2에서 TurtleBot4의 현재 위치 확인
- Nav2 Goal 기능을 이용한 목표 지점 이동 테스트
- amcl_pose 토픽을 이용한 로봇 현재 위치 확인
- TurtleBot4가 실제로 목표 지점까지 이동 가능한지 검증

### 5. Waypoint Collection

순찰 경로를 구성하기 위해 waypoint 좌표를 수집했습니다.

주요 작업은 다음과 같습니다.

- RViz2의 clicked_point 토픽을 활용한 waypoint 후보 좌표 확인
- RViz2 Nav2 Goal 기능을 활용한 목표 지점 이동 테스트
- teleop 명령어를 이용한 수동 이동 및 위치 검증
- amcl_pose 토픽을 이용한 로봇 현재 위치 확인
- 실제 주행 가능한 waypoint만 순찰 경로에 반영

### 6. Waypoint-based Patrol Control

수집한 waypoint를 기반으로 TurtleBot4가 지정된 순찰 경로를 반복 주행하도록 Python 기반 ROS2 순찰 코드를 작성했습니다.

주요 작업은 다음과 같습니다.

- waypoint 좌표를 코드에 반영
- TurtleBot4Navigator를 이용한 Nav2 goal 이동 구현
- amcl_pose 기반 현재 위치 확인
- 현재 위치에서 가장 가까운 waypoint 선택
- 가장 가까운 waypoint로 이동한 뒤 순찰 루프 진입
- 지정된 waypoint 순서에 따라 반복 순찰 수행

### 7. Nav2 Speed Parameter Tuning

순찰 중 특정 구간에서 TurtleBot4의 속도가 빨라 카메라 기반 객체 탐지가 불안정한 문제가 발생했습니다.

이를 해결하기 위해 순찰 구간에서 TurtleBot4가 더 천천히 이동하도록 Nav2 controller parameter를 코드 내부에서 조정했습니다.

적용한 속도 설정은 다음과 같습니다.

- 일반 주행 속도: 0.30 m/s
- 순찰 구간 속도: 0.15 m/s
- 일반 회전 속도: 1.00
- 순찰 구간 회전 속도: 1.00

조정한 주요 Nav2 파라미터는 다음과 같습니다.

- FollowPath.max_vel_x
- FollowPath.max_speed_xy
- FollowPath.max_vel_theta

이를 통해 순찰 중 카메라 기반 객체 탐지 안정성을 개선했습니다.

## What I Learned

이 프로젝트를 통해 다음 내용을 경험했습니다.

- SLAM 맵 품질이 Localization과 Nav2 주행 안정성에 직접적인 영향을 준다는 점
- False Loop Closure 문제를 줄이기 위해 SLAM 파라미터 튜닝이 필요하다는 점
- waypoint는 단순 좌표가 아니라 실제 로봇이 이동 가능한 위치인지 검증해야 한다는 점
- Nav2 기반 자율주행에서는 속도 파라미터가 perception 성능에도 영향을 줄 수 있다는 점
- 로봇 시스템에서는 Mapping, Localization, Planning, Control이 함께 맞물려야 안정적으로 동작한다는 점

## Note

이 문서는 GreenGuard 팀 프로젝트 중 제가 담당한 AMR Navigation 부분만 정리한 것입니다.

객체 탐지 모델 개발, 사람 추적 로직, 웹 대시보드, DB 구현은 이 문서의 주요 담당 범위에 포함하지 않았습니다.
