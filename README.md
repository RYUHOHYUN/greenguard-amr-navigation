# GreenGuard AMR Navigation

ROS2 Humble, Nav2, TurtleBot4, RPLIDAR를 활용한 SLAM 기반 AMR 자율주행 순찰 프로젝트입니다.

이 저장소는 GreenGuard 팀 프로젝트 중 제가 담당한 AMR 자율주행, SLAM 맵 생성, Localization, Waypoint 수집, 순찰 경로 제어, Nav2 속도 파라미터 튜닝 부분을 정리한 저장소입니다.

## Project Overview

GreenGuard는 스마트팜 환경에서 AMR이 자율주행으로 순찰하며 작물 상태와 이상 상황을 확인하는 스마트팜 AMR 순찰 시스템입니다.

전체 시스템은 AMR 자율주행, 객체 탐지, 이벤트 처리, 로그 저장, 웹 기반 모니터링으로 구성됩니다.

이 저장소에서는 그중 제가 담당한 AMR Navigation 부분만 다룹니다.

## My Role

저는 프로젝트에서 TurtleBot4 기반 AMR 자율주행 및 순찰 제어를 담당했습니다.

주요 담당 내용은 다음과 같습니다.

- 스마트팜 테스트 환경에 맞는 맵 구조 설계
- TurtleBot4와 연결된 Ubuntu Linux PC에서 SLAM을 실행하여 실내 맵 생성
- RViz2를 이용한 맵 생성 상태 확인
- 생성된 맵을 기반으로 Localization 및 Nav2 실행
- TurtleBot4의 위치 추정 및 목표 지점 이동 테스트
- /amcl_pose 토픽을 이용한 로봇 현재 위치 확인
- RViz2의 /clicked_point 토픽과 Nav2 Goal 기능을 활용한 waypoint 좌표 수집
- 수집한 waypoint를 기반으로 TurtleBot4 순찰 경로 구성
- Python 기반 ROS2 순찰 제어 코드 작성
- False Loop Closure 문제 해결을 위한 slam.yaml 파라미터 수정
- 순찰 루프 구간에서 객체 탐지 안정성을 높이기 위해 Nav2 속도 파라미터를 조정하여 저속 주행 구현

## Tech Stack

- ROS2 Humble
- Nav2
- TurtleBot4
- RPLIDAR
- RViz2
- AMCL
- SLAM
- Python
- Ubuntu 22.04

## Key Features

### 1. SLAM 기반 맵 생성

TurtleBot4와 RPLIDAR를 이용하여 테스트 환경의 실내 맵을 생성했습니다.

맵 생성 과정에서는 TurtleBot4와 연결된 Ubuntu Linux PC에서 SLAM을 실행하고, RViz2를 통해 실시간으로 맵 생성 상태를 확인했습니다.

생성된 맵은 이후 Localization과 Nav2 기반 자율주행 테스트에 활용했습니다.

### 2. False Loop Closure 문제 해결

초기 맵 생성 과정에서 False Loop Closure 문제가 발생했습니다.

이 문제를 해결하기 위해 맵 구조를 조정하고 slam.yaml의 SLAM 관련 파라미터를 수정했습니다.

수정한 주요 내용은 다음과 같습니다.

- minimum_travel_distance: 0.0에서 0.15로 변경
  - scan node가 너무 자주 생성되는 문제를 완화하기 위해 수정했습니다.

- minimum_travel_heading: 0.0에서 0.12로 변경
  - 아주 작은 회전에도 node가 생성되는 문제를 줄이기 위해 수정했습니다.

- loop_search_maximum_distance: 3.0에서 1.5로 변경
  - 너무 먼 loop closure 후보를 제거하기 위해 수정했습니다.

- loop_match_minimum_chain_size: 10에서 15로 변경
  - loop closure를 인정하기 위한 연속 매칭 기준을 강화했습니다.

- loop_match_maximum_variance_coarse: 3.0에서 1.5로 변경
  - 불확실한 coarse match를 제거하기 위해 수정했습니다.

