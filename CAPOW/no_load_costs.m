% Formulates piecewise linear approximizations of power plant cost functions
% based on average heat rate data from EPA eGRID (2014) and NREL report
% (Lew, D. et al. Wind and Solar Impacts on Fossil-fuel Generators (2012)).

% Polynomials (Y = Ax^2 + Bx + C); y = heat rate (MMBtu/MWh); x = % of maximum generating capacity
% Rows: Coal, NGCC, NGCT, NG (steam)
      %A       %B      %C
M = [1.6071, -3.4107, 11.207;
     5.3571, -10.193, 12.45;
     4.9107, -10.595, 15.357;
     2.4107, -4.6304, 12.161];
 
% Define desired number of segments
no_segments = 10;
 
% Piecewise linear functions
S = zeros(4,no_segments);

% For each power plant
for i = 1:4
    % For each segment
    for j = 1:no_segments
        S(i,j) = M(i,1)*((j)/no_segments)^2 + M(i,2)*((j)/no_segments) + M(i,3);
    end
end

% Create "zero-mean" profiles that can be added to average heat rates from
% eGRID; assumes average heat rates from eGRID are for plant producing at
% 70% of maximum capacity
S_zero = zeros(size(S));
for i = 1:4
    S_zero(i,:) = S(i,:) - (M(i,1)*(.7)^2 + M(i,2)*(.7) + M(i,3));
end

%Read eGRID data
[num,word,combined]=xlsread('MasterControl','TAC North');
word(1,:) = [];

MC = zeros(length(num),no_segments);
NoLOAD = zeros(length(num),1);

%Add average heat rate to NREL profiles
for i=1:length(num)
    if strcmp(word(i,10),'NATURAL GAS')>0
        if strcmp(word(i,11),'COMBINED CYCLE') > 0
            MC(i,:) = S_zero(2,:) + num(i,20);
                
                %Convert to total fuel costs for no-load calculation (model
                %parameters for no_segments = 10)
                cap = num(i,7);
                x = [.1:.1:1]*cap;
                F = zeros(no_segments,1);
                
                %Total fuel consumption by production level
                for j=1:no_segments
                    F(j) = cap*(j/no_segments)*MC(i,j);
                end
                p = polyfit(x',F,2);
                NoLOAD(i) = p(3);
                
            
        elseif strcmp(word(i,11),'COMBUSTION TURBINE') > 0
            
            %Marginal Heat Rate
            MC(i,:) = S_zero(3,:) + num(i,20);
            
                %Convert to total fuel costs for no-load calculation (model
                %parameters for no_segments = 10)
                cap = num(i,7);
                x = [.1:.1:1]*cap;
                F = zeros(no_segments,1);
                
                %Total fuel consumption by production level
                for j=1:no_segments
                    F(j) = cap*(j/no_segments)*MC(i,j);
                end
                p = polyfit(x',F,2);
                NoLOAD(i) = p(3);
            
        elseif strcmp(word(i,11),'STEAM') > 0
            
            %Marginal Heat Rate
            MC(i,:) = S_zero(4,:) + num(i,20);
            
                %Convert to total fuel costs for no-load calculation (model
                %parameters for no_segments = 10)
                cap = num(i,7);
                x = [.1:.1:1]*cap;
                F = zeros(no_segments,1);
                
                %Total fuel consumption by production level
                for j=1:no_segments
                    F(j) = cap*(j/no_segments)*MC(i,j);
                end
                p = polyfit(x',F,2);
                NoLOAD(i) = p(3);
        end
        
    elseif strcmp (word(i,10),'COAL')>0
            
            %Marginal Heat Rate
            MC(i,:) = S(1,:) + num(i,20);
            
                %Convert to total fuel costs for no-load calculation (model
                %parameters for no_segments = 10)
                cap = num(i,7);
                x = [.1:.1:1]*cap;
                F = zeros(no_segments,1);
                
                %Total fuel consumption by production level
                for j=1:no_segments
                    F(j) = cap*(j/no_segments)*MC(i,j);
                end
                p = polyfit(x',F,2);
                NoLOAD(i) = p(3);
            
    end
end


%xlswrite('MasterControl.xlsx',NoLOAD,'out');
    

