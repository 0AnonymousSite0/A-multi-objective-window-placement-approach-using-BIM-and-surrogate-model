function [Y,Xf,Af] = TheAnnualTotalEnergyConsumption(X,~,~)

x1_step1.xoffset = [8.4;1.7;7.2;0.8];
x1_step1.gain = [0.0938967136150235;0.102040816326531;0.10752688172043;0.103626943005181];
x1_step1.ymin = -1;
b1 = -0.35325540570301833254;
IW1_1 = [1.7324153993281492525 3.9329151904857280186 -1.5210463816018680028 -3.6775955932740220788];
b2 = 0.69893644389576448095;
LW2_1 = 2.4946252708143936694;
y1_step1.ymin = -1;
y1_step1.gain = 0.433321886881418;
y1_step1.xoffset = -2.05018571523958;
isCellX = iscell(X);
if ~isCellX
    X = {X};
end
TS = size(X,2);
if ~isempty(X)
    Q = size(X{1},1); 
else
    Q = 0;
end
Y = cell(1,TS);
for ts=1:TS

    X{1,ts} = X{1,ts}';
    Xp1 = mapminmax_apply(X{1,ts},x1_step1);
    a1 = tansig_apply(repmat(b1,1,Q) + IW1_1*Xp1);
    a2 = repmat(b2,1,Q) + LW2_1*a1;
    Y{1,ts} = mapminmax_reverse(a2,y1_step1);
    Y{1,ts} = Y{1,ts}';
end

Xf = cell(1,0);
Af = cell(2,0);
if ~isCellX
    Y = cell2mat(Y);
end
end

function y = mapminmax_apply(x,settings)
y = bsxfun(@minus,x,settings.xoffset);
y = bsxfun(@times,y,settings.gain);
y = bsxfun(@plus,y,settings.ymin);
end

function a = tansig_apply(n,~)
a = 2 ./ (1 + exp(-2*n)) - 1;
end

function x = mapminmax_reverse(y,settings)
x = bsxfun(@minus,y,settings.ymin);
x = bsxfun(@rdivide,x,settings.gain);
x = bsxfun(@plus,x,settings.xoffset);
end
