from matplotlib import pyplot as plt

eixo_x_dias = [2,4,23,15,30,28]
eixo_y_temp_max = [28,36,12,31,20,7]
eixo_y_temp_min = [18,22,7,23,12,-10]

plt.title("Temperaturaa Maximas é Minimas")
plt.xlabel("Datas")
plt.ylabel("Temperaturaa Maximas é Minimas")

plt.plot(eixo_x_dias,eixo_y_temp_max, linestyle = "--", marker = "o")
plt.plot(eixo_x_dias,eixo_y_temp_min, linestyle = "--", marker = "o")

plt.legend(["Temp Max","Temp Min"])
plt.grid(True)
plt.show()