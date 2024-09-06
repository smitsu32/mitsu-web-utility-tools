hold off;
clear;

load dispatchPrice.mat;
bar(poolPrice,0.5);
xlim([0.5,48.5]);
xlabel('Price per MWH at each period');

% Example value
fuelPrice=3;
totalFuel=3.95e4;
nPeriods=length(poolPrice);% Period number
nGens=2; % 2 Generators
gen=[61,152;50,150]; % generater 1Low:61MW,1High:152MW, ...
fuel=[427,806;325,765]; % consume fuel 2Low:325,2High:765
startcost=1e4; % cost of start generators


efficiency=gen./fuel; % efficiency of unit fuel use
rr=efficiency'; % for plotting
h=bar(rr); 
h(1).FaceColor='g';
h(2).FaceColor='c';
legend(h,'Generator 1','Generator 2','Location','northeastoutside'); % legendary

ax=gca; % current axes(for setting)
ax.XTick=[1,2]; % posision of tick marks
ax.XTickLabel={'Low','High'};
ylim([0.1,0.2]);
ylabel('Efficiency');



% Optimization
%% y:schedule 48*2*2 items, 0:no 1:better on (Gen1,Gen2)(Low,High) 
y=optimvar('y',nPeriods,nGens,{'Low','High'},'Type','integer','Lowerbound',0,'Upperbound',1);
%% z:restart generators for each Period? 
z=optimvar('z',nPeriods,nGens,'Type','integer','Lowerbound',0,'Upperbound',1);

% constraints designate Low or High
powercons = y(:,:,'Low') + y(:,:,'High') <= 1;

% separate period
yFuel=zeros(nPeriods,nGens,2);
yFuel(:,1,1)=fuel(1,1); % gen1 low setting
yFuel(:,1,2)=fuel(1,2);
yFuel(:,2,1)=fuel(2,1);
yFuel(:,2,2)=fuel(2,2);

fuelUsed=sum(sum(sum(y.*yFuel))); % because of 3->1 dimention(select Low or High 1)

% Constraints, fuel is lower than total one
fuelcons=fuelUsed<=totalFuel;


% make optim array(sum_k y(i+1,j,k)-y(i,j,k))
w=optimexpr(nPeriods,nGens);
idx=1:(nPeriods-1); % because of using idx+1 and start=1

%% w=diff(y[Low or High])
w(idx,:)=y(idx+1,:,'Low')-y(idx,:,'Low')+y(idx+1,:,'High')-y(idx,:,'High');
%% final->start is continuous
w(nPeriods,:)=y(1,:,'Low')-y(nPeriods,:,'Low')+y(1,:,'High')-y(nPeriods,:,'High');

% if z(i,j)==1; y(i,j,:)=0->y(i+1,j,:)=1 (i:Period, j: 1:On 0:Off)
% w(i,j)-z(i,j)<=0-1<=0 
switchcons=w-z<=0;

% MW energy per Periods from Gen1 or 2, Low or High
generatorlevel=zeros(size(yFuel));
generatorlevel(:,1,1)=gen(1,1);
generatorlevel(:,1,2)=gen(1,2);
generatorlevel(:,2,1)=gen(2,1);
generatorlevel(:,2,2)=gen(2,2);

% revenue=y(1 or 0).*genlevel(MW).*poolPrice($)
revenue=optimexpr(size(y));
for i=1:nPeriods % for i in range(1,nPeriods+1):, for(i=0,i<nPeriod+1,i++):
    revenue(i,:,:)=poolPrice(i)*y(i,:,:).*generatorlevel(i,:,:); % optimvar is *, not .*
end

fuelCost=fuelUsed*fuelPrice;
startingCost=z*startcost; % z: starting number(2dim)
% profit=revenue-cost
profit=sum(sum(sum(revenue)))-fuelCost-sum(sum(startingCost));



% optimization 
dispatch=optimproblem('ObjectiveSense','maximize');
dispatch.Objective=profit;
dispatch.Constraints.switchcons=switchcons;
dispatch.Constraints.fuelcons=fuelcons;
dispatch.Constraints.powercons=powercons;

% only display final value
option=optimoptions('intlinprog','Display','final');

%% sol=i,j,k, fval=y(i,j,k), exitflag=1(success termination), output: window->
[sol,fval,exitflag,output]=solve(dispatch,'Options',option);

% plot sum(energy)
subplot(3,1,1)
bar(sol.y(:,1,1)*gen(1,1)+sol.y(:,1,2)*gen(1,2),0.5,'g')
xlim([0.5,48.5])
ylabel('MWh')
title('Generator 1 Optimal Schedule','FontWeight','bold')

subplot(3,1,2)
bar(sol.y(:,2,1)*gen(2,1)+sol.y(:,2,2)*gen(2,2),0.5,'c')
xlim([0.5,48.5])
ylabel('MWh')
title('Generator 2 Optimal Schedule','FontWeight','bold')

subplot(3,1,3)
bar(poolPrice,0.5)
xlim([0.5,48.5])
ylabel('$/MWh')
title('Energy Price','FontWeight','bold')


starttimes=find(round(sol.z)==1); % time for start gen
% [row, col]=ind2sub[size(n*n),index] return index's col and row
[thePeriod,theGenerator]=ind2sub(size(sol.z),starttimes) % 48*2 start time and gen
%% Only once for each generator


% if startCost reduce, ...
% definite values again
startCost=500;

% same as above
startingCost=z*startcost;
profit=sum(sum(sum(revenue)))-fuelCost-sum(sum(startingCost));
dispatch.Objective=profit;

[solnew,fvalnew,exitflagnew,outputnew]=solve(dispatch,'options',option);

subplot(3,1,1)
bar(solnew.y(:,1,1)*gen(1,1)+solnew.y(:,1,2)*gen(1,2),.5,'g')
xlim([.5,48.5])
ylabel('MWh')
title('Generator 1 Optimal Schedule','FontWeight','bold')
subplot(3,1,2)
bar(solnew.y(:,2,1)*gen(2,1)+solnew.y(:,2,2)*gen(2,2),.5,'c')
title('Generator 2 Optimal Schedule','FontWeight','bold')
xlim([.5,48.5])
ylabel('MWh')
subplot(3,1,3)
bar(poolPrice,.5)
xlim([.5,48.5])
title('Energy Price','FontWeight','bold')
xlabel('Period')
ylabel('$ / MWh')
