## 스파르타 코딩클럽
## 내일배움캠프 AI 웹개발자양성과정 2회차
## 2022.04.25~ python 게임만들기

### 1. 프로젝트명
스파르타 파이터 - pygame을 이용한 격투게임 만들기

### 2. 목적
직접 게임을 설계해보고 python을 이용하여 설계한 내용을 구현해봄으로써 설계과 구현에 익숙해지고 python 실력을 향상시키고자 함

### 3. 설명 
2명의 플레이어가 각자의 캐릭터로 싸우는 2d 횡스크롤 게임

- 예시
<figure style="display:block; text-align:center;">
  <img src="https://t1.daumcdn.net/cfile/tistory/1526011E4BD2531A6C"
       style="width: 400px; margin:0px auto">
  <figcaption style="text-align:center; font-size:15px; color:#808080">
    출처 : 고전게임랜드 (스트리트파이터2)
  </figcaption>
</figure>


### 4. 게임 설계 
-  조작 : 좌우 이동, 점프 가능

- 캐릭터 타격/피격/수비 범위 : 상단/중단/하단

- 타격 : 상단/중단/하단 3개의 각각 다른 범위의 공격 가능하고 공격범위에 상대 캐릭터가 있으면 타격 성공

- 피격 : 상대 캐릭터가 3개의 범위 중 한 곳으로 공격했을 경우 자신의 캐릭터가 그 공격범위에 있으면 피격 판정

- 수비 : 공격을 예상해서 3개의 범위 중 한 곳으로 수비 가능, 수비한 범위에 상대 캐릭터가 공격하면 수비 성공, 수비 성공하면 궁게이지 업, 공격과 동시에 불가능

- 궁극기 : 공격에 성공하거나, 피격 당하거나, 수비에 성공했을 때 궁게이지 참, 궁게이지가 꽉차면 필살기 가능, 3개의 범위 동시공격, 수비불가능, 회피만 가능

- 시간제한 : 60초 - 시간 다될때까지 승부가 안나면 체력 많은 캐릭터가 승리

- 크리티컬 데미지 : 공격 성공시 확률적으로 크리티컬 데미지 적용  (10%확률로 200% 데미지)

- 피격 시 경직 -> 일정시간동안 못 움직임, but 일정 피격 이상되면 피격 면역


### additional)
- 공격콤보 -> 넘어뜨리기 : 더 많이 타격 가능
- 여러캐릭터를 만들어서 공격패턴, 종류 다양화
- 태그매치
 


