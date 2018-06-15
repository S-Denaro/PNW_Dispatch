% Formulates piecewise linear approximizations of power plant cost functions
% based on average heat rate data from EPA eGRID (2014), an NREL report
% (Lew, D. et al. Wind and Solar Impacts on Fossil-fuel Generators (2012), and some 
% plant specific data from units in CAISO (Klein report). 

% Zero-centered heat rate profiles
P=xlsread('heat_rate_curves.xlsx','profiles');

%Read eGRID data
[num,word,combined]=xlsread('PNW_generators','Gen_2011');

%Avg. heat rate curves for each power plant
A_HR = zeros(length(num),10);

%Total fuel consumption curves for each power plant
F = zeros(size(A_HR));

%No Load costs
No_Load = zeros(length(num),1);

%Incremental heat rate curve
I_HR = zeros(length(num),9);

%HR segments
HR_segments = nan(length(num),3);

word(1,:) = [];

%Add average heat rate to zero-centered profiles
for i=1:length(word)
    if strcmp(word(i,4),'cc')>0
        A_HR(i,:) = P(:,3)' + num(i,12);
    elseif strcmp (word(i,4),'coal')>0
        A_HR(i,:) = P(:,2)' + num(i,12);
    elseif strcmp(word(i,4),'ct')>0
        A_HR(i,:) = P(:,4)' + num(i,12);
    elseif strcmp(word(i,4),'steam') > 0
        A_HR(i,:) = P(:,5)' + num(i,12);
    end

    % Calculate total fuel consumption curve
    MW = [.1:.1:1]*num(i,1); 
    F(i,:) = MW.*A_HR(i,:);
    
    % Calculate no-load costs
    p = polyfit(MW,F(i,:),2);
    No_Load(i) = p(3);
    
    %Calculate incremental heat rate curve
    for j = 1:9
        I_HR(i,j) = (F(i,j+1)-F(i,j))/(MW(j+1)-MW(j));
    end
    
    %Linear function describing HR = f(MW)
    r = polyfit(MW(2:end),I_HR(i,:),1);
    
    %Three HR segments
    HR_segments(i,1) = r(1)*.5*num(i,1) + r(2);
    HR_segments(i,2) = r(1)*.7*num(i,1) + r(2);
    HR_segments(i,3) = r(1)*.9*num(i,1) + r(2);
end

%Output
%xlswrite('PNW_generators.xlsx',HR_segments,'out');
%xlswrite('MasterControl.xlsx',No_Load,'out2');

