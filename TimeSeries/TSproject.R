setwd("C:/Users/Lucille/Desktop/major courses/time series/大作业")
rm(list = ls())
library(TSA)
library(forecast)
library(lmtest)
library(fGarch)
library(readr)
library(tseries)

# This code read the data set
data <- read_csv("C:/Users/Lucille/Desktop/major courses/time series/大作业/sunspotnumbers.csv")
data.ts = as.vector(t(data[,-1]))
data.ts = ts(data.ts,start=c(1998,1), end=c(2016,12), frequency=12)

## time-series plot
plot(data.ts, type = "l", ylab='sun spot',main = "Time series plot.")
points(y=data.ts,x=time(data.ts), pch=as.vector(season(data.ts))) 

# scatter plot
y<-data.ts
x<-zlag(data.ts)# Generate first lag of the Spawners series
index = 2:length(x)          
cor(y[index],x[index])  #0.9149703

# thus the series  is higly auto correlated with the previous year 
plot(y=data.ts,x=zlag(data.ts),ylab='sunspot', xlab='Previous Year sunspot' , 
     main = "Scatter plot")

##The plots of acf,pacf
par(mfrow=c(1,2))
acf(data.ts, main="ACF of sun spot number series")
pacf(data.ts, main="PACF of sun spot number series")

## To test if the process is the stationary after differencing

### To find the value of lag in the following adfTest() function
ar(diff(data.ts)) #k=11
adf.test(data.ts,k=11)
Box.test(data.ts,lag = 12,type = "Ljung-Box")## from package(tseries)
##p-value = 0.7063

# Fails to reject the null hypothesis, we should get rid of seasonlity effect

#----------------model selecting-------------
  ## This part is to create some useful functions that helps model selecting
# This  function sort the AIC and BIC accoring to their score
sort.score <- function(x, score = c("bic", "aic")){
  if (score == "aic"){
    x[with(x, order(AIC)),]
  } else if (score == "bic") {
    x[with(x, order(BIC)),]
  } else {
    warning('score = "x" only accepts valid arguments ("aic","bic")')
  }
} 

# This function produce the out put for residual analysis
residual.analysis <- function(model, std = TRUE){
  library(TSA)
  library(tseries)
  #library(FitAR)
  if (std == TRUE){
    res.model = rstandard(model)
  }else{
    res.model = residuals(model)
  }
  par(mfrow=c(3,2))
  plot(res.model,type='o',ylab='Standardized residuals', main="Time series plot of standardised residuals")
  abline(h=0)
  hist(res.model,main="Histogram of standardized residuals")
  qqnorm(res.model,main="QQ plot of standardized residuals")
  qqline(res.model, col = 2)
  acf(res.model,main="ACF of standardised residuals")
  adf.test(res.model,nlag =11)
  for(k in 1:3)
  print(Box.test(res.model,lag = 6*k,type = "Ljung-Box"))
}

#--------------- seasonal arima model----------------------------

# First fit a plain model with only the first seasonal difference with order D = 1 
# and see if we can get rid of the seasonal trend effect
# by inspecting the autocorrelation structure of the residuals.
m1.sunspot = arima(data.ts,order=c(0,0,0),seasonal=list(order=c(0,1,0), period=4))
res.m1 = residuals(m1.sunspot);  
plot(res.m1,xlab='Time',ylab='Residuals',main="Time series plot of the residuals from m1.sunspot")
par(mfrow=c(1,2))
acf(res.m1, lag.max = 36, main = "The ACF of the residuals from m1.sunspot")
pacf(res.m1, lag.max = 36, main = "The PACF of the residuals from m1.sunspot")
ar(res.m1)#k=20
adf.test(res.m1,k=20)
Box.test(res.m1,lag = 20,type = "Ljung-Box")
# from the above time series plot we have not seen any clear trends, however seasonal lags
# are still significant in ACF and lags are in decreasing in PACF.so, we add SARMA(0,1) 
#  see if we get rid of seasonal component.

# adding MA(1) in seasoanl part
m2.sunspot = arima(data.ts,order=c(0,0,0),seasonal=list(order=c(0,1,1), period=4))
res.m2 = residuals(m2.sunspot);  
plot(res.m2,xlab='Time',ylab='Residuals',main="Time series plot of the residuals from m2.sunspot")
par(mfrow=c(1,2))
acf(res.m2, lag.max = 36, main = "The ACF of the residuals from m2.sunspot")
pacf(res.m2, lag.max = 36, main = "The PACF of the residuals from m2.sunsopt")
# first seasonal lags in ACF is resolved while others higher order are still significant 
# and decresing  patterns of lags in PACF. We think this is due to ordinary series 
ar(res.m2)#k=21
adf.test(res.m2,k=21)#p-value = 0.4939
Box.test(res.m2,lag = 12,type = "Ljung-Box")# p-value < 2.2e-16

