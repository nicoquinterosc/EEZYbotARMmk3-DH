%% Matriz de D-H

close all; clear variables; clc
syms q1 q2 q3 real 
 
% Longitud de enlaces [m]
d1 = 0.034;
a2 = 0.08;
a3 = 0.14;

% Parámetros de DH
q=[q1 (pi/2+q2) (-pi/2+q3) pi/2];
d=[d1 0 0 0];
a=[0 a2 a3 0];
alfa=[pi/2 0 0 pi/2];
 
i=1;
A01=[cos(q(i)) -cos(alfa(i))*sin(q(i))  sin(alfa(i))*sin(q(i)) a(i)*cos(q(i));...
   sin(q(i))  cos(alfa(i))*cos(q(i)) -sin(alfa(i))*cos(q(i)) a(i)*sin(q(i));...
   0          sin(alfa(i))            cos(alfa(i))           d(i);...
   0 0 0 1]
 
i=2;
A12=[cos(q(i)) -cos(alfa(i))*sin(q(i))  sin(alfa(i))*sin(q(i)) a(i)*cos(q(i));...
   sin(q(i))  cos(alfa(i))*cos(q(i)) -sin(alfa(i))*cos(q(i)) a(i)*sin(q(i));...
   0          sin(alfa(i))            cos(alfa(i))           d(i);...
   0 0 0 1]
 
i=3;
A23=[cos(q(i)) -cos(alfa(i))*sin(q(i))  sin(alfa(i))*sin(q(i)) a(i)*cos(q(i));...
   sin(q(i))  cos(alfa(i))*cos(q(i)) -sin(alfa(i))*cos(q(i)) a(i)*sin(q(i));...
   0          sin(alfa(i))            cos(alfa(i))           d(i);...
   0 0 0 1]
 
i=4;
A34=[cos(q(i)) -cos(alfa(i))*sin(q(i))  sin(alfa(i))*sin(q(i)) a(i)*cos(q(i));...
   sin(q(i))  cos(alfa(i))*cos(q(i)) -sin(alfa(i))*cos(q(i)) a(i)*sin(q(i));...
   0          sin(alfa(i))            cos(alfa(i))           d(i);...
   0 0 0 1]


T=A01*A12*A23*A34;

 %% Pruebas 
 

q1 = deg2rad(-30); q2 = deg2rad(-36); q3 = deg2rad(-44); 
eval(T) % posición inicial

q1=0; q2=0; q3=0;
eval(T) 

%% Evaluación de una trayectoria. Giro de q1, q2 y q3
q1 = deg2rad(-30); q2 = deg2rad(-36); q3 = deg2rad(-44);
i=1;

for t1 = q1:deg2rad(1):deg2rad(30)
    for t2 = q2:deg2rad(1):deg2rad(56)
        for t3 = q3:deg2rad(1):deg2rad(0)
            q1 = t1;
            q2 = t2;
            q3 = t3;
            Aux=eval(T);
            % De cada paso tomo la posición
            x(i)=Aux(1,4);        %Eje x
            y(i)=Aux(2,4);        %Eje y
            z(i)=Aux(3,4);        %Eje z
            i=i+1;
        end
    end
end

figure(1)
plot3(x,y,z);
grid
axis equal
xlabel('x');
ylabel('y');
zlabel('z')


%% Evaluación de una trayectoria. Giro de q3, q2 y q1
q1 = deg2rad(-30); q2 = deg2rad(-36); q3 = deg2rad(-44);
i=1;

for t3 = q3:deg2rad(1):deg2rad(0)
    for t2 = q2:deg2rad(1):deg2rad(56)
        for t1 = q1:deg2rad(1):deg2rad(30)
            q1 = t1;
            q2 = t2;
            q3 = t3;
            Aux=eval(T);
            % De cada paso tomo la posición
            x(i)=Aux(1,4);        %Eje x
            y(i)=Aux(2,4);        %Eje y
            z(i)=Aux(3,4);        %Eje z
            i=i+1;
        end
    end
end

figure(2)
plot3(x,y,z);
grid
axis equal
xlabel('x');
ylabel('y');
zlabel('z')
