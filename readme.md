# 💪 스파르타 파이터
> 2명의 플레이어가 각자의 캐릭터로 싸우는 2d 횡스크롤 게임

<br />

# 📖 프로젝트 정보

### 1. 제작기간
> 2022.04.25 ~ 04.27

### 2. 개발자
> [김동우](https://github.com/kimphysicsman)

### 3. 목적
> 직접 게임을 설계해보고 python을 이용하여 설계한 내용을 구현해봄으로써 설계과 구현에 익숙해지고 python 실력을 향상시키고자 함

### 4. 데모
> <img width="600px" src="https://user-images.githubusercontent.com/68724828/186097034-1239a3e6-c267-41bc-b04b-995d4b602a24.png" />

<br />

# ⚙ 게임 설계 
> - 조작 : 좌우 이동, 점프 가능
> - 캐릭터 타격/피격/수비 범위 : 상단/중단/하단
> - 타격 : 상단/중단/하단 3개의 각각 다른 범위의 공격 가능하고 공격범위에 상대 캐릭터가 있으면 타격 성공
> - 피격 : 상대 캐릭터가 3개의 범위 중 한 곳으로 공격했을 경우 자신의 캐릭터가 그 공격범위에 있으면 피격 판정
> - 수비 : 공격을 예상해서 3개의 범위 중 한 곳으로 수비 가능, 수비한 범위에 상대 캐릭터가 공격하면 수비 성공, 수비 성공하면 궁게이지 업, 공격과 동시에 불가능
> - 궁극기 : 공격에 성공하거나, 피격 당하거나, 수비에 성공했을 때 궁게이지 참, 궁게이지가 꽉차면 필살기 가능, 3개의 범위 동시공격, 수비불가능, 회피만 가능
> - 시간제한 : 60초 - 시간 다될때까지 승부가 안나면 체력 많은 캐릭터가 승리
> - 크리티컬 데미지 : 공격 성공시 확률적으로 크리티컬 데미지 적용  (10%확률로 200% 데미지)
> - 피격 시 넉백 -> 일정시간동안 못 움직임, but 일정 피격 이상되면 피격 면역


<br />

# 📕 기타 자료
### 1. 개발일지
> [python 게임 만들기 - (1) 설계](https://velog.io/@kimphysicsman/%EB%82%B4%EC%9D%BC%EB%B0%B0%EC%9B%80%EC%BA%A0%ED%94%84-python-%EA%B2%8C%EC%9E%84-%EB%A7%8C%EB%93%A4%EA%B8%B0-1-%EC%84%A4%EA%B3%84)  
> [python 게임 만들기 - (2) 1일차 개발일지](https://velog.io/@kimphysicsman/%EB%82%B4%EC%9D%BC%EB%B0%B0%EC%9B%80%EC%BA%A0%ED%94%84-python-%EA%B2%8C%EC%9E%84-%EB%A7%8C%EB%93%A4%EA%B8%B0-2-1%EC%9D%BC%EC%B0%A8-%EA%B0%9C%EB%B0%9C%EC%9D%BC%EC%A7%80)  
> [python 게임 만들기 - (3) 2일차 개발일지](https://velog.io/@kimphysicsman/%EB%82%B4%EC%9D%BC%EB%B0%B0%EC%9B%80%EC%BA%A0%ED%94%84-python-%EA%B2%8C%EC%9E%84-%EB%A7%8C%EB%93%A4%EA%B8%B0-3-2%EC%9D%BC%EC%B0%A8-%EA%B0%9C%EB%B0%9C%EC%9D%BC%EC%A7%80)  
> [python 게임 만들기 - (4) 3일차 개발일지](https://velog.io/@kimphysicsman/%EB%82%B4%EC%9D%BC%EB%B0%B0%EC%9B%80%EC%BA%A0%ED%94%84-python-%EA%B2%8C%EC%9E%84-%EB%A7%8C%EB%93%A4%EA%B8%B0-4-3%EC%9D%BC%EC%B0%A8-%EA%B0%9C%EB%B0%9C%EC%9D%BC%EC%A7%80)  

### 2. 발표영상
> <a link="https://youtu.be/rO3BVG2kE4o"> <img src="https://user-images.githubusercontent.com/68724828/186100279-92ae19a4-339f-4ae0-ac6b-91859cab55ce.png" /> </a>



