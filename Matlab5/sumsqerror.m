function f=sumsqerror(parameters,exptX,exptY,n,fonction)
%theoY = FittingFunction2(exptX,parameters);
%theoY = fonction(exptX,parameters,n);
theoY = arrayfun(@(i)fonction(i,parameters,n),exptX);
b=(exptY-theoY).^2;
f=sum(b);
end