- loop_match_minimum_response_coarse: 0.35에서 0.50으로 변경
  - 1차 매칭 점수 기준을 강화했습니다.

- loop_match_minimum_response_fine: 0.45에서 0.60으로 변경
  - 최종 매칭 점수 기준을 강화했습니다.

이를 통해 불안정한 loop closure 후보를 줄이고, SLAM 맵 생성 안정성을 개선했습니다.

### 3. Localization 및 Nav2 실행

생성된 맵을 기반으로 Localization과 Nav2를 실행했습니다.

RViz2에서 TurtleBot4의 현재 위치를 확인하고, Nav2 Goal 기능을 이용해 로봇이 목표 지점까지 이동하는지 테스트했습니다.

또한 /amcl_pose 토픽을 통해 로봇의 현재 위치 정보를 확인하며 waypoint 기반 순찰 로직에 활용했습니다.

### 4. Waypoint 수집

순찰 경로를 구성하기 위해 RViz2의 /clicked_point 토픽과 Nav2 Goal 기능을 활용했습니다.

또한 teleop 명령어로 TurtleBot4를 직접 이동시키며 실제 주행 가능한 위치를 확인했습니다.

수집한 waypoint는 TurtleBot4가 실제로 이동 가능한 위치인지 확인한 뒤 순찰 경로에 반영했습니다.

사용한 주요 정보는 다음과 같습니다.

- /amcl_pose
- /clicked_point
- RViz2 Nav2 Goal
- teleop command

### 5. Waypoint 기반 순찰

수집한 waypoint를 기반으로 TurtleBot4가 지정된 순찰 경로를 반복 주행하도록 Python 기반 ROS2 순찰 코드를 작성했습니다.

로봇은 /amcl_pose 토픽으로 현재 위치를 확인한 뒤, 현재 위치에서 가장 가까운 waypoint를 선택하고 순찰 루프에 진입하도록 구성했습니다.

순찰 waypoint 좌표는 가독성을 위해 config/waypoints.yaml에 별도로 정리했습니다.

현재 Python 실행 코드에는 실험 당시 사용한 waypoint 좌표가 직접 포함되어 있습니다.

순찰 경로는 다음과 같이 구성했습니다.

- point2
- point3
- point35_mid
- point24_mid
- point35_mid
- point5
- point4

### 6. Nav2 속도 파라미터 조정

순찰 중 특정 구간에서 TurtleBot4의 속도가 빨라 카메라 기반 객체 탐지가 불안정한 문제가 발생했습니다.

이를 해결하기 위해 순찰 구간에서는 TurtleBot4가 더 천천히 이동하도록 Nav2 controller parameter를 코드 내부에서 변경했습니다.

속도 설정은 다음과 같습니다.

- 일반 주행 속도: 0.30 m/s
- 순찰 구간 속도: 0.15 m/s
- 일반 회전 속도: 1.00
- 순찰 구간 회전 속도: 1.00

코드 내부에서 변경한 주요 Nav2 파라미터는 다음과 같습니다.

- FollowPath.max_vel_x
  - 전진 최대 속도

- FollowPath.max_speed_xy
  - 평면 이동 최대 속도

- FollowPath.max_vel_theta
  - 회전 최대 속도

순찰 루프에 진입할 때 위 파라미터를 조정하여 TurtleBot4가 특정 순찰 구간에서 저속으로 이동하도록 구현했습니다.

이를 통해 주행 중 카메라 기반 객체 탐지 안정성을 개선했습니다.

## Repository Structure

- README.md
- src/patrol_control_node.py
- docs/my_contribution.md
- config/waypoints.yaml

## Note

이 프로젝트는 팀 프로젝트로 진행되었습니다.

이 저장소는 팀 전체 시스템 중 제가 담당한 SLAM 맵 생성, False Loop Closure 문제 해결, Localization, Nav2 기반 자율주행, waypoint 수집, waypoint 순찰 제어, 순찰 속도 튜닝 부분만 정리한 것입니다.
