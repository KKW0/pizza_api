# 2023은 계묘년 입니다.
# 년도를 입력받아 60간지를 반환하는 프로그램을 만들어 보세요
# 10간지: 갑을병정무기경신임계
# 12간지: 자축인묘진사오미신유술해


# 2023년을 기준(계묘)
# 기준에서 1년이 지나면 10간지에서 1칸 넘어감 - 원형 리스트 사용
# 기준에서 1년이 지나면 12간지에서 1칸 넘어감 - 원형 리스트 사용
# 입력 받은 년도와 기준 년도의 차이를 확인하여 그 차이 만큼 10간지와 12간지에서 계산된 텍스트를 받아 AB로 리턴

# 10간지에서 계 다음은 갑으로 넘어감
# 12간지에서 해 다음은 자로 넘어감


gan_10 = ["경", "신", "임", "계", "갑", "을", "병", "정", "무", "기"]
gan_12 = ["신", "유", "술", "해", "자", "축", "인", "묘", "진", "사", "오", "미"]


year = input("연도를 입력하시오: ")

if type(input) == int:
    print("입력하신 " + year + "년은 " + "[" + gan_10[int(year)%10] + gan_12[int(year)%12] + "] 해 입니다.")
    # print(gan_10[int(year)%10])
    # print(gan_12[int(year)%12])
    # print("해 입니다.")p
    else:
    print("Warning: 숫자 형태의 연도를 입력하시오.")