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

- 스마트팜 테스트 환경에 맞는 MAP 구조를 설계했습니다.
- TurtleBot4와 연결된 Ubuntu Linux PC에서 SLAM을 실행하여 실내 맵을 생성했습니다.
- 생성한 맵을 기반으로 RViz2, Localization, Nav2를 실행하여 TurtleBot4의 위치 추정과 자율주행을 테스트했습니다.
- `/amcl_pose` 토픽을 이용해 TurtleBot4의 현재 위치를 확인했습니다.
- RViz2의 `/clicked_point` 토픽과 Nav2 Goal 기능을 활용하여 순찰 waypoint 좌표를 수집했습니다.
- 수집한 waypoint를 기반으로 TurtleBot4가 지정된 순찰 경로를 반복 주행하도록 Python 기반 ROS2 순찰 코드를 작성했습니다.
- MAP 생성 과정에서 False Loop Closure 문제가 발생하여 `slam.yaml` 파라미터를 수정하고, 안정적으로 맵이 생성되도록 조정했습니다.
- 특정 순찰 구간에서 TurtleBot4의 주행 속도가 빨라 객체 탐지가 불안정한 문제가 발생했습니다.
- 이를 해결하기 위해 코드 내부에서 Nav2 controller parameter를 조정하여 순찰 구간에서 TurtleBot4가 저속 주행하도록 구현했습니다.

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

이후 생성된 맵을 기반으로 Localization과 Nav2를 실행하여 TurtleBot4가 맵 상에서 자신의 위치를 추정하고 목표 지점까지 이동할 수 있도록 구성했습니다.

### 2. False Loop Closure 문제 해결

초기 맵 생성 과정에서 False Loop Closure 문제가 발생했습니다.

이 문제를 해결하기 위해 맵 구조를 조정하고, `slam.yaml`의 SLAM 관련 파라미터를 수정했습니다.

수정한 주요 파라미터는 다음과 같습니다.

| Parameter | Change | Purpose |
|---|---|---|
| `minimum_travel_distance` | `0.0 → 0.15` | scan node가 너무 자주 생성되는 문제 완화 |
| `minimum_travel_heading` | `0.0 → 0.12` | 작은 회전마다 node가 생성되는 문제 완화 |
| `loop_search_maximum_distance` | `3.0 → 1.5` | 너무 먼 loop closure 후보 제거 |
| `loop_match_minimum_chain_size` | `10 → 15` | loop closure 인정 기준 강화 |
| `loop_match_maximum_variance_coarse` | `3.0 → 1.5` | 불확실한 coarse match 제거 |
| `loop_match_minimum_response_coarse` | `0.35 → 0.50` | 1차 매칭 점수 기준 강화 |
| `loop_match_minimum_response_fine` | `0.45 → 0.60` | 최종 매칭 점수 기준 강화 |

이를 통해 불안정한 loop closure 후보를 줄이고, SLAM 맵 생성 안정성을 개선했습니다.

### 3. Localization 및 Nav2 실행

생성된 맵을 기반으로 Localization과 Nav2를 실행했습니다.

RViz2에서 TurtleBot4의 현재 위치를 확인하고, Nav2 Goal 기능을 이용해 로봇이 목표 지점까지 이동하는지 테스트했습니다.

또한 `/amcl_pose` 토픽을 통해 로봇의 현재 위치 정보를 확인하며 waypoint 기반 순찰 로직에 활용했습니다.

### 4. Waypoint 수집

순찰 경로를 구성하기 위해 RViz2의 `/clicked_point` 토픽과 Nav2 Goal 기능을 활용했습니다.

수집한 waypoint는 TurtleBot4가 실제로 이동 가능한 위치인지 확인한 뒤 순찰 경로에 반영했습니다.

사용한 주요 정보는 다음과 같습니다.

```text
/amcl_pose
/clicked_point
RViz2 Nav2 Goal
teleop command
```

### 5. Waypoint 기반 순찰

수집한 waypoint를 기반으로 TurtleBot4가 지정된 순찰 경로를 반복 주행하도록 Python 기반 ROS2 순찰 코드를 작성했습니다.

로봇은 현재 위치에서 가장 가까운 waypoint를 선택한 뒤 순찰 루프에 진입합니다.

순찰 경로는 다음과 같이 구성했습니다.

```text
point2 -> point3 -> point35_mid -> point24_mid -> point35_mid -> point5 -> point4
```

### 6. Nav2 속도 파라미터 조정

순찰 중 특정 구간에서 TurtleBot4의 속도가 빨라 카메라 기반 객체 탐지가 불안정한 문제가 발생했습니다.

이를 해결하기 위해 순찰 구간에서는 TurtleBot4가 더 천천히 이동하도록 Nav2 controller parameter를 코드 내부에서 변경했습니다.

속도 설정은 다음과 같습니다.

```text
NORMAL_MAX_VEL_X = 0.30
NORMAL_MAX_VEL_THETA = 1.00

PATROL_MAX_VEL_X = 0.15
PATROL_MAX_VEL_THETA = 1.00
```

기존에는 일반 주행 속도인 `0.30 m/s`로 이동했지만, 순찰 구간에서는 `0.15 m/s`로 감속하여 객체 탐지 안정성을 개선했습니다.

코드 내부에서 변경한 주요 Nav2 파라미터는 다음과 같습니다.

```text
FollowPath.max_vel_x
FollowPath.max_speed_xy
FollowPath.max_vel_theta
```

각 파라미터의 의미는 다음과 같습니다.

| Parameter | Meaning |
|---|---|
| `FollowPath.max_vel_x` | 전진 최대 속도 |
| `FollowPath.max_speed_xy` | 평면 이동 최대 속도 |
| `FollowPath.max_vel_theta` | 회전 최대 속도 |

순찰 루프에 진입할 때 위 파라미터를 조정하여 TurtleBot4가 특정 순찰 구간에서 저속으로 이동하도록 구현했습니다.

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

이 저장소는 팀 전체 시스템 중 제가 담당한 SLAM 맵 생성, False Loop Closure 문제 해결, Localization, Nav2 기반 자율주행, waypoint 수집, waypoint 순찰 제어, 순찰 속도 튜닝 부분만 정리한 것입니다.
