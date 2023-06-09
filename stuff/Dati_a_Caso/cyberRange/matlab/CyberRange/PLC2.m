%trialfirS An M-file S-function 
function [sys,x0,str,ts] = PLC2(t,x,u,flag)
 


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
x0= [1];
str = [];
ts  = [1 0];
% end mdlInitializeSizes

%=============================================================================
% mdlOutputs
% Return the block outputs.
%=============================================================================
%

function [sys]=mdlDerivatives(t,x,u)
A1 = 154; %cm^2
s12 = 0.5; %no-dim
H2_max = 100; % cm
Q1_max = 100; %cm^3/s
a1 = 0.45; %no-dim
g = 980.665; % grav const

h = u(1);
req = x(1); 
% if(h >= 0.15*H2_max)
if(h >= 0.2*H2_max)
%if(h >= 0.9*H1_max) 
    req = 0;
elseif (h < 0.1*H2_max)
   req = 1;
% else
%     req = 3;
end
    
sys = [req];

function [sys]=mdlOutputs(t,x,u)
sys = x;
return 
% end mdlOutputs