from serial import Serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime

# serialPort.open()
init = False
step = False
outputOld = str()
systemOutput = str()

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
sample = []  # store trials here (n)
gyroYData = []  # store relative frequency here
systemOutputData = []  # for theoretical probability


# This fuction initialize the serial port
def initializeSerialPort():
    global serialPort
    serialPort = Serial('/dev/ttyUSB1', baudrate=115200, timeout=10000)
    try:
        if serialPort.isOpen:
            print('\nTudo Certo, Serial port foi inicializada. Configuração:\n')
            print(serialPort, "\n")  # print serial parameters
    except serialPort.SerialException:
        print('\nNão foi possível inializar a Serial port.\n')


# This function handles the lines read by the serial.
def lineTreatment(line):
    treatedLine = []
    line_as_list = line.split(b',')

    for idx, val in enumerate(line_as_list):
        if idx == 0:
            treatedLine.append(int(val))
        else:
            treatedLine.append(float(val))
    return treatedLine    


# This function is called periodically from FuncAnimation
def animate(i, sample, gyroYData):
    # Aquire and parse data from serial port
    line = serialPort.readline()  # ascii
    print(line)
    line_as_list = line.split(b',')
    # print(line_as_list[0])

    # if line_as_list[0] != '\r\n':
    #     print('entrou no if')
    j = float(line_as_list[0])
    print(j)

    gyroData = line_as_list[1]
    gyroData_as_list = gyroData.split(b'\n')
    gyroData_float = float(gyroData_as_list[0])
    print(gyroData_float)

    systemOutput = line_as_list[2]
    systemOutput_as_list = systemOutput.split(b'\n')
    systemOutput_float = float(systemOutput_as_list[0])

    # Add x and y to lists
    sample.append(j)
    gyroYData.append(gyroData_float)
    systemOutputData.append(systemOutput_float)

    # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(sample, gyroYData, label="Dado do Giroscópio")
    ax.plot(sample, systemOutputData, label="Saida do Sistema")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    plt.title('Pêndulo Hélice')
    plt.ylabel('°/s')
    plt.xlabel('Tempo (ms)')

    plt.legend()
    # plt.axis([1, None, 0, 1.1])  # Use for arbitrary number of trials
    # plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo

# Set up plot to call animate() function periodically
def plotRealTimeGraph():
    ani = animation.FuncAnimation(fig, animate, fargs=(sample, gyroYData), interval=100)
    plt.show()

def printLine():
    while True:
        print(serialPort.readline())

def saveDataInFile():
    fileName = 'pendulum_data_' + datetime.now().strftime("%m-%d-%Y_%H:%M:%S") + '.txt'
    while True:
        try:
            readedLine = serialPort.readline()
            treatedLine = lineTreatment(readedLine)
            with open(fileName, 'a') as file:
                file.write('{} {} {}\n'.format(treatedLine[0], treatedLine[1], treatedLine[2]))
        except:
            file.close()
            print('Keyboard Interrupt')
            break

if __name__ == '__main__':
    initializeSerialPort()
    saveDataInFile()