%trialfirS An M-file S-function 
function [sys,x0,str,ts] = PLC3(t,x,u,flag)
 


switch flag,

 %%%%%%%%%%%%%%%%%%
 % Initialization %
 %%%%%%%%%%%%%%%%%%
 case 0,
   [sys,x0,str,ts]=mdlInitializeSizes();

 %%%%%%%%%%%%%%%
 % Derivatives %
 %%%%%%%%%%%%%%%
 case 2,
   sys=mdlDerivatives(t,x,u);

 %%%%%%%%%%%
 % Outputs %
 %%%%%%%%%%%
 case 3,
   [sys]=mdlOutputs(t,x,u);
 %%%%%%%%%%%%%%%%%%%
 % Unhandled flags %
 %%%%%%%%%%%%%%%%%%%
 case {1,2,4,9},
   sys = [];

   
 %%%%%%%%%%%%%%%%%%%%
 % Unexpected flags %
 %%%%%%%%%%%%%%%%%%%%
 otherwise
   error(['Unhandled flag = ',num2str(flag)]);

end
% end trialfirS function

%
%=============================================================================
% mdlInitializeSizes
% Return the sizes, initial conditions, and sample times for the S-function.
%=============================================================================
%
function [sys,x0,str,ts]=mdlInitializeSizes()
sizes = simsizes;  % creating a structure variable
sizes.NumContStates  = 0;
sizes.NumDiscStates  = 1; 
sizes.NumOutputs     = 1;
sizes.NumInputs      = 1;
sizes.DirFeedthrough = 0;
sizes.NumSampleTimes = 1;
%
sys = simsizes(sizes);
x0= [0];
str = [];
ts  = [1 0];
% end mdlInitializeSizes

%=============================================================================
% mdlOutputs
% Return the block outputs.
%=============================================================================
%

function [sys]=mdlDerivatives(t,x,u)
A3 = 154; %cm^2
s12 = 0.5; %no-dim
H3_max = 100; % cm
Q3_max = 10; %cm^3/s
a1 = 0.45; %no-dim
g = 980.665; % grav const

h = u(1);
pump = x(1); 
if(h >= 0.01*H3_max)
    pump = 1;% Q3_max / A3;
elseif (h < 0.00000001*H3_max)
   pump = 0;
end
sys = [pump];

function [sys]=mdlOutputs(t,x,u)
sys = x;
return 
% end mdlOutputs