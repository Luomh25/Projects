function [obj,h11r,s1r,s2r] = min_area(h11,s1,s2)%安装高度，镜面宽度，镜面高度
if s1<s2||h11<=s2/2
    obj = 10001;
    h11r = h11;
    s1r = s1;
    s2r = s2; 
else
    %定日镜总数N(面)
    N = 2564;
    %计算每月21号到春分的天数D
    d = 21;
    m = 0:1:11;
    AA = [31,28,31,30,31,30,31,31,30,31,30,31];
    D = cumsum(AA)+d;
    D = D-D(3);
    %当地时间ST
    ST=9:1.5:15;
    %太阳时角omega
    omega=pi/12*(ST-12);
    %太阳赤纬角delta的正余弦值（每天不同，12个值）
    sin_delta = sin(2*pi*D/365)*sin(2*pi/360*23.45);
    delta = sin(2*pi*D/365)*23.45;
    cos_delta = sqrt(1-sin_delta.^2);
    %当地纬度phi
    phi = 39.4*pi/180 ;
    %海拔高度H(km)
    H = 3;
    %太阳高度角alpha_s的正余弦值（每天每时不同，60个值）
    sin_alpha_s = cos_delta'*cos(omega)*cos(phi)+sin_delta'*sin(phi);%12*5
    cos_alpha_s = sqrt(1-sin_alpha_s.^2);%12*5
    %太阳方位角gamma_s的正余弦值（每天每时不同，60个值）
    cos_gamma_s = (sin_delta'-sin_alpha_s*sin(phi))./(cos_alpha_s*cos(phi));%12*5
    cos_gamma_s = cos_gamma_s';
    cos_gamma_s = cos_gamma_s(:);%60*1
    sin_gamma_s = -cos_delta'*sin(omega)./cos_alpha_s
    sin_gamma_s = sin_gamma_s';
    sin_gamma_s = sin_gamma_s(:);

    %将太阳高度角的正余弦值转为一列向量
    sin_alpha_s = sin_alpha_s';
    sin_alpha_s = sin_alpha_s(:);%每天每个时间点的数值（60*1）
    cos_alpha_s = cos_alpha_s';
    cos_alpha_s = cos_alpha_s(:);%60*1

    %sss=acos(cos_alpha_s)-cos_alpha_s;
    %太阳常数G0(kW/m^2)
    G0 = 1.366;
    %法向直接辐射辐照度DNI
    a = 0.4237-0.00821*(6-H)^2;
    b = 0.5055+0.00595*(6.5-H)^2;
    c = 0.2711+0.01858*(2.5-H)^2;
    DNI = G0*(a+b*exp(-c./sin_alpha_s));
    DNI = reshape(DNI,5,12);
    mean_DNI = mean(DNI)';

    %定日镜宽度和高度(m)
    mirror_width = s1;
    mirror_height = s2;
    %定日镜面积(m^2)
    A = mirror_width*mirror_height;
    %定日镜安装高度(m)
    h1 = h11;
    %吸收塔高度(m)
    h2 = 80;
    %定日镜坐标xy
    xy = xlsread('D:\桌面文件夹\CUMCM2023Problems\A\问题2\xy2564.xlsx');
    %镜面中心到集热器中心的距离d_HR(m)
    d_HR = sqrt(xy(:,1).^2+xy(:,2).^2+(h1-h2)^2);
    %大气透射率(其中d_HR<=1000)
    eta_at =  0.99321-0.0001176*d_HR+1.97*1e-8*d_HR.^2;
    %镜面反射率eta_ref
    eta_ref = 0.92;

    %反射光向量
    reflect = ([0,0,h2]-[xy,h1*ones(N,1)]);
    norm = sqrt(reflect(:,1).^2+reflect(:,2).^2+reflect(:,3).^2);
    reflect = reflect./norm;
    %入射光方向向量
    incident = [cos_alpha_s.*sin_gamma_s,cos_alpha_s.*cos_gamma_s,sin_alpha_s];
    %余弦效率
    cos_eff = zeros(N,60);
    for i = 1:60
        temp = sum(reflect.*incident(i,:),2);
        cos_eff(:,i) = sqrt((1+temp)/2);
    end
    cos_eff_all = real(cos_eff);
    cos_eff = mean(reshape(mean(cos_eff),5,12));%每月21日的平均余弦效率
    cos_eff = real(cos_eff);
    cos_eff_mean = mean(cos_eff);%年平均余弦效率

    %阴影遮挡效率
    eta_sb = 1;
    %集热器截断效率
    eta_trunc = 0.925;
    %定日镜的光学效率eta
    eta_all =  real(eta_sb*cos_eff_all.*eta_at*eta_trunc*eta_ref);
    eta = mean(eta_all);
    eta = mean(reshape(eta,5,12))';
    %定日镜场的输出热功率E_field
    E_field = mean(N*A*mean_DNI.*eta)/1000;
    if E_field<60
        obj = 10002;
        h11r = h11;
        s1r = s1;
        s2r = s2;
    else
        %单位面积镜面平均输出热功率
        P = mean_DNI.*eta;
        obj = s1*s2;
        h11r = h11;
        s1r = s1;
        s2r = s2; 
    end
end
end