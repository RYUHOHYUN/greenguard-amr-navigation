# GreenGuard AMR Navigation

ROS2 Humble, Nav2, TurtleBot4, RPLIDAR를 활용한 SLAM 기반 AMR 자율주행 순찰 프로젝트입니다.

이 저장소는 GreenGuard 팀 프로젝트 중 제가 담당한 AMR 자율주행, 맵 생성, Localization, Waypoint 순찰 제어 부분을 정리한 저장소입니다.

## Project Overview

GreenGuard는 스마트팜 환경에서 AMR이 자율주행으로 순찰하며 작물 상태와 이상 상황을 확인하는 스마트팜 AMR 순찰 시스템입니다.

전체 시스템은 AMR 자율주행, 객체 탐지, 이벤트 처리, 로그 저장, 웹 기반 모니터링으로 구성됩니다.

이 저장소에서는 그중 제가 담당한 AMR Navigation 부분만 다룹니다.

## My Role

저는 프로젝트에서 TurtleBot4 기반 AMR 자율주행 및 순찰 제어를 담당했습니다.

주요 담당 내용은 다음과 같습니다.

- 스마트팜 테스트 환경에 맞는 MAP 구조를 설계했습니다.
- TurtleBot4와 연결된 Ubuntu Linux PC에서 SLAM을 실행하여 실내 맵을 생성했습니다.
- SLAM 과정에서 발생한 False Loop Closure 문제를 확인하고, 맵 구조 조정과 `slam.yaml` 파라미터 수정을 통해 안정적인 맵 생성을 수행했습니다.
- 생성한 맵을 기반으로 RViz2, Localization, Nav2를 실행하여 TurtleBot4의 위치 추정과 자율주행을 테스트했습니다.
- `/amcl_pose` 토픽을 이용해 TurtleBot4의 현재 위치를 확인했습니다.
- RViz2의 `clicked_point` 토픽과 Nav2 Goal 기능을 활용하여 순찰 지점 후보 좌표를 수집했습니다.
- 수집한 waypoint를 기반으로 TurtleBot4가 지정된 순찰 경로를 반복 주행하도록 Python 기반 ROS2 순찰 코드를 작성했습니다.
- 특정 순찰 구간에서 TurtleBot4의 주행 속도가 빨라 객체 탐지가 불안정한 문제가 발생했습니다.
- 이를 해결하기 위해 코드 내부에서 Nav2 controller parameter를 조정하여 특정 구간에서 TurtleBot4가 저속 주행하도록 구현했습니다.

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

맵 생성 과정에서 False Loop Closure 문제가 발생했으며, 이를 해결하기 위해 맵 구조를 조정하고 `slam.yaml` 파라미터를 수정하여 안정적인 맵을 생성했습니다.

### 2. Localization 및 Nav2 실행

생성된 맵을 기반으로 Localization과 Nav2를 실행하여 TurtleBot4가 맵 상에서 자신의 위치를 추정하고 목표 지점까지 이동할 수 있도록 구성했습니다.

### 3. Waypoint 수집

RViz2의 `clicked_point` 토픽과 Nav2 Goal 기능을 활용하여 순찰에 사용할 waypoint 좌표를 수집했습니다.

또한 `/amcl_pose` 토픽을 이용해 로봇의 현재 위치를 확인하며 waypoint를 검증했습니다.

### 4. Waypoint 기반 순찰

수집한 waypoint를 기반으로 TurtleBot4가 지정된 순찰 경로를 반복 주행하도록 구현했습니다.

로봇은 현재 위치에서 가장 가까운 waypoint를 선택한 뒤 순찰 루프에 진입합니다.

### 5. Nav2 속도 파라미터 조정

일부 순찰 구간에서 TurtleBot4의 속도가 빨라 카메라 기반 객체 탐지가 불안정한 문제가 있었습니다.

이를 해결하기 위해 코드 내부에서 Nav2 controller parameter를 조정하여 순찰 구간에서는 저속 주행하도록 구현했습니다.

조정한 주요 파라미터는 다음과 같습니다.

```text
FollowPath.max_vel_x
FollowPath.max_speed_xy
FollowPath.max_vel_theta
```

## Repository Structure

```text
greenguard-amr-navigation/
├── README.md
├── src/
│   └── patrol_control_node.py
├── docs/
│   └── my_contribution.md
└── config/
    └── waypoints.yaml
```

## Note

이 프로젝트는 팀 프로젝트로 진행되었습니다.

이 저장소는 팀 전체 시스템 중 제가 담당한 SLAM 맵 생성, Localization, Nav2 기반 자율주행, waypoint 순찰 제어, 순찰 속도 튜닝 부분만 정리한 것입니다.
