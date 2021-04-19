import numpy as np
array = np.random.randint(0,10,(3,3))
print(array)

#평균이 0이고, 표준편차가 1인 표준정규를 띄는 배열
array2 = np.random.normal(0,1,(3,3))
print(array2)
print(array2.shape)

#배열의 모양바꾸기
array3 = array.reshape((1,9))
print(array3)

#배열 합치기(axis = 0 : vecter, axis = 1 : metrix, acis = 2 : tensor)
array4 = np.arange(9).reshape(3,3)
print(array4)
array5 = np.concatenate([array2, array4], axis=0)
print(array5)

#배열 나누기
array6, array7 = np.split(array5, [1], axis=1)
print(array6)
print(array7)
print("합계 : ", np.sum(array7, axis=0))
print(array6 + array7)

#배열 마스킹
array8 = array7 < 3
print(array8)
array7[array8] = 100
print(array7)

#복수 객체 저장 및 불러오기
array9 = np.arange(0,10)
array10 = np.arange(10,20)
np.savez('saved.npz', array1=array1, array2=array2)

data = np.load('saved.npz')
result = data['array1']

#Numpy 원소 오름차순 정렬
array5.sort()
print(array5)

#Numpy 원소 내림차순 정렬
print(array5[::-1])