# So, we will apply differentiating on the ordinary seris and see if we can see the trend more clearly.
m3.sunspot = arima(data.ts,order=c(0,1,0),seasonal=list(order=c(0,1,1), period=4))
ar(diff(data.ts))

res.m3 = residuals(m3.sunspot);  
plot(res.m3,xlab='Time',ylab='Residuals',main="Time series plot of the residuals from m3.sunspot")
par(mfrow=c(1,2))
acf(res.m3, lag.max = 36, main = "The ACF of the residuals m3.sunspot")
pacf(res.m3, lag.max = 36, main = "The PACF of the residuals m3.sunspot")
par(mfrow=c(1,2))
plot(decompose(res.m3)$trend,main="Trend effect of res.m3")
plot(decompose(res.m3)$seasonal,main="seasonal effect of res.m3")
ar(res.m3)
adf.test(res.m3,k=11)

m4.sunspot = arima(data.ts,order=c(0,2,0),seasonal=list(order=c(0,2,1), period=4))
res.m4 = residuals(m4.sunspot);  
plot(res.m4,xlab='Time',ylab='Residuals',main="Time series plot of the residuals from m4.sunspot")
par(mfrow=c(1,2))
acf(res.m4, lag.max = 36, main = "The ACF of the residuals m4.sunspot")
pacf(res.m4, lag.max = 36, main = "The PACF of the residuals m4.sunspot")
par(mfrow=c(1,2))
plot(decompose(res.m4)$trend,main="Trend effect of res.m4")
plot(decompose(res.m4)$seasonal,main="seasonal effect of res.m4")
ar(diff(res.m4,1,4))
adf.test(diff(res.m4,1,4),k=10)
# we get rid of trends and seaonal effects. Not a single seasonal lags in ACF and PACF are significant 
# for lower lags 

# We are going to see the possible sets of models using eacf and BIC of residulas of the 
# above models
eacf(data.ts)
res = armasubsets(y=data.ts, nar=14,nma=14,y.name='test',ar.method='ols') 
plot(res)

# From the EACF, we will include AR(1) order as well.
# SARIMA(0,1,2)x(0,1,1)_4
# SARIMA(0,1,3)x(0,1,1)_4 
# SARIMA(1,1,1)x(0,1,1)_4
# SARIMA(1,1,2)x(0,1,1)_4 and
# SARIMA(2,1,1)x(0,1,1)_4 will be fitted

# from BIC table we wil include AR(3)
# SARIMA(1,1,0)x(0,1,1)_4
# SARIMA(1,1,3)x(0,1,1)_4
# SARIMA(3,1,0)x(0,1,1)_4
# SARIMA(3,1,3)x(0,1,1)_4

##ARIMA(0,1,2)(0,1,1)_4
m4_012.sunspot = arima(data.ts ,order=c(0,1,2),seasonal=list(order=c(0,1,1), period=4),method = "ML")
res_012 = residuals(m4_012.sunspot);  
plot(res_012,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res_012, lag.max = 36, main = "The sample ACF of the residuals")
pacf(res_012, lag.max = 36, main = "The sample PACF of the residuals")
summary(m4_012.sunspot)
Box.test(res_012,lag=18)
adf.test(res_012,nlag=11)

##ARIMA(0,1,3)(0,1,1)_4
m4_013.sunspot = arima(data.ts ,order=c(0,1,3),seasonal=list(order=c(0,1,1), period=4),method = "ML")
res_013 = residuals(m4_013.sunspot);  
plot(res_013,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res_013, lag.max = 36, main = "The sample ACF of the residuals")
pacf(res_013, lag.max = 36, main = "The sample PACF of the residuals")
summary(m4_013.sunspot)

##ARIMA(1,1,0)(0,1,1)_4
m4_110.sunspot = arima(data.ts ,order=c(1,1,0),seasonal=list(order=c(0,1,1), period=4),method = "ML")
res_110 = residuals(m4_110.sunspot);  
plot(res_110,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res_110, lag.max = 36, main = "The sample ACF of the residuals")
pacf(res_110, lag.max = 36, main = "The sample PACF of the residuals")
summary(m4_110.sunspot)

