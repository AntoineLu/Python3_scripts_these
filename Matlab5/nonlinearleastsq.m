function newParameters = nonlinearleastsq(parameters,stepSize,exptX,exptY,n,fonction)
%Calcul de la matrice Hessienne
[hessB,Hess] = Hessian(parameters,stepSize,exptX,exptY,n,fonction);
newParameters = parameters + Hess\hessB'; %Nouveaux paramètres A
end