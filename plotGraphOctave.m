datafile = load('pendulum_data_09-05-2022_12:51:20.txt');

x = linspace(0,500,0.4)
%hour = datafile(:,1);
sensorOutput = datafile(:,1);
%pwm = datafile(:,3)


hold on

%plot(x,sensorOutput, '_',systemOutput, 'ro');
%plot(systemOutput);
plot(sensorOutput)
%xlabel('Amostragem');       %  add axis labels and plot title
%ylabel('valor da amostra');

hold off
%plot(x,y,'-',x,yn,'ro');
