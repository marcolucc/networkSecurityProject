%trialfirS An M-file S-function 
function [sys,x0,str,ts] = PLC1(t,x,u,flag)
 


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
sizes.NumDiscStates  = 2; 
sizes.NumOutputs     = 2;
sizes.NumInputs      = 2;
sizes.DirFeedthrough = 0;
sizes.NumSampleTimes = 1;
%
sys = simsizes(sizes);
x0= [1, 1];
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
H1_max = 100; % cm
Q1_max = 100; %cm^3/s
a1 = 0.45; %no-dim
g = 980.665; % grav const
h = u(1);
req = u(2);
pump = x(1);
valve = x(2);
if(h >= 0.8*H1_max)
    pump = 0;
    if ( req == 0)
        valve = 0;
%     else
    elseif (req == 1)
        valve = 1;
    end
elseif (h < 0.4*H1_max)
   pump = 1;%(Q1_max/A1);
     if ( req == 0)
        valve = 0;
     %else
     elseif (req == 1)
        valve = 1;
     end
end
if (req == 0)
    valve = 0;
elseif (req == 1 && h >= 0.4*H1_max)
     valve = 1;
end


sys = [pump, valve];

function [sys]=mdlOutputs(t,x,u)
y = x;
sys = y;
return 
% end mdlOutputs