function [hessB, Hess]=Hessian(A,h,exptX,exptY,n,fonction)

M=length(A);
for i=1:M
    ABp=A; ABp(i)=A(i)+h;
    ABm=A; ABm(i)=A(i)-h;
    hessB(i)=-(sumsqerror(ABp,exptX,exptY,n,fonction)-sumsqerror(ABm,exptX,exptY,n,fonction))/(2*h);
    for j = i:M
        if (i == j)
            Ap= A; Am = A;
            Ap(i) = A(i)+h;
            Am(i) = A(i)-h;
            Hess(i,i)=(sumsqerror(Ap,exptX,exptY,n,fonction)-2*sumsqerror(A,exptX,exptY,n,fonction)+sumsqerror(Am,exptX,exptY,n,fonction))/(h*h);
        else
            App = A;
            Apm = A;
            Amp = A;
            Amm = A;
            App(i) = A(i) + h;
            App(j) = A(j) + h;
            Apm(i) = A(i) + h;
            Apm(j) = A(j) - h;
            Amp(i) = A(i) - h;
            Amp(j) = A(j) + h;
            Amm(i) = A(i) - h;
            Amm(j) = A(j) - h;
            Hess(i,j) =((sumsqerror(App,exptX,exptY,n,fonction)-sumsqerror(Apm,exptX,exptY,n,fonction))/(2*h)-(sumsqerror(Amp,exptX,exptY,n,fonction)-sumsqerror(Amm,exptX,exptY,n,fonction))/(2*h))/(2*h);
            Hess(j,i) = Hess(i,j);
        end
    end
end