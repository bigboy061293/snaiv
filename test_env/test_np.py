import numpy as np

pumpFlowRateRaw = np.zeros((3,2))
print pumpFlowRateRaw
print np.shape(pumpFlowRateRaw)
pumpFlowRateRaw = [[1,2], [3,4] ,[5,6]]
print pumpFlowRateRaw
print np.shape(pumpFlowRateRaw)
pumpFlowRateRaw = np.roll(pumpFlowRateRaw,-1, axis = 1)
print pumpFlowRateRaw
pumpFlo = [1, 2]
pumpFlowRateRaw[2] = pumpFlo
print pumpFlowRateRaw

print np.shape(pumpFlo)
aa = np.average(pumpFlowRateRaw,axis = 0)
print aa