##ARIMA(1,1,1)(0,1,1)_4
m4_111.sunspot = arima(data.ts ,order=c(1,1,1),seasonal=list(order=c(0,1,1), period=4),method = "ML")
res_111 = residuals(m4_111.sunspot);  
plot(res_111,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res_111, lag.max = 36, main = "The sample ACF of the residuals")
pacf(res_111, lag.max = 36, main = "The sample PACF of the residuals")
summary(m4_111.sunspot)

##ARIMA(1,1,2)(0,1,1)_4
m4_112.sunspot = arima(data.ts ,order=c(1,1,2),seasonal=list(order=c(0,1,1), period=4),method = "ML")
res_112 = residuals(m4_112.sunspot);  
plot(res_112,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res_112, lag.max = 36, main = "The sample ACF of the residuals")
pacf(res_112, lag.max = 36, main = "The sample PACF of the residuals")
summary(m4_112.sunspot)

##ARIMA(1,1,3)(0,1,1)_4
m4_113.sunspot = arima(data.ts ,order=c(1,1,3),seasonal=list(order=c(0,1,1), period=4),method = "ML")
res_113 = residuals(m4_110.sunspot);  
plot(res_113,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res_113, lag.max = 36, main = "The sample ACF of the residuals")
pacf(res_113, lag.max = 36, main = "The sample PACF of the residuals")
summary(m4_113.sunspot)

#ARIMA(2,1,1)(0,1,1)_4
m4_211.sunspot = arima(data.ts ,order=c(2,1,1),seasonal=list(order=c(0,1,1), period=4),method = "ML")
res_211 = residuals(m4_211.sunspot);  
plot(res_211,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res_211, lag.max = 36, main = "The sample ACF of the residuals")
pacf(res_211, lag.max = 36, main = "The sample PACF of the residuals")
summary(m4_211.sunspot)


##ARIMA(3,1,0)(0,1,1)_4
m4_310.sunspot = arima(data.ts ,order=c(3,1,0),seasonal=list(order=c(0,1,1), period=4),method = "ML")
res_310 = residuals(m4_310.sunspot);  
plot(res_310,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res_310, lag.max = 36, main = "The sample ACF of the residuals")
pacf(res_310, lag.max = 36, main = "The sample PACF of the residuals")
summary(m4_310.sunspot)

##ARIMA(3,1,3)(0,1,0)_4
m4_313.sunspot = arima(data.ts ,order=c(3,1,3),seasonal=list(order=c(0,1,1), period=4),method = "ML")
res_313 = residuals(m4_313.sunspot);  
plot(res_313,xlab='Time',ylab='Residuals',main="Time series plot of the residuals")
par(mfrow=c(1,2))
acf(res_313, lag.max = 36, main = "The sample ACF of the residuals")
pacf(res_313, lag.max = 36, main = "The sample PACF of the residuals")
summary(m4_313.sunspot)

## model testing
coeftest(m4_012.sunspot) 
coeftest(m4_013.sunspot)  
coeftest(m4_110.sunspot)
coeftest(m4_111.sunspot)
coeftest(m4_112.sunspot)
coeftest(m4_113.sunspot)
coeftest(m4_211.sunspot) 
coeftest(m4_310.sunspot)
coeftest(m4_313.sunspot)


sc.AIC=AIC(m4_012.sunspot, m4_013.sunspot, m4_110.sunspot,m4_112.sunspot,m4_113.sunspot,m4_211.sunspot, m4_310.sunspot,m4_313.sunspot)
sc.BIC=BIC(m4_012.sunspot, m4_013.sunspot, m4_110.sunspot,m4_112.sunspot,m4_113.sunspot,m4_211.sunspot, m4_310.sunspot,m4_313.sunspot)

sort.score(sc.AIC, score = "aic")
sort.score(sc.BIC, score = "bic")

ts.diag(model = m4_012.sunspot) 

mse_list <- c()
models <- c("m4_012.sunspot", "m4_013.sunspot", "m4_112.sunspot",
            "m4_211.sunspot", "m4_310.sunspot", "m4_313.sunspot")
for (model in models) {
  mse <- mean(get(model)$residuals^2)
  mse_list <- c(mse_list, mse)
}
mse_df <- data.frame(models, mse_list)
mse_df <- mse_df[order(mse_df$mse_list, decreasing = TRUE), ]


