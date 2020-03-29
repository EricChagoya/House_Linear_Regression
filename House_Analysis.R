
# Import the data set
# I called it houses
# If it is not reading the column names, you can remove '#' from
# the beginning of the text file
head(houses)

fit1 <- lm(Price.~SqftHome, data= houses)
summary(fit1)
# Low p-values
# R2= 0.8289, R2adj= 0.8252
plot(houses$Bedrooms, houses$Price.)
plot(houses$SqftHome, houses$Price.)
# There is just one wierd outlier
# Both have similar spread

fit2 <- lm(Price.~SqftHome+I(SqftHome^2), data= houses)
summary(fit2)
# Noticeably better than the model above
# R2= 0.8759, R2adj= 0.8704

fit3 <- lm(Price.~SqftHome+I(SqftHome^2)+Bathrooms, data= houses)
summary(fit3)
# R2= 0.8783, R2adj= 0.87
# Bathrooms slightly increased R2 while decreasing R2adj
# AcresLot, Bedrooms, and CarSpace all brought R2adj down

# Best model
fit4 <- lm(Price.~SqftHome+I(SqftHome^2) +Bathrooms+ SqftHome*Bathrooms, data= houses)
summary(fit4)
# R2= 0.8911, R2adj= 0.881
# Price= (6.807e+04)+ (6.164e+02)X1- (1.035e-01)X1- 
#            (3.271e+05)X2+ (1.536e+02)X1*X2
# You can make an argument that the third model is better becaause of one less
# predictor and fourth model barely outperforms it




# Just seeing what happens when you add more variables
fit5 <- lm(Price.~SqftHome+I(SqftHome^2) +Bathrooms+ SqftHome*Bathrooms+Bedrooms, data= houses)
summary(fit5)
fit6 <- lm(Price.~SqftHome+Bathrooms+ AcresLot + CarSpace+ Bedrooms, data= houses)
summary(fit6)
fit7 <- lm(Price.~SqftHome+I(SqftHome^2) +Bathrooms+ SqftHome*Bathrooms+
             Bedrooms+CarSpace+AcresLot, data= houses)
summary(fit7)
# Adding anything else just decreases R2 and R2adj
