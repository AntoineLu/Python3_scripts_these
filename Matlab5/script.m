%%
%Importation des datas
importChampTerrestre = csvread('champTerrestre.csv',2,0);
z = -importChampTerrestre(1:102,1); %si problème chelou, prendre le même vecteur que z_bob de FittingFunction (décommenter la ligne du dessous
global z_bob
z = z_bob;
exptB = -importChampTerrestre(1:102,4); %on va fitter sur l'opposé du champ terrestre d'où le "-"
clearvars importChampTerrestre

initialParameters = [1 1 1 1 1]'; % on definit les courants initiaux dans chaque bobine.
nbrParametres = 5; %nombre de paramètres = 5 bobines.
theoB_init = arrayfun(@(x)FittingFunction5(x,initialParameters,nbrParametres),z); %On calcul le champ théorique produit par les bobines.

% Plot initial : champ des bobines avec les paramètres initiaux et
% comparaison avec l'opposé du champ terrestre
figure
plot(z, exptB,'ro',z,theoB_init)
title(strcat({'Premier tracé avec paramètres originaux - '},num2str(nbrParametres),{' bobines'}))
xlabel('Profondeur depuis la platine supérieure (m)')
ylabel('B (T)')
legend('-B_{z, terre}',strcat('B_{z, bobines} - I = [',num2str(initialParameters'),'] A'))
hold off
%%
%Optimisation
stepSize = 1e-4; %pas d'erreur autorisée
nombreIncrements = 1; %nombre d'incréments de l'algo d'optimisation

parameters = initialParameters;

figure
hold all
plot(z, exptB,'ro')
plot(z, arrayfun(@(x)FittingFunction5(x,initialParameters,nbrParametres),z))
title(strcat({'Optimisation - '},num2str(nbrParametres),{' bobines'}))
xlabel('Profondeur depuis la platine supérieure (m)')
ylabel('B (T)')
string = {'-B_{z, terre}','incr0'};
for i = 1:nombreIncrements
    newParameters = nonlinearleastsq(parameters,stepSize,z,exptB,nbrParametres,@FittingFunction5);
    parameters = newParameters;
    plot(z, arrayfun(@(x)FittingFunction5(x,newParameters,nbrParametres),z))
    string = [string,{strcat('incr',num2str(i))}];
end
legend(string)
hold off
clearvars i string parameters %nombreIncrements stepSize 
%%
%Plots résumés
global posBob

figure
plot(z, exptB,'ro')
hold on
grid on
plot(z, arrayfun(@(x)FittingFunction5(x,newParameters,nbrParametres),z))
title(strcat({'Optimisé - '},num2str(nbrParametres),{' bobines'}))
xlabel('Profondeur dans le cryostat (m)')
ylabel('B (T)')
legend('-B_{z, terre}',strcat('B_{z, bobines} - I = [',num2str(newParameters'),'] A'))
hold off

disp('Les paramètres optimaux sont :')
label = {};
unit = {};
for i=1:nbrParametres
    label = [label,{strcat('I_',num2str(i))}];
    unit = [unit,{'A'}];
end
unit = unit';
label = label';
num2str(newParameters)
horzcat(label,num2str(newParameters),unit)
clearvars label unit i
%AJOUTER POSITION CAVITÉS (ZONE COLORÉE) ET BOBINES AINSI QUE L'AMPÉRAGE AVEC UNE FLECHE
%PLUS LISIBLE.
%FAIRE LE GRAPHE DE L'ERREUR