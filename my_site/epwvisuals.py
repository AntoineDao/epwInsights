from ladybug.epw import EPW, EPWDataTypes
import matplotlib.pyplot as plt
import numpy as np
import mpld3
import json


epwFileAddress = "C:\Users\Antoine\Desktop\Python Mega Course\Flask\my_site\epw\uploads\DEU_Dusseldorf.104000_IWEC.epw"

def print_epw_temp(epwFileAddress):

    epwData = EPW(epwFileAddress)

    dryBulbTemp = epwData.dryBulbTemperature.values

    t = np.arange(0,len(dryBulbTemp), 1)
    s = dryBulbTemp
    fig = plt.figure(figsize=(10,5))
    plt.plot(t,s)
    plt.xlabel('time')
    plt.ylabel('Dry Bulb Temperature')
    plt.title('Hourly Dry Bulb Temperature in ' + epwData.location.city)
    plt.grid(True)
    output = json.dumps(mpld3.fig_to_dict(fig))

    return output
def epw_city(epwFileAddress):
    epwData = EPW(epwFileAddress)

    return epwData.location.city

#def yearly_heatmap(epwFileAddress, metric):
    #Some attemp at making a heatmap...

    # hours = np.arange(0,25,1)
    # days = np.arange(0,366,1)
    #
    # dryBulb = [dryBulb[i:i+24] for i in range(0,len(dryBulb),24)]
    #
    # days,hours = np.meshgrid(days,hours)
    #
    # dryBulb = np.array(dryBulb).transpose()
    # print(dryBulb[3])
    # #print(len(dryBulb[364]))
    # #
    # # hours = [1,2,3,4,5,6]
    # # days = [1,2,3,4]
    # #
    # # dryBulb =  [[2,3,1,1,10,1],[2,5,7,1,4,6],[7,3,2,1,8,5],[4,3,2,1,12,5]]
    # # dryBulb = np.array(dryBulb).transpose()
    # # plt.pcolormesh(days,hours,dryBulb)
    # # plt.colorbar()
    # # plt.show()