fit_de_1 <- decompose(sunspot)
fit_de_1$trend
par(mfrow=c(1,1))
plot(fit_de_1$trend, main = "fit_de$trend")
fit_de_1$figure
plot(1:12,fit_de_1$figure,type="l",xlab="Month",main="fit_de$figure")
mse_de <- mean(na.exclude(fit_de_1$random)^2)
mse_de

# HoltWinters
fit_hw_1 <- HoltWinters(sunspot, seasonal = "additive")
fit_hw_1
mse_hw <- mean((sunspot-fit_hw_1$fit[,1])^2)
mse_hw

# ets
fit_ets <- ets(sunspot)
fit_ets # AIC=2654.228 BIC = 2664.516 
mse_ets <- mean(fit_ets$residuals^2)
mse_ets # 485.7487

# GARCH 
library(rugarch)
spec <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
                   mean.model = list(armaOrder = c(3, 1, 3), include.mean = TRUE), 
                   distribution.model = "norm")
fit_garch <- ugarchfit(spec, sunspot)
summary(fit_garch)
fit_garch # LogLikelihood : -985.7126
fit_garch_aic <- -2*(-985.7126) + 2*sum(fit_garch@fit$varcoef)
fit_garch_bic <- -2*(-985.7126) +
  log(length(fit_garch@fit$residuals)) * length(fit_garch@fit$coef)
plot(fit_garch, which = 1)
res_garch = residuals(fit_garch)
mse_garch = mean(res_garch^2)
mse_garch # 489.0057

spec_012 <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
                       mean.model = list(armaOrder = c(0, 1, 2), include.mean = TRUE),
                       distribution.model = "norm")
fit_gar_012 <- ugarchfit(spec_012, sunspot)
summary(fit_gar_012)
fit_gar_012 # LogLikelihood : -1119.672 -985.7126
fit_gar_012_aic <- -2*(-1119.672) + 2*sum(fit_gar_012@fit$varcoef) # 2239.344 1971.425
fit_gar_012_aic
fit_gar_012_bic <- -2*(-1119.672) +
  log(length(fit_gar_012@fit$residuals)) * length(fit_gar_012@fit$coef) # 2282.779 2014.86
fit_gar_012_bic
plot(fit_gar_012, which = 1)
res_gar_012 = residuals(fit_gar_012)
mse_gar_012 = mean(res_gar_012^2)
mse_gar_012 

spec_313 <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
                       mean.model = list(armaOrder = c(3, 1, 3), include.mean = TRUE),
                       distribution.model = "norm")
fit_gar_313 <- ugarchfit(spec_313, sunspot)
plot(fit_gar_313, which = 1)
fit_gar_313 # LogLikelihood : -985.7126
fit_gar_313_aic <- -2*(-985.7126) + 2*sum(fit_gar_313@fit$varcoef) # 2239.344 1971.425
fit_gar_313_aic
fit_gar_313_bic <- -2*(-985.7126) +
  log(length(fit_gar_313@fit$residuals)) * length(fit_gar_313@fit$coef) # 2282.779 2014.86
fit_gar_313_bic
res_gar_313 = residuals(fit_gar_313)
mse_gar_313 = mean(res_gar_313^2)
mse_gar_313 # 489.0057 452.9685

c(mse_313,mse_de_1,mse_hw_1,mse_ets,mse_garch)
# 406.6898 348.6840 658.5065 485.7487 489.0057s

model_names <- c("m4_313.sunspot", "fit_de", "fit_hw",
                 "fit_ets", "fit_gar_012", "fit_gar_313")
mse_vec <- c(mse_313, mse_de_1, mse_hw_1,
             mse_ets, mse_gar_012, mse_gar_313)
mse_df <- data.frame(Model = model_names, MSE = mse_vec)
mse_df_sorted <- mse_df[order(mse_df$MSE, decreasing = TRUE),]
mse_df_sorted


# prediction
preds1 = forecast(m4_012.sunspot, h = 24)
plot(preds1)
print(preds1)
preds2 = forecast(m4_313.sunspot, h = 24)
plot(preds2)
print(preds2)
act<-read.table("C:\\Users\\lenovo\\Desktop\\时序\\SN_m_tot_V2.0.txt")
act<-act[,4]
act<-ts(act,start=c(2017,1),frequency = 12)
plot(preds1,xlim=c(2017,2018),ylim=c(-10,100),main="ARIMA012 v.s actual")
lines(act,col=2)
plot(preds2,xlim=c(2017,2018),ylim=c(-10,80),main="ARIMA313 v.s actual")
lines(act,col=2)
# model analysis
summary(m4_012.sunspot)
summary(m4_313.sunspot